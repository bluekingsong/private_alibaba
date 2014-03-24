#ifndef _ALS_H_
#define _ALS_H_
#include <cmath>

struct FeatureNode{
	int index; // legal index start from 0. -1 means end of the feature vector
	double value;
};

struct Problem{
	int n,l;  // number of features & number of instances
	double *y; // label
	struct FeatureNode **x;
	double bias;            /* < 0 if no bias term */
};

double als_obj(const double *user,int userNum,const double *item, int itemNum,int k,double *g,const Probelm &data,bool fixUser);
/*
double evaluator_interface(
	void *instance, // user-specified object
	double *x, // the current variables
	double *g, // gradient
	int n // number of variables
);
*/
#endif
