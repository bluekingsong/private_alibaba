#include <cstring>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <fstream>
#include "als.h"

int main(int argc,char **argv){
	if(argc!=3){
		cerr<<"usage: "<<argv[0]<<" train_data(lbm) latentFactorNum"<<endl;
		return 1;
	}
	Problem prob=read_problem(argv[1]);
	int latentFactorNum=atoi(argv[2]);
	int maxIter=40;
	double objDelta=1e-8*prob.numSlots;
	double lambda=0;
	int m=60;
	ostringstream os;
	os<<"model_"<<lambda;
	alternating_least_square(prob,latentFactorNum,maxIter,objDelta,lambda,m,os.str());
	return 0;
}
