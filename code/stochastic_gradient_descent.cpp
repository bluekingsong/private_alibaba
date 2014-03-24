#include <cstring>
#include <iostream>
#include "linear_search.h"
#include "vec_op.h"
using namespace std;

void evaluate_gradient(const double *w,FeatureNode *x,double y,double *g,int n){
	double t=0;
	int i=0;
	while(x[i].index>0){
		t+=w[x[i].index-1]*x[i].value;
		++i;
	}
	double u=sigmod(t);
	i=0;
	memset(g,0,sizeof(g)*n);
	while(x[i].index>0){
		g[x[i].index-1]=(u-y)*x[i].value;
		++i;
	}
}

void sgd(const char* filename,int iteration,double learningRate){
	time_t t=time(0);
	cout<<"begin read probelm:"<<asctime(localtime(&t))<<endl;
	Problem prob=read_problem(filename);
	t=time(0);
	cout<<"end of read:"<<asctime(localtime(&t))<<endl;
	int iter=0;
	int n=prob.n;
	double *mem=new double[2*n];
	double *w=mem;
	double *g=mem+n;

	double fx=func_evaluate(w,g,prob);
	cout<<"init obj value="<<fx<<endl;
	while(iter++<iteration){
		double last=fx;
		for(int i=0;i<prob.l;++i){
			evaluate_gradient(w,(prob.x)[i],(prob.y)[i],g,n);
			vec_add(w,w,g,n,1.0,-learningRate);
			//if(i%10000==0) cout<<"i="<<i<<endl;
		}
		fx=func_evaluate(w,g,prob);
		double decrease=last-fx;
		cout<<"#iteration "<<iter<<" #obj_value "<<fx<<" #ave_obj "<<fx/prob.l<<endl;
		t=time(0);
		cout<<"time:"<<asctime(localtime(&t))<<endl;
	}
	delete []mem;
}
int main(int argc,char **argv){
	sgd("../data/train.lbm",6,0.002);
	return 0;
}
