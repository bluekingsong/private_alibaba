#include <cstring>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include "als.h"

int main(int argc,char **argv){
	Problem prob=read_problem("../mat.lbm");
	int latentFactorNum=100;
	int maxIter=40;
	double objDelta=1e-8*prob.numSlots;
	double lambda=0;
	int m=40;
	alternating_least_square(prob,latentFactorNum,maxIter,objDelta,lambda,m,string("model"));
	return 0;
}
