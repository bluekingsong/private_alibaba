#! /usr/bin/env python
from sys import argv;
from math import log;

if __name__=="__main__":
	if len(argv)!=2:
		print "usage: convert2lbm.py input";
	else:
		filename=argv[1];
		output=filename+".lbm";
		fout=open(output,"w");
		indexMap={};
		brands=[];
		for line in open(filename):
			items=line[:-1].split("\t");
			for item in items[1:]:
				brand=item.split(" ")[0];
				if brand not in indexMap:
					brands.append(int(brand));
					indexMap[brand]=0;
#		print "len of indexMap",len(indexMap);
#		print "len of brands",len(brands);
		brands.sort();
		for i in xrange(len(brands)):
			indexMap[str(brands[i])]=i+1;
#		print "len of indexMap",len(indexMap);
		cnt=0;
		for line in open(filename):
			cnt+=1;
			items=line[:-1].split("\t");
			content=str(cnt); #items[0];
			brands=[];
			for item in items[1:]:
				paras=item.split(" ");
				brands.append((indexMap[paras[0]],paras[1]));
			brands.sort(key=lambda x:x[0])
			for brand in brands:
				content=content+" "+str(brand[0])+":"+brand[1];
			fout.write(content+"\n");
		fout.close();

