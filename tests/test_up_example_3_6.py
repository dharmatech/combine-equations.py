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


def solve_numeric(equations, values, want):
    solutions = solve_system_multiple_solutions(equations, values, want)
    if len(solutions) != 1:
        raise AssertionError(f"Expected 1 solution for {want}, got {len(solutions)}")
    solution = solutions[0]
    if solution.lhs != want:
        raise AssertionError(f"Unexpected solution form: {solution}")
    return float(sp.N(solution.rhs.subs(values)))


def build_base_case():
    m = make_states_model("m", 2)
    m0, m1 = m.states
    m01 = m.edges[0]

    eqs = kinematics_fundamental(m, axes=["x", "y"])

    g = sp.symbols("g")

    eqs += eq_flat(
        m0.pos.x, 0,
        m0.pos.y, 0,
        m01.a.x, 0,
        m01.a.y, -g,
        m0.t, 0,
    )

    eqs = eliminate_zero_eqs(eqs)

    values = {
        m0.vel.x: 9.0,
        m0.vel.y: 0.0,
        m1.vel.x: 9.0,
        g: 9.8,
        m1.t: 0.50,
    }

    return eqs, values, m1


class TestUpExample36(unittest.TestCase):
    def test_position(self):
        eqs, values, m1 = build_base_case()
        x = solve_numeric(eqs, values, m1.pos.x)
        y = solve_numeric(eqs, values, m1.pos.y)
        self.assertAlmostEqual(x, 4.5, places=9)
        self.assertAlmostEqual(y, -1.225, places=9)

    def test_distance(self):
        eqs, values, m1 = build_base_case()
        dist = sp.symbols("dist")
        eqs = eqs + eq_flat(dist, sp.sqrt(m1.pos.x ** 2 + m1.pos.y ** 2))
        actual = solve_numeric(eqs, values, dist)
        self.assertAlmostEqual(actual, 4.66375653309647, places=9)

    def test_velocity(self):
        eqs, values, m1 = build_base_case()
        vel_mag = sp.symbols("vel_mag")
        vel_angle = sp.symbols("vel_angle")
        vel_angle_deg = sp.symbols("vel_angle_deg")

        eqs = eqs + eq_flat(
            vel_mag, sp.sqrt(m1.vel.x ** 2 + m1.vel.y ** 2),
            vel_angle, sp.atan2(m1.vel.y, m1.vel.x),
            vel_angle_deg, vel_angle * 180 / sp.pi,
        )

        mag_value = solve_numeric(eqs, values, vel_mag)
        angle_value = solve_numeric(eqs, values, vel_angle)
        angle_deg_value = solve_numeric(eqs, values, vel_angle_deg)

        self.assertAlmostEqual(mag_value, 10.2474387043788, places=9)
        self.assertAlmostEqual(angle_value, -0.498567905638218, places=9)
        self.assertAlmostEqual(angle_deg_value, -28.5658367937466, places=9)


if __name__ == "__main__":
    unittest.main()
