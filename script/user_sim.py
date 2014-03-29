#! /usr/bin/env python
from sys import argv;
from math import exp;
from common import load_index_map;
import numpy as np;
from nnmf import nmf;
from convert_lbm2spa import convert2spa;

def cos_distance(v1,v2):
	print v1.shape,"---",v2.shape
	a=np.dot(v1,v2);
	n1=np.linalg.norm(v1);
	n2=np.linalg.norm(v2);
	if(n1*n2<1e-10):
		return -1;
		#print "a=%f,n1=%f,n2=%f"%(a,n1,n2);
	return a/(n1*n2);
def build_sim_dict(userLatentMat):
	(m,n)=userLatentMat.shape;
	sim_dict=[];
	memo={};
	invalidCnt=0;
	for i in xrange(m):
		ui={};
		sim_dict.append(ui);
		if np.linalg.norm(userLatentMat[i,:])<1e-10:
			invalidCnt+=1;
		for j in xrange(m):
			if i==j:
				ui[j]=1.0; #TODO: or set it to -1
			elif i>j:
				ui[j]=memo[(i,j)];
			else:
				ui[j]=cos_distance(userLatentMat[i,:],userLatentMat[j,:]);
				memo[(j,i)]=ui[j];
	print "invalid user parameter vectors:",invalidCnt;
	return sim_dict;

if __name__=="__main__":
	if len(argv)!=3:
		print "usage:",argv[0],"traindata_prefix(say,data/mat) nearest_neigbor_num";
	else:
		trainfile=argv[1];
		userMap,userIndex=load_index_map(argv[1]+".user");
		itemMap,itemIndex=load_index_map(argv[1]+".brand");
		knn=int(argv[2]);
		clickMat=convert2spa(argv[1]+".clk.lbm",len(userIndex),len(itemIndex)).todense();
		buyMat=convert2spa(argv[1]+".buy.lbm",len(userIndex),len(itemIndex)).todense();
		clickMat[clickMat>100]=100;  ## drop outlier 61/32760=0.00186203
		clickMat=clickMat/100.0;
		buyMat[buyMat>16]=16;     ## drop outlier 10/4317=0.00231642
		buyMat=buyMat/16.0;
		#UK,KC=nmf(clickMat,max_iter=1000);
		sim_dict=build_sim_dict(clickMat);
		fout=open("/tmp/sim_score","w");
		for i in xrange(len(sim_dict)):
			usim=sim_dict[i];
			usim=sorted(usim.items(),key=lambda x:x[1],reverse=True);
			if usim[0][1]<0:
				continue;
			score=np.array([[0.0]*len(itemIndex),]);
			for para in usim[:knn]:
				score+=para[1]*buyMat[para[0],:];
			content=userIndex[i];
			for j in xrange(len(itemIndex)):
				if score[0,j]>1e-5:
					content+="\t"+itemIndex[j]+":"+str(score[0,j]);
			fout.write(content+"\n");
		fout.close();
		print "score file is /tmp/sim_score,BACKUP it!!";

