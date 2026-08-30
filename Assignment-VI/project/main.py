"""
main.py

Runs everything, one question after another. Could split this into
argparse with --q1, --q2 etc later if I need to run just one, but for
now running all of them takes like a second so not really worth it.
"""

import q1_newton_basic
import q2_unequal_spacing
import q3_more_data
import q4_newton_vs_lagrange
import q5_runge_phenomenon
import q6_numerical_differentiation


def main():
    q1_newton_basic.run()
    print()
    q2_unequal_spacing.run()
    print()
    q3_more_data.run()
    print()
    q4_newton_vs_lagrange.run()
    print()
    q5_runge_phenomenon.run()
    print()
    q6_numerical_differentiation.run()


if __name__ == "__main__":
    main()
