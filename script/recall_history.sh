#!/bin/bash
if [ $# -lt 1 ]
then
	echo "usage:$0 train_data [click_weight,defalut 0]"
	exit 1;
fi;
userfile="data/all.user";
itemfile="data/all.brand";
if [ ! -f $userfile ] || [ ! -f $itemfile ]
then
	echo $userfile" or "$itemfile" don't exist.";
	exit 1;
fi;
train_data=$1;
clk_weight=0;
if [ $# -eq 2 ]
then
	clk_weight=$2;
fi;
awk -v clk_weight="$clk_weight" '{
	if(FILENAME==ARGV[1]){
		users[$1];
	}else if(FILENAME==ARGV[2]){
		items[$1];
	}else{
		if($1!=last && last!=""){
			content=last;
			recalls=0;
			for(i in score){
				recalls++;
				content=content"\t"i":"score[i];
			}
			if(recalls>0)
				print content > "/tmp/history_score";
			delete score;
			#delete month;
			#delete last_month;
		}
		last=$1;
		if($3>=1){
			score[$2]++;
#			if(last_month[$3]!=$4){
#				month[$2]++;
#				last_month[$2]=$4;
#			}
		}else if(clk_weight>0){
			score[$2]+=clk_weight;
		}
	}
}END{
	#print "maxium buy brands:"maxBuy;
}' $userfile $itemfile $train_data  #> "/tmp/score_history";
echo "score file is /tmp/history_score";
#head /tmp/history_score

