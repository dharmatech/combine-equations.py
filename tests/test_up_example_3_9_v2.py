import math
import sys
import unittest
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from combine_equations.kinematics_states import make_states_model, kinematics_fundamental
from combine_equations.solve_system import solve_with_elimination_attempts
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


def magnitude_and_angle_equations(obj):
    return eq_flat(
        obj.vel.x, obj.vel.mag * sp.cos(obj.vel.angle),
        obj.vel.y, obj.vel.mag * sp.sin(obj.vel.angle),
        obj.vel.mag, sp.sqrt(obj.vel.x ** 2 + obj.vel.y ** 2),
        obj.vel.angle, sp.atan2(obj.vel.y, obj.vel.x),
    )


def solve_numeric_solutions(equations, values, want):
    solutions = solve_with_elimination_attempts(equations, values, want)
    numeric = []
    for solution in solutions:
        if solution.lhs != want:
            raise AssertionError(f"Unexpected solution form: {solution}")
        numeric.append(float(sp.N(solution.rhs.subs(values))))
    return numeric


def build_window_throw_case():
    b = make_states_model("b", 2)
    b0, b1 = b.states
    b01 = b.edges[0]

    eqs = kinematics_fundamental(b, axes=["x", "y"])

    g = sp.symbols("g")

    eqs += eq_flat(
        b0.pos.x, 0,
        b01.a.x, 0,
        b01.a.y, -g,
        b0.t, 0,
        b0.vel.x, b1.vel.x,
        b1.pos.y, 0,
    )

    eqs = eliminate_zero_eqs(eqs)

    eqs += magnitude_and_angle_equations(b0)

    values = {
        g: 9.81,
        b0.pos.y: 8.0,
        b0.vel.mag: 10.0,
        b0.vel.angle: math.radians(-20.0),
    }

    return eqs, values, b1


class TestUpExample39V2(unittest.TestCase):
    def test_horizontal_range(self):
        eqs, values, b1 = build_window_throw_case()
        solutions = solve_numeric_solutions(eqs, values, b1.pos.x)
        self.assertEqual(len(solutions), 2)
        solutions = sorted(solutions)
        self.assertAlmostEqual(solutions[0], -15.7161745661753, places=9)
        self.assertAlmostEqual(solutions[1], 9.16380341748480, places=9)


if __name__ == "__main__":
    unittest.main()
