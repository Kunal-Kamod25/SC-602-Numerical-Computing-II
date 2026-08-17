// differentiator.h
// This class contains the 3 finite difference methods we were asked
// to implement: forward, backward and central difference.
//
// I made the methods "static" because they don't need to remember any
// state between calls -> you just give them a function, a point x,
// and a step size h, and they hand back a number. No need to create
// an object of this class every time.

#ifndef DIFFERENTIATOR_H
#define DIFFERENTIATOR_H

#include "functions.h"

class Differentiator {
public:
    // f'(x) ~= ( f(x+h) - f(x) ) / h
    double forwardDifference(const MathFunction& func, double x, double h);

    // f'(x) ~= ( f(x) - f(x-h) ) / h
    double backwardDifference(const MathFunction& func, double x, double h);

    // f'(x) ~= ( f(x+h) - f(x-h) ) / (2h)
    double centralDifference(const MathFunction& func, double x, double h);

private:
    // shared helper that all three methods call first.
    // throws InvalidStepSizeException if h is not a valid step size.
    void validateStepSize(double h);
};

#endif // DIFFERENTIATOR_H
