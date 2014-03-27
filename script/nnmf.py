#! /usr/bin/env python
from sys import argv;
from math import log;
from datetime import datetime;
from scipy.sparse import csc_matrix;
from scipy import *;
import numpy as np;
from numpy.linalg import norm;
from sklearn.decomposition import ProjectedGradientNMF;
from convert_lbm2spa import convert;

if __name__=="__main__":
	if len(argv)!=2:
		print "usage:",argv[0],"datafile_prefix";
	else:
		clickMat=convert(argv[1]+".clk.lbm");
		buyMat=convert(argv[1]+".buy.lbm");
		model=ProjectedGradientNMF(n_components=50,init='nndsvd',tol=1e-8,max_iter=2000);
		print "nnmf start:",datetime.now();
		W,H=model.fit_transform(clickMat);
		print "nnmf end:",datetime.now();
		click_buyMat=np.dot(np.transpose(clickMat),buyMat);
		Y=np.dot(W,H);
		buyPredict=np.dot(Y,click_buyMat);
		Y[clickMat==0]=0;
		print "error=",norm(clickMat-Y);
		print buyPredict

