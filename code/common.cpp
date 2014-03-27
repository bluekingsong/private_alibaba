#include <string>
#include <fstream>
#include <iostream>
#include "common.h"
using namespace std;

int load_index_map(const string& filename, map<int,string>& indexMap){
	ifstream fin(filename.c_str());
	if(!fin.is_open()){
		cerr<<"open file "<<filename<<" failed."<<endl;
		return -1;
	}
	string item;
	int index=0;
	indexMap.clear();
	while(getline(fin,item))  indexMap[index++]=item;
	fin.close();
	return index;
}
