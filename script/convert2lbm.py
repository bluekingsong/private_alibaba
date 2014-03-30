#! /usr/bin/env python
from sys import argv;
from math import log;
from common import load_index_map;

if __name__=="__main__":
	if len(argv)!=2:
		print "usage: convert2lbm.py input[say,data/mat.clk, the correspoinding indecies are data/mat.user and data/mat.brand";
	else:
		filename=argv[1];
		prefix=filename.split(".")[0];
		output=filename+".lbm";
		fout=open(output,"w");
		userMap,userIndex=load_index_map(prefix+".user");
		itemMap,itemIndex=load_index_map(prefix+".brand");
		cnt=0;
		all_data=[];
		for line in open(filename):
			cnt+=1;
			items=line[:-1].split("\t");  # user"\t"item1 cnt1"\t"...
			brands=[];
			for item in items[1:]:
				paras=item.split(" ");
				brands.append((itemMap[paras[0]],paras[1]));
			brands.sort(key=lambda x:x[0]);
			all_data.append([userMap[items[0]],brands]);
		all_data.sort(key=lambda x:x[0]);
		for terms in all_data:
			content=str(terms[0]);
			brands=terms[1];
			for brand in brands:
				content=content+" "+str(brand[0])+":"+brand[1];
			fout.write(content+"\n");
		fout.close();

