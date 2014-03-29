#! /usr/bin/env python
from sys import argv;
from math import log;
from datetime import datetime;
from scipy.sparse import csc_matrix;
from scipy import *;
import numpy as np;
from numpy.linalg import norm;
from sklearn.decomposition import ProjectedGradientNMF;

def convert2spa(filename,m,n):
	row=[];
	column=[];
	data=[];
	for line in open(filename):
		items=line[:-1].split(" ");
		i=int(items[0]);
		for item in items[1:]:
			paras=item.split(":");
			j=int(paras[0]);
			data.append(float(paras[1]));
			row.append(i-1);
			column.append(j-1);
	return csc_matrix((array(data),(array(row),array(column))),shape=(m,n));

if __name__=="__main__":
	if len(argv)!=2:
		print "usage: convert_lbm2spa.py inputfile";
	else:
		X=convert(argv[1]);
		model=ProjectedGradientNMF(n_components=20,init='nndsvd',tol=1e-8,max_iter=2000);
		print "start:",datetime.now();
		W,H=model.fit_transform(X);
		Y=np.dot(W,H);
		#Y=W*H;
		print Y.shape
		print "end:",datetime.now();
		print "error=",norm(X-Y);
