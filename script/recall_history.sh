#!/bin/bash
if [ $# -ne 1 ]
then
	echo "usage:$0 train_data"
	exit 1;
fi;

train_data=$1;
records=`wc -l $train_data|cut -d' ' -f1`;
awk -v recordCnt="$records" '{
	if(FILENAME==ARGV[1] && NR<=recordCnt){
		if($3==1) buyCnt[$2]++;
		if(buyCnt[$2]>maxBuy) maxBuy=buyCnt[$2];
	}else{
		if($1!=last && last!=""){
			content=last;
			recalls=0;
			for(i in score){
				#print "i="i" buy cnt="buyCnt[i];
				if(buyCnt[i]<5) continue;
				recalls++;
				content=content"\t"i":"score[i]+(month[i]-1)*1000;
			}
			if(recalls>0)
				print content > "/tmp/score_history";
			delete score;
			delete month;
			delete last_month;
		}
		last=$1;
		if($3==1){
			score[$2]++;
			if(last_month[$3]!=$4){
				month[$2]++;
				last_month[$2]=$4;
			}
		}
	}
}END{
	print "maxium buy brands:"maxBuy;
}' $train_data $train_data  #> "/tmp/score_history";
echo "score file is /tmp/score_history";
head /tmp/score_history

