#! /usr/bin/env python
from sys import argv;
from math import exp,log;
from cPickle import load,dump;
from datetime import datetime;
from common import load_index_map;
import numpy as np;
from nnmf import nmf;
from convert_lbm2spa import convert2spa;

def cos_distance(v1,v2):
	#print v1.shape,"---",v2.shape
	a=np.dot(v1,np.transpose(v2));
	n1=np.linalg.norm(v1);
	n2=np.linalg.norm(v2);
	if(n1*n2<1e-10):
		return -1;
		#print "a=%f,n1=%f,n2=%f"%(a,n1,n2);
	return a[0,0]/(n1*n2);
def convert_mat2map(mat,threshold=1):
	Map={};
	(m,n)=mat.shape;
	for i in xrange(m):
		Map[i]=set();
		for j in xrange(n):
			if mat[i,j]>=threshold:
				Map[i].add(j);
		if len(Map[i])==0:
			print "Empty Row",i;
	return Map;
def jaccard_sim_dict(Map,threshold=0.2):
	sim_dict=[];
	invalid=0;
	for i in xrange(len(Map)):
		ui={};
		sim_dict.append(ui);
		if len(Map[i])==0:
			continue;
		for j in xrange(len(Map)):
			if i==j:
				ui[j]=1;
			else:
				s=float(len(Map[i].intersection(Map[j])))/len(Map[i].union(Map[j]));
				if s>=threshold:
					ui[j]=s;
	return sim_dict;
def build_cos_distance(rowMat):  ## row to row similar
	(m,n)=rowMat.shape;
	sim_dict=[];
	memo={};
	invalidCnt=0;
	for i in xrange(m):
		ui={};
		sim_dict.append(ui);
		if np.linalg.norm(rowMat[i,:])<1e-10:
			print "invalid row index=",i;
			print "content=",rowMat[i,:];
			invalidCnt+=1;
		for j in xrange(m):
			if i==j:
				ui[j]=1.0; #TODO: or set it to -1
			elif i>j:
				ui[j]=memo[(i,j)];
			else:
				ui[j]=cos_distance(rowMat[i,:],rowMat[j,:]);
				if ui[j]>1+1e-6:
					print "Error cos result for index=",i,"cos=",ui[j];
				memo[(j,i)]=ui[j];
		##TODO: debug
		#if i==100:
		#	break;
		if i%200==0:
			print "building similar dict,progress:",i,"time:",datetime.now();
	if invalidCnt>0:
		print "invalid row parameter vectors:",invalidCnt;
	return sim_dict;

if __name__=="__main__":
	if len(argv)!=3:
		print "usage:",argv[0],"traindata_prefix(say,data/mat) nearest_neigbor_num";
	else:
		trainfile=argv[1];
		userMap,userIndex=load_index_map(argv[1]+".user");
		itemMap,itemIndex=load_index_map(argv[1]+".brand");
		knn=int(argv[2]);
		clickMat=convert2spa(argv[1]+".clk.lbm",len(userIndex),len(itemIndex));
		userFreqs=[clickMat[:,i].getnnz() for i in xrange(len(itemIndex))];
		clickMat=clickMat.todense();
		clickMat[clickMat>100]=100;  ## drop outlier 61/32760=0.00186203
		clickMat=clickMat/100.0;
		for i in xrange(len(itemIndex)):
			clickMat[:,i]=log(float(len(userIndex))/userFreqs[i])*clickMat[:,i];
		buyMat=convert2spa(argv[1]+".buy.lbm",len(userIndex),len(itemIndex)).todense();
		buyMat[buyMat>16]=16;     ## drop outlier 10/4317=0.00231642
		buyMat=buyMat/16.0;
		#UK,KC=nmf(clickMat,max_iter=5);
		#print "UK shape=",UK.shape," clickMat shape=",clickMat.shape;
		sim_dict=build_cos_distance(clickMat);
		dump(sim_dict,open("/tmp/usersim_dict","wb"));
		#sim_dict=load(open("/tmp/usersim_dict","rb"));
		#sim_dict=jaccard_sim_dict(convert_mat2map(clickMat));
		sim_dict=[sorted(x.items(),key=lambda x:x[1],reverse=True) for x in sim_dict];
		fout=open("/tmp/usersim_score","w");
		for i in xrange(len(sim_dict)):
			usim=sim_dict[i];
			if len(usim)==0 or usim[0][1]<0:
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
		print "score file is /tmp/usersim_score,BACKUP it!!";

