#ifndef _ALS_H_
#define _ALS_H_
#include "common.h"
#include <string>
using namespace std;

class AlsEvaluator : public Evaluator {
public:
	//@prob the alternating least sequare problem
	//@latentLen number of latent factors(common dimension in matrix decomposition);
	AlsEvaluator(const Problem &_prob,int latentLen,double _lambda):
		xLen(_prob.l*latentLen),yLen(_prob.n*latentLen),k(latentLen),lambda(_lambda)
	{	prob=_prob; };
	void set_parameter_vec(double *_x,double *_y){
		x=_x; y=_y;
	};
	void set_derivation2FirstSet(bool mark){ derivation2FirstSet=mark; };
	int get_current_parameter(double *& para)const{
		if(derivation2FirstSet){	para=x; return xLen;}
		else{	para=y; return yLen;	};
	};
	double evaluate();
	double evaluate(double *w,double *gradient);
private:
	int xLen,yLen,k; //xLen is the length of vectorization of Matrix(x), k is the number of latent factors
	double *x; // the first subset parameters
	double *y; // the second subset parameters;
	double lambda; // regurization parameter
	bool derivation2FirstSet;
};
// prediction, matrix completion
//@user pointer of user matrix
//@item pointer of item matrix
//@k number of the latent factors
//@i row index(user)
//@j column index(item)
double predict_credit(const double *user,const double *item,int k,int i,int j);
// objective function value
//@user pointer of user matrix
//@item pointer of item matrix
//@k number of latent factors
//@g gradient vector
//@data the probelm
//@derivation2UserPara mark of which subset of parameters we derivate to
//@lambda regurization parameter
double als_obj(const double *user,const double *item,int k,double *g,const Problem &data,bool derivation2UserPara,double lambda);

void alternating_least_square(const Problem& prob,int latentFactorNum,int maxIter,double objDelta,double lambda,int m,const string& outputPrefix);
#endif
