#! /usr/bin/env python
from sys import argv;
from math import exp,log;
from cPickle import load,dump;
import numpy as np;
from scipy.sparse import csr_matrix;
from common import load_index_map;
from nnmf import nmf;
from convert_lbm2spa import convert2spa;
from user_sim import build_cos_distance;

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
        buyMat=convert2spa(argv[1]+".buy.lbm",len(userIndex),len(itemIndex));
        clickMat=clickMat.todense();
        clickMat[clickMat>100]=100;  ## drop outlier 61/32760=0.00186203
        clickMat=clickMat/100.0;
        for i in xrange(len(itemIndex)):
            clickMat[:,i]*=log(float(len(userIndex))/userFreqs[i]);
        #buyMat[buyMat>16]=16;     ## drop outlier 10/4317=0.00231642
        #buyMat=buyMat/16.0;
        #UK,KC=nmf(clickMat,max_iter=5);
        #print "UK shape=",UK.shape," clickMat shape=",clickMat.shape;
        #sim_dict=build_sim_dict(buyMat);
        sim_dict=build_cos_distance(np.transpose(clickMat));
        dump(sim_dict,open("/tmp/itemsim_dict","wb"));
        #sim_dict=load(open("/tmp/itemsim_dict","rb"));
        sim_dict=[sorted(x.items(),key=lambda x:x[1],reverse=True) for x in sim_dict];
        fout=open("/tmp/itemsim_score","w");
        for i in xrange(len(userIndex)):
            if buyMat[i,:].getnnz()==0:
                continue;
            score={};
            for j in buyMat[i,:].indices:
                itemSimList=sim_dict[j];
                #print "item=",j,"simList=",itemSimList[:knn];
                for term in itemSimList[:knn]:
                    item=term[0];
                    similar=term[1];
                    score[item]=score.get(item,0)+similar;
            content=userIndex[i];
            for j in score:
                content+="\t"+itemIndex[j]+":"+str(score[j]);
            fout.write(content+"\n");
        fout.close();
        print "score file is /tmp/itemsim_score,BACKUP it!!";

