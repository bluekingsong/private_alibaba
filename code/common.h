#ifndef _COMMON_H_
#define _COMMON_H_
#include <cmath>
#include <cstdlib>

struct FeatureNode{
	int index; // legal index start from 0. -1 means end of the feature vector
	double value;
};

struct Problem{
	int n,l;  // number of features & number of instances
	double *y; // label
	struct FeatureNode **x;
	int numSlots; // total number of FeatureNodes
	double bias;            /* < 0 if no bias term */
	~Problem(){
		free(y); free(x);
	}
};

Problem read_problem(const char *filename);

class Evaluator{
public:
	virtual double evaluate()=0;
	virtual double evaluate(double *x,double *g)=0;
	virtual int get_current_parameter(double *& x)const=0;
	double* get_gradient_vec()const{	return g;	};
	void set_gradient_vec(double *_g){	g=_g;	};
	double get_last_objvalue()const { return lastObjValue; };
	const Problem& get_problem()const { return prob; };
protected:
	Problem prob;
	double *g; // gradient vector
	double lastObjValue;
};

//double sigmod(double x);
#endif
