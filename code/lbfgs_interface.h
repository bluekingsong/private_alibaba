#ifndef _LBFGS_INTERFACE_H_
#define _LBFGS_INTERFACE_H_
#include "common.h"

// L-BFGS two-loop recursion
// @s the difference of Xk+1 and Xk for k=0 to m-1
// @y the difference of Gk+1 and Gk for k=0 to m-1
// @rho 1.0/(Yk'*Sk)
// @alpha alpha variable in the two-loop
// @g gradient at current iteration
// @n the number of parameter
// @m we keep at most latest m iteration information
// @gamma the initail approximation of inverse Hessian using gamma*I
// @result the bfgs direciton we need
void calc_bfgs_direction(double *s,double *y,double *rho,double *alpha,double *g,int n,int m,int k,double gamma,double *result);

// limited-memory BFGS optimization method
// @maxIter maximum iteration
// @objDelta minimum required decrease on objective function
// @m we keep at most lastest m iteration gradient data
// @mem the given memory, we need 2*n*m+2*m+3*n bytes, n is the number of parameter
// @evalutor the evaluator function class
void lbfgs(int maxIter,double objDelta,int m,double *mem,Evaluator& evaluator);
#endif
