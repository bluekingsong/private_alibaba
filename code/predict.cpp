#include <string>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <algorithm>
#include "als.h"
using namespace std;

int read_model(const string& filename,int latentFactorNum,double *& result){
	ifstream sin(filename.c_str());
	if(!sin.is_open()){
		cerr<<"open file "<<filename<<" failed."<<endl;
		return -1;
	}
	int cnt=0;
	string line;
	while(getline(sin,line))	++cnt;
	sin.close();
	sin.open(filename.c_str());
	//sin.seekg(0,sin.beg);    don't work, Why?
	result=new double[cnt*latentFactorNum];
	for(int i=0;i<cnt*latentFactorNum;++i) sin>>result[i];
	return cnt;
}

int main(int argc,char **argv){
	string output("score");
	string lambda("0");
	string mapPrefix("../mat.");
	int latentFactorNum=100;

	double *user=0, *item=0;
	int userNum=read_model(string("model_")+lambda+string(".user"),latentFactorNum,user);
	int itemNum=read_model(string("model_")+lambda+string(".item"),latentFactorNum,item);
	map<int,string> userMap,itemMap;
	load_index_map(mapPrefix+string("user"),userMap);
	load_index_map(mapPrefix+string("brand"),itemMap);
	cout<<"users="<<userNum<<" items="<<itemNum<<endl;
	ofstream fout(output.c_str());
	for(int i=0;i<userNum;++i){
		fout<<userMap[i];
		for(int j=0;j<itemNum;++j) fout<<"\t"<<itemMap[j]<<":"<<predict_credit(user,item,latentFactorNum,i,j);
		fout<<endl;
	}
	fout.close();

	delete[] user;
	delete[] item;
	return 0;
}
