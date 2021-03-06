#! /usr/bin/env python
from sys import argv;

if __name__=="__main__":
	if len(argv)<4:
		print "usage: predict.py score test threshold [max_recall,default 500]";
	else:
		threshold=float(argv[3]);
		predict={};
		score_filename=argv[1];
		maxRecall=500;
		if len(argv)==5:
			maxRecall=int(argv[4]);
		for line in open(score_filename):
			items=line[:-1].split("\t");
			user=items[0];
			brands=[(x.split(":")[0],float(x.split(":")[1])) for x in items[1:]];
			brands.sort(key=lambda x:x[1],reverse=True);
			for item in brands[:maxRecall]:
				if item[1]>=threshold:
					if user not in predict:
						predict[user]=set();
					predict[user].add(item[0]);
				else:
					break;
			#print brands[:10];
		buy={};
		for line in open(argv[2]):
			items=line[:-1].split("\t");
			u=items[0];
			if items[2]=="1":
				if u not in buy:
					buy[u]=set();
				buy[u].add(items[1]);
		#prediction
		pbrands=0;
		hitcnt=0;
		for u in predict:
			pbrands+=len(predict[u]);
			if u not in buy:
				continue;
			for item in predict[u]:
				if item in buy[u]:
					hitcnt+=1;
		precision=float(hitcnt)/pbrands;
		#recall
		bbrands=0;
		hitcnt=0;
		for u in buy:
			bbrands+=len(buy[u]);
			if u not in predict:
				continue;
			for item in buy[u]:
				if item in predict[u]:
					hitcnt+=1;
		print "ground truths=",bbrands,"recall hits=",hitcnt;
		recall=float(hitcnt)/bbrands;
		f1=2*precision*recall/(precision+recall);
		f=open("temp/predict.txt","w");
		for u in predict:
			items=list(predict[u]);
			content=u+"\t"+",".join(items);
			f.write(content+"\n");
		f.close();
		print "p=%4.2f,r=%4.2f,f1=%4.2f"%(precision*100,recall*100,f1*100);
		print "predict file output is temp/predict.txt.\n";


