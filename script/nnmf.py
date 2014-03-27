#! /usr/bin/env python
from sys import argv;
from os import system;
from math import log;
from datetime import datetime;
from scipy.sparse import csc_matrix;
from scipy import *;
import numpy as np;
from numpy.linalg import norm;
from sklearn.decomposition import ProjectedGradientNMF;
from convert_lbm2spa import convert;
from common import load_index_map;

if __name__=="__main__":
	if len(argv)!=3:
		print "usage:",argv[0],"datafile_prefix threshold";
	else:
		t,users=load_index_map(argv[1]+".user");
		t,brands=load_index_map(argv[1]+".brand");
		clickMat=convert(argv[1]+".clk.lbm",len(users),len(brands));
		buyMat=convert(argv[1]+".buy.lbm",len(users),len(brands));
		testUCMat=convert("data/8.clk.lbm",len(users),len(brands)).todense();
		testUBMat=convert("data/8.clk.lbm",len(users),len(brands)).todense();
		model=ProjectedGradientNMF(n_components=50,init='nndsvd',tol=1e-8,max_iter=1000);
		print "nnmf start:",datetime.now();
		#W,H=model.fit_transform(clickMat);
		W,H=model.fit_transform(buyMat);
		print "nnmf end:",datetime.now();
		Y=np.dot(W,H);   # prediction

		#cuMat=np.transpose(clickMat).todense();
		#cbMat=cuMat.dot(buyMat.todense());
		#buyPredict=np.dot(Y,cbMat);
		buyPredict=Y;
		#print "error=",norm(clickMat-Y);
		fout=open("/tmp/score","w");
		for i in range(len(users)):
			content=users[i];
			for j in range(len(brands)):
				if buyPredict[i,j]<1e-5:
					continue;
				content+="\t"+brands[j]+":"+str(buyPredict[i,j]);
			fout.write(content+"\n");
		fout.close();
		Y[testUBMat==0]=0;
		print "test buy prediction error=",norm(Y-testUBMat);
		system("./script/predict.py /tmp/score data/8.txt "+argv[2]);
		print "the score file is /tmp/score, BACKUP IT!!!";

