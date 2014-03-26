#include <cstring>
#include <cstdlib>
#include <string>
#include <iostream>
#include <fstream>
#include "linear_search.h"
#include "vec_op.h"
#include "als.h"
#include "lbfgs_interface.h"
using namespace std;

double AlsEvaluator::evaluate(){
	if(x==0||y==0||g==0){
		cerr<<"error:null pointer of parameter vectors."<<endl;
		return 0;
	}
	lastObjValue=als_obj(x,y,k,g,prob,derivation2FirstSet,lambda);
	return lastObjValue;
}
double AlsEvaluator::evaluate(double *w,double *gradient){
	if(derivation2FirstSet)	return als_obj(w,y,k,gradient,prob,derivation2FirstSet,lambda);
	lastObjValue=als_obj(x,w,k,gradient,prob,derivation2FirstSet,lambda);
	return lastObjValue;
}
double predict_credit(const double *user,const double *item,int k,int i,int j){
	double result=0.0;
	for(int a=0;a<k;++a){
		result+=user[i*k+a]*item[j*k+a];              //(*userPoint)*(*itemPoint);
	}
	return result;
}
// user= Matrix(U,K);
// item= Matrix(I,K);
double als_obj(const double *user,const double *item,int k,double *g,const Problem &data,bool derivation2UserPara,double lambda){
	if(0==g){
		cerr<<"error:null pointer of gradients g,exit."<<endl;
		return 0;
	}
	int userNum=data.l;
	int itemNum=data.n;
	if(derivation2UserPara)	memset(g,0,sizeof(g)*userNum*k);
	else	memset(g,0,sizeof(g)*itemNum*k);
	double obj=0.0;  // obj-function value
	int numSlots=0;
	for(int i=0;i<userNum;++i){
		const FeatureNode *instance=data.x[i];
		int z=0;
		while(-1!=instance[z].index){
			++numSlots;
			int j=instance[z].index-1;
			double Rij=instance[z].value;
			double r=predict_credit(user,item,k,i,j);
			obj+=(Rij-r)*(Rij-r);
			if(derivation2UserPara){  // partial derivative to user parameter
				vec_add(g+i*k,g+i*k,item+j*k,k,1,-(Rij-r));
			}else{ // partial derivative to item parameter
				vec_add(g+j*k,g+j*k,user+i*k,k,1,-(Rij-r));
			}
			++z;
		}
	}
	//regularization
	if(lambda>0){
		if(derivation2UserPara){
			for(int i=0;i<userNum*k;++i)	g[i]+=lambda*user[i];
		}else{
			for(int i=0;i<itemNum*k;++i)	g[i]+=lambda*item[i];
		}
	}
	return obj;
}
void alternating_least_square(const Problem& prob,int latentFactorNum,int maxIter,double objDelta,double lambda,int m,const string& outputPrefix){
	int userMatLen=prob.l*latentFactorNum;
	int itemMatLen=prob.n*latentFactorNum;
	int n=max(userMatLen,itemMatLen); // number of parameters
	int memLen=userMatLen+itemMatLen+n+(2*n*m+2*m+3*n);  // user para,item para, gradient, LBFGS memory
	double *mem=new double[memLen];
	double *user=mem;
	double *item=mem+userMatLen;
	double *g=mem+userMatLen+itemMatLen;
	double *lbfgsMem=mem+userMatLen+itemMatLen+n;
	// init
	//memset(mem,0,sizeof(mem)*memLen);
	for(int i=0;i<userMatLen+itemMatLen;++i)	mem[i]=double(rand())/RAND_MAX;

	AlsEvaluator evaluator(prob,latentFactorNum,lambda);
	evaluator.set_parameter_vec(user,item);
	evaluator.set_gradient_vec(g);
	int bfgsMaxIter=m;
	int numSlots=prob.numSlots;
	double lastObjValue=evaluator.evaluate();
	cout<<"MSG:initial obj value="<<lastObjValue<<" aveObj="<<lastObjValue/numSlots<<endl;
	for(int iter=0;iter<maxIter;++iter){
		evaluator.set_derivation2FirstSet(true); // first optimization to user matrix
		lbfgs(bfgsMaxIter,1e-8,m,lbfgsMem,evaluator);
		evaluator.set_derivation2FirstSet(false); // then optimization to item matrix
		lbfgs(bfgsMaxIter,1e-8,m,lbfgsMem,evaluator);
		double objValue=evaluator.get_last_objvalue();
		cout<<"at iteration #"<<iter<<" objValue #"<<objValue<<" aveObj #"<<objValue/numSlots<<" decrease #"<<lastObjValue-objValue<<endl;
		if(lastObjValue-objValue<objDelta){
			cout<<"MSG:objValue decrease not meet requirement. target:"<<objDelta<<" now:"<<lastObjValue-objValue<<endl;
			break;
		}
		lastObjValue=objValue;
	}
	string output=outputPrefix+string(".user");
	ofstream outfile(output.c_str());
	for(int i=0;i<prob.l;++i){
		outfile<<user[i*latentFactorNum];
		for(int j=1;j<latentFactorNum;++j) outfile<<" "<<user[i*latentFactorNum+j];
		outfile<<endl;
	}
	outfile.close();
	output=outputPrefix+string(".item");
	outfile.open(output.c_str());
	for(int i=0;i<prob.n;++i){
		outfile<<item[i*latentFactorNum];
		for(int j=1;j<latentFactorNum;++j)	outfile<<" "<<item[i*latentFactorNum+j];
		outfile<<endl;
	}
	outfile.close();
	delete[] mem;
};

