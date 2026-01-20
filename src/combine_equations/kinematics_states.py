"""
kinematics_states.py

A small SymPy-based kinematics "equation generator" library.

Core ideas:
- "States" holds an arbitrary number of states for one object.
- Edge variables (dt, a, optional v_av) live between state i and i+1.
- Generate the three fundamental equations (EQ2/EQ7/EQ10) component-wise,
  restricted to chosen axes.

This file intentionally does NOT include a solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence

import sympy as sp


# ----------------------------
# Data structures
# ----------------------------

Axis = Literal["x", "y", "z"]


@dataclass(frozen=True)
class Point3:
    """A fixed 3-component container used for position/velocity/acceleration."""
    x: sp.Symbol
    y: sp.Symbol
    z: sp.Symbol
    
    # optional propertys for polar/magnitude-angle representation
    mag: sp.Symbol | None = None
    angle: sp.Symbol | None = None

    def get(self, axis: Axis) -> sp.Symbol:
        return getattr(self, axis)

    @staticmethod
    def make(prefix: str) -> "Point3":
        return Point3(
            x=sp.Symbol(f"{prefix}_x"),
            y=sp.Symbol(f"{prefix}_y"),
            z=sp.Symbol(f"{prefix}_z"),
        )

def make_point(prefix: str) -> Point3:
    return Point3(
        x = sp.symbols(f"{prefix}_x"),
        y = sp.symbols(f"{prefix}_y"),
        z = sp.symbols(f"{prefix}_z"),

        mag = sp.symbols(f"{prefix}_mag"),
        angle=sp.symbols(f"{prefix}_angle")
    )


@dataclass(frozen=True)
class State:
    """
    One discrete state of an object: (pos, vel, t).

    Note:
    - acceleration is not stored here (to avoid duplication with edge acceleration).
    - if you *really* want per-state acceleration later, you can add it and then
      add consistency constraints tying it to edge acceleration.
    """
    pos: Point3
    vel: Point3
    t: sp.Symbol


@dataclass(frozen=True)
class EdgeVars:
    """Variables associated with the interval from state i to i+1."""
    dt: sp.Symbol         # Δt_i = t_{i+1} - t_i (optional but recommended)
    a: Point3             # acceleration over the interval i→i+1
    v_av: Point3 | None   # average velocity over interval (optional helper)


@dataclass(frozen=True)
class IntervalView:
    """Convenience view: state i to i+1 along with edge vars."""
    i: int
    s0: State
    s1: State
    e: EdgeVars


@dataclass
class StatesModel:
    """
    A multi-state model for a single object.

    - states: list of node states
    - edges:  list of edge vars between consecutive states (len = len(states)-1)
    """
    states: list[State]
    edges: list[EdgeVars]

    @property
    def n(self) -> int:
        return len(self.states)

    def interval(self, i: int) -> IntervalView:
        if i < 0 or i >= self.n - 1:
            raise IndexError(f"interval index {i} out of range for n={self.n}")
        return IntervalView(i=i, s0=self.states[i], s1=self.states[i + 1], e=self.edges[i])


# ----------------------------
# Constructors
# ----------------------------

def make_states_model(
    prefix: str,
    n_states: int,
    *,
    include_v_av: bool = True,
) -> StatesModel:
    """
    Create a model with n_states = N, and N-1 edges.

    Naming scheme (example prefix="m"):
      states:
        m_0_x, m_0_v_x, m_0_t, ...
        m_1_x, ...
      edges:
        dt_m_0_1, a_x_m_0_1, ...
        v_av_x_m_0_1, ... (if include_v_av)

    """
    if n_states < 2:
        raise ValueError("n_states must be >= 2")

    states: list[State] = []
    edges: list[EdgeVars] = []

    for i in range(n_states):
        pos = Point3.make(f"{prefix}_{i}")
        # velocity components are conventionally named with v_*
        vel = Point3(
            x=sp.Symbol(f"{prefix}_{i}_v_x"),
            y=sp.Symbol(f"{prefix}_{i}_v_y"),
            z=sp.Symbol(f"{prefix}_{i}_v_z"),

            mag=sp.Symbol(f"{prefix}_{i}_v_mag"),
            angle=sp.Symbol(f"{prefix}_{i}_v_angle"),
        )
        t = sp.Symbol(f"{prefix}_{i}_t")
        states.append(State(pos=pos, vel=vel, t=t))

    for i in range(n_states - 1):
        dt = sp.Symbol(f"dt_{prefix}_{i}_{i+1}")

        a = Point3(
            x=sp.Symbol(f"a_x_{prefix}_{i}_{i+1}"),
            y=sp.Symbol(f"a_y_{prefix}_{i}_{i+1}"),
            z=sp.Symbol(f"a_z_{prefix}_{i}_{i+1}"),
        )

        v_av = None
        if include_v_av:
            v_av = Point3(
                x=sp.Symbol(f"v_av_x_{prefix}_{i}_{i+1}"),
                y=sp.Symbol(f"v_av_y_{prefix}_{i}_{i+1}"),
                z=sp.Symbol(f"v_av_z_{prefix}_{i}_{i+1}"),
            )

        edges.append(EdgeVars(dt=dt, a=a, v_av=v_av))

    return StatesModel(states=states, edges=edges)


def normalize_axes(axes: Sequence[Axis] | None) -> tuple[Axis, ...]:
    """Default to 1D-x if not specified; validate axes."""
    if axes is None:
        axes = ("x",)
    axes_t = tuple(axes)
    valid = {"x", "y", "z"}
    for a in axes_t:
        if a not in valid:
            raise ValueError(f"Invalid axis: {a!r}. Must be one of {sorted(valid)}")
    if len(set(axes_t)) != len(axes_t):
        raise ValueError(f"Duplicate axes not allowed: {axes_t}")
    return axes_t


# ----------------------------
# Fundamental kinematics equations (EQ2, EQ7, EQ10)
# ----------------------------

def eq_dt_def(model: StatesModel) -> list[sp.Eq]:
    """
    Define dt on each edge:
      dt_i = t_{i+1} - t_i
    This makes prints cleaner and later elimination more controlled.
    """
    eqs: list[sp.Eq] = []
    for i in range(model.n - 1):
        I = model.interval(i)
        eqs.append(sp.Eq(I.e.dt, I.s1.t - I.s0.t))
    return eqs


def eq2_avg_velocity(model: StatesModel, *, axes: Sequence[Axis] | None = None) -> list[sp.Eq]:
    """
    EQ2: average velocity definition (component-wise):
      v_av = (x1 - x0) / (t1 - t0)
    In our model we prefer dt:
      v_av = (x1 - x0) / dt
    Requires include_v_av=True in model creation.
    """
    axes_t = normalize_axes(axes)
    eqs: list[sp.Eq] = []
    for i in range(model.n - 1):
        I = model.interval(i)
        if I.e.v_av is None:
            raise ValueError("Model was created with include_v_av=False; EQ2 requires v_av.")
        for ax in axes_t:
            eqs.append(
                sp.Eq(
                    I.e.v_av.get(ax),
                    (I.s1.pos.get(ax) - I.s0.pos.get(ax)) / I.e.dt,
                )
            )
    return eqs


def eq7_acceleration(model: StatesModel, *, axes: Sequence[Axis] | None = None) -> list[sp.Eq]:
    """
    EQ7: acceleration definition (component-wise):
      a = (v1 - v0) / (t1 - t0)
    Using dt:
      a = (v1 - v0) / dt
    """
    axes_t = normalize_axes(axes)
    eqs: list[sp.Eq] = []
    for i in range(model.n - 1):
        I = model.interval(i)
        for ax in axes_t:
            eqs.append(
                sp.Eq(
                    I.e.a.get(ax),
                    (I.s1.vel.get(ax) - I.s0.vel.get(ax)) / I.e.dt,
                )
            )
    return eqs


def eq10_vavg_mean_endpoints(model: StatesModel, *, axes: Sequence[Axis] | None = None) -> list[sp.Eq]:
    """
    EQ10: average velocity equals mean of endpoint velocities:
      v_av = (v0 + v1)/2
    This is the relation that (in textbooks) is tied to constant acceleration.
    Requires include_v_av=True.
    """
    axes_t = normalize_axes(axes)
    eqs: list[sp.Eq] = []
    for i in range(model.n - 1):
        I = model.interval(i)
        if I.e.v_av is None:
            raise ValueError("Model was created with include_v_av=False; EQ10 requires v_av.")
        for ax in axes_t:
            eqs.append(
                sp.Eq(
                    I.e.v_av.get(ax),
                    (I.s0.vel.get(ax) + I.s1.vel.get(ax)) / 2,
                )
            )
    return eqs


def kinematics_fundamental(
    model: StatesModel,
    *,
    axes: Sequence[Axis] | None = None,
    include_dt_defs: bool = True,
    include_eq2: bool = True,
    include_eq7: bool = True,
    include_eq10: bool = True,
) -> list[sp.Eq]:
    """
    Convenience: build a standard set of fundamental equations.

    Typical usage for constant-acceleration problems:
      include_dt_defs=True
      include_eq2=True
      include_eq7=True
      include_eq10=True

    If you want to explore non-constant acceleration (where EQ10 may not apply),
    you can set include_eq10=False.
    """
    eqs: list[sp.Eq] = []
    if include_dt_defs:
        eqs += eq_dt_def(model)
    if include_eq2:
        eqs += eq2_avg_velocity(model, axes=axes)
    if include_eq7:
        eqs += eq7_acceleration(model, axes=axes)
    if include_eq10:
        eqs += eq10_vavg_mean_endpoints(model, axes=axes)
    return eqs


# ----------------------------
# Dimension/axis helpers (constraints or substitutions)
# ----------------------------

def axis_zero_constraints(
    model: StatesModel,
    *,
    keep: Sequence[Axis] = ("x",),
    include_edge_vars: bool = True,
) -> list[sp.Eq]:
    """
    Return explicit equations constraining all non-kept axes to 0.

    This is the declarative way to "flatten" a 3D model to 2D/1D.

    Example:
      axis_zero_constraints(model, keep=("x",))   -> constrain y,z to 0 everywhere
      axis_zero_constraints(model, keep=("x","z"))-> constrain y to 0 everywhere
    """
    keep_t = normalize_axes(keep)
    kill = tuple(ax for ax in ("x", "y", "z") if ax not in keep_t)

    eqs: list[sp.Eq] = []
    zero = sp.Integer(0)

    for s in model.states:
        for ax in kill:
            eqs.append(sp.Eq(s.pos.get(ax), zero))
            eqs.append(sp.Eq(s.vel.get(ax), zero))

    if include_edge_vars:
        for e in model.edges:
            for ax in kill:
                eqs.append(sp.Eq(e.a.get(ax), zero))
                if e.v_av is not None:
                    eqs.append(sp.Eq(e.v_av.get(ax), zero))

    return eqs


def axis_zero_substitution_map(
    model: StatesModel,
    *,
    keep: Sequence[Axis] = ("x",),
    include_edge_vars: bool = True,
) -> dict[sp.Symbol, sp.Integer]:
    """
    Return a substitution map {sym: 0} for all non-kept axes.
    This is the procedural/printing-friendly way to collapse 3D to 1D/2D.

    You'll typically apply it, simplify, and drop tautologies in your own pipeline.
    """
    keep_t = normalize_axes(keep)
    kill = tuple(ax for ax in ("x", "y", "z") if ax not in keep_t)

    sub: dict[sp.Symbol, sp.Integer] = {}
    zero = sp.Integer(0)

    for s in model.states:
        for ax in kill:
            sub[s.pos.get(ax)] = zero
            sub[s.vel.get(ax)] = zero

    if include_edge_vars:
        for e in model.edges:
            for ax in kill:
                sub[e.a.get(ax)] = zero
                if e.v_av is not None:
                    sub[e.v_av.get(ax)] = zero

    return sub


# ----------------------------
# Small convenience helpers
# ----------------------------

def constant_velocity_constraints(model: StatesModel, v_const: Point3 | sp.Symbol, *, axes: Sequence[Axis] | None = None) -> list[sp.Eq]:
    """
    Constrain velocity of every state to a constant.

    If v_const is a Symbol, it applies to each chosen axis (1D usage).
    If v_const is a Point3, it uses components.
    """
    axes_t = normalize_axes(axes)
    eqs: list[sp.Eq] = []

    for s in model.states:
        for ax in axes_t:
            if isinstance(v_const, Point3):
                eqs.append(sp.Eq(s.vel.get(ax), v_const.get(ax)))
            else:
                eqs.append(sp.Eq(s.vel.get(ax), v_const))

    return eqs


def link_same_time(a: State, b: State, t_sym: sp.Symbol | None = None) -> list[sp.Eq]:
    """
    Constrain two states to share the same time.
    Optionally introduce a named time symbol t_sym with:
      t_sym = a.t and t_sym = b.t
    """
    if t_sym is None:
        return [sp.Eq(a.t, b.t)]
    return [sp.Eq(t_sym, a.t), sp.Eq(t_sym, b.t)]


def link_same_position(a: State, b: State, *, axes: Sequence[Axis] | None = None, dist_sym: sp.Symbol | None = None) -> list[sp.Eq]:
    """
    Constrain two states to share the same position on chosen axes.
    Optionally introduce a named distance-like symbol dist_sym per axis is not handled here;
    if you want a single scalar 'dist' in 1D, pass axes=("x",) and dist_sym=dist.
    """
    axes_t = normalize_axes(axes)
    eqs: list[sp.Eq] = []

    if dist_sym is not None:
        if axes_t != ("x",):
            raise ValueError("dist_sym is intended for 1D usage: axes=('x',)")
        eqs.append(sp.Eq(dist_sym, a.pos.x))
        eqs.append(sp.Eq(dist_sym, b.pos.x))
        return eqs

    for ax in axes_t:
        eqs.append(sp.Eq(a.pos.get(ax), b.pos.get(ax)))
    return eqs

from combine_equations.misc import eq_flat

def magnitude_and_angle_equations(obj: State) -> list:
    eqs = eq_flat(
        obj.vel.x,    obj.vel.mag*sp.cos(obj.vel.angle),
        obj.vel.y,    obj.vel.mag*sp.sin(obj.vel.angle),

        obj.vel.mag,   sp.sqrt(obj.vel.x**2 + obj.vel.y**2),
        obj.vel.angle, sp.atan2(obj.vel.y, obj.vel.x)
    )

    return eqs        