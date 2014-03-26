#include <cstring>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include "als.h"

int read_model(const string& filename,int latentFactorNum,double *& result){
	ifstream sin(filename.c_str());
	int cnt=0;
	string line;
	while(getline(sin,line))	+cnt;

	result=new double[cnt*latentFactorNum];
	for(int

}

int main(int argc,char **argv){
	return 0;
}
