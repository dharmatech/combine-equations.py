import math
import sys
import unittest
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from combine_equations.kinematics_states import make_states_model, kinematics_fundamental
from combine_equations.solve_system import solve_system_multiple_solutions
from combine_equations.eliminate_variable_subst import eliminate_variable_subst


def eq_flat(*items):
    if len(items) % 2:
        raise ValueError(f"eq_flat needs an even number of items; got {len(items)}")
    return [sp.Eq(items[i], items[i + 1]) for i in range(0, len(items), 2)]


def eliminate_zero_eqs(equations):
    eqs_zero = [eq for eq in equations if eq.rhs == 0]
    tmp = equations
    for eq in eqs_zero:
        var = eq.lhs
        tmp, _ = eliminate_variable_subst(tmp, var)
    return tmp


def solve_numeric_solutions(equations, values, want):
    equations = [eq.subs(values) for eq in equations]
    solutions = solve_system_multiple_solutions(equations, values, want)
    numeric = []
    for solution in solutions:
        if solution.lhs != want:
            raise AssertionError(f"Unexpected solution form: {solution}")
        numeric.append(float(sp.N(solution.rhs.subs(values))))
    return numeric


def solve_numeric(equations, values, want):
    solutions = solve_numeric_solutions(equations, values, want)
    if len(solutions) != 1:
        raise AssertionError(f"Expected 1 solution for {want}, got {len(solutions)}")
    return solutions[0]


def build_projectile_case():
    b = make_states_model("b", 2)
    b0, b1 = b.states
    b01 = b.edges[0]

    eqs = kinematics_fundamental(b, axes=["x", "y"])

    g = sp.symbols("g")

    eqs += eq_flat(
        b0.pos.x, 0,
        b0.pos.y, 0,
        b01.a.x, 0,
        b01.a.y, -g,
        b0.t, 0,
        b0.vel.x, b1.vel.x,
    )

    eqs = eliminate_zero_eqs(eqs)

    b0_vel_mag = sp.symbols("b0_vel_mag")
    b0_vel_angle = sp.symbols("b0_vel_angle")

    eqs += eq_flat(
        b0.vel.x, b0_vel_mag * sp.cos(b0_vel_angle),
        b0.vel.y, b0_vel_mag * sp.sin(b0_vel_angle),
    )

    values = {
        g: 9.81,
        b0_vel_mag: 37.0,
        b0_vel_angle: math.radians(53.1),
    }

    return eqs, values, b1


class TestUpExample37(unittest.TestCase):
    def test_position_and_velocity_at_t(self):
        eqs, values, b1 = build_projectile_case()
        values[b1.t] = 2.0

        x = solve_numeric(eqs, values, b1.pos.x)
        y = solve_numeric(eqs, values, b1.pos.y)
        vx = solve_numeric(eqs, values, b1.vel.x)
        vy = solve_numeric(eqs, values, b1.vel.y)

        self.assertAlmostEqual(x, 44.4310966741154, places=9)
        self.assertAlmostEqual(y, 39.5566647280447, places=9)
        self.assertAlmostEqual(vx, 22.2155483370577, places=9)
        self.assertAlmostEqual(vy, 9.96833236402235, places=9)

        vel_mag = sp.symbols("vel_mag")
        vel_angle = sp.symbols("vel_angle")
        vel_angle_deg = sp.symbols("vel_angle_deg")

        eqs_vel = eqs + eq_flat(
            vel_mag, sp.sqrt(b1.vel.x ** 2 + b1.vel.y ** 2),
            vel_angle, sp.atan2(b1.vel.y, b1.vel.x),
            vel_angle_deg, vel_angle * 180 / sp.pi,
        )

        mag = solve_numeric(eqs_vel, values, vel_mag)
        angle = solve_numeric(eqs_vel, values, vel_angle)
        eqs_deg, _ = eliminate_variable_subst(eqs_vel, vel_angle)
        angle_deg = solve_numeric(eqs_deg, values, vel_angle_deg)

        self.assertAlmostEqual(mag, 24.3495018026193, places=9)
        self.assertAlmostEqual(angle, 0.421780406158419, places=9)
        self.assertAlmostEqual(angle_deg, 24.1662371541911, places=9)

    def test_highest_point(self):
        eqs, values, b1 = build_projectile_case()
        eqs = eqs + eq_flat(b1.vel.y, 0)

        t_peak = solve_numeric(eqs, values, b1.t)
        height = solve_numeric(eqs, values, b1.pos.y)

        self.assertAlmostEqual(t_peak, 3.01613989439575, places=9)
        self.assertAlmostEqual(height, 44.6212748258844, places=9)

    def test_range_and_impact_velocity(self):
        eqs, values, b1 = build_projectile_case()
        eqs = eqs + eq_flat(b1.pos.y, 0)
        x = solve_numeric(eqs, values, b1.pos.x)
        vx = solve_numeric(eqs, values, b1.vel.x)
        vy = solve_numeric(eqs, values, b1.vel.y)

        self.assertAlmostEqual(x, 134.010403230554, places=9)
        self.assertAlmostEqual(vx, 22.2155483370577, places=9)
        self.assertAlmostEqual(vy, -29.5883323640224, places=9)
        


if __name__ == "__main__":
    unittest.main()
