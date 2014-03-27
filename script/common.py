#! /usr/bin/env python
from sys import argv;
from math import log;

def load_index_map(filename):
	indexMap={};
	indies=[];
	cnt=1;
	for line in open(filename):
		key=line[:-1].split("\t")[0];
		indexMap[key]=cnt;
		cnt+=1;
		indies.append(key);
	return indexMap,indies;



