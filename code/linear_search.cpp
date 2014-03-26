#include <iostream>
#include "linear_search.h"
#include "vec_op.h"
using namespace std;

double backtracking_linear_search(
	Evaluator& evaluator,   // class of objective function value evaluation
	double *xp, // backup place for x
	double *p, // negative of search direction
	double *fx, // current function value at x
	double c, // sufficient decrease condition threshold
	double init_step, // initial step length
	double r, // scale factor in backtracking
	int *evaluateCnt // counter
){
	double *x=0; //current points
	int n=evaluator.get_current_parameter(x);
	double *g=evaluator.get_gradient_vec();
	double dec=vec_dot(g,p,n);
	//cout<<"#IN_LINEAR_SEARCH unit decrease of g'p="<<dec<<endl;
	if(dec<0){ // non suitable step,p is not a descent search direction
		return -1;
	}
//	for(int i=0;i<5;i++) 		cout<<"x["<<i<<"]="<<x[i]<<" p["<<i<<"]="<<p[i]<<endl; 
	double alpha=init_step;
	vec_add(xp,x,p,n,1,-alpha);  // p is the negative of search of direction
	double old_fx=*fx;
	*fx=evaluator.evaluate(xp,g);
	++(*evaluateCnt);
	int trials=0;
	while( *fx > old_fx-alpha*c*dec ){
		//cout<<"-----try step length "<<alpha<<" get obj="<<*fx<<" dec="<<old_fx-*fx<<" require min dec="<<alpha*c*dec<<endl;
		alpha*=r;
		vec_add(xp,x,p,n,1,-alpha);
		*fx=evaluator.evaluate(xp,g);
		++(*evaluateCnt);
		++trials;
	}
	//cout<<"#IN_LINEAR_SEARCH success linear search, get alpha="<<alpha<<" obj="<<*fx<<" dec="<<old_fx-*fx<<" required min dec="<<alpha*c*dec<<" trails="<<trials<<endl;
	return alpha;
}

double guess_init_step(const double *g,const int n,int iter){
	double result=abs(g[0]);
	for(int i=1;i<n;++i){
		result=max(result,abs(g[i]));
	}
	return 1.0/result*pow(0.9,iter-1);
}
