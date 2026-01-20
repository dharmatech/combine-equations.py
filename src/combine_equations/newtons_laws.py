
from combine_equations.kinematics_states import Point3

from combine_equations.misc import eq_flat

def superposition_equations(R: Point3, forces: list[Point3]):
    eqs = []

    eqs += eq_flat(
        R.x, sum(f.x for f in forces),
        R.y, sum(f.y for f in forces)
    )

    return eqs

def newtons_second_law(forces: list[Point3], mass: sp.Symbol, acceleration: Point3):
    # F = m*a
    eqs = []
    
    # for coord in ['x', 'y']:
    #     eqs += eq_flat(
    #         sum(getattr(f, coord) for f in forces),
    #         mass * getattr(acceleration, coord)
    #     )

    eqs += eq_flat(
        sum(f.x for f in forces),    mass * acceleration.x,
        sum(f.y for f in forces),    mass * acceleration.y,
    )

    return eqs
