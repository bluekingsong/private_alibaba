#! /usr/bin/env python
from sys import argv;
from math import exp;
from common import load_index_map;

if __name__=="__main__":
	if len(argv)!=2:
		print "usage:",argv[0],"train_data";
	else:
		trainfile=argv[1];
		userMap,t=load_index_map("data/all.user");
		itemMap,t=load_index_map("data/all.brand");
		ubMat={};
		users={};
		items={};
		for line in open(trainfile):
			paras=line[:-1].split("\t");
			if( paras[2] not in ['1'] ):
				continue;
			u=paras[0];
			i=paras[1];
			if (u not in userMap)or(i not in itemMap):
				continue;
			if u not in users:
				users[u]=set();
			users[u].add(i);
			if i not in items:
				items[i]=set();
			items[i].add(u);
			if u not in ubMat:
				ubMat[u]={};
			ubMat[u][i]=ubMat[u].get(i,0)+1;
		fout=open("/tmp/link_score","w");
		for u in users:
			score={};
			for i in users[u]:
				for v in items[i]:
					if v==u:
						continue;
					for j in users[v]:
						score[j]=score.get(j,0)+ubMat[v][j];
						#exp(-abs(ubMat[u][i]-ubMat[v][i]))*ubMat[v][j];  #TODO: improve it!
			if len(score)==0:
				continue;
			content=u;
			for i in score:
				content+="\t"+i+":"+str(score[i]);
			fout.write(content+"\n");
		fout.close();
		print "score file is /tmp/link_score,BACKUP it!!";

