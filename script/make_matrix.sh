#!/bin/bash
if [ $# -ne 6 ]
then
	echo "usage:$0 train_data output_prefix [user_click_eps user_buy_eps brand_click_eps brand_buy_eps]"
	if [ $# -eq 2 ]
	then
		u_clk_eps=2;
		u_buy_eps=1;
		b_clk_eps=4;
		b_buy_eps=1;
	else
		exit 1;
	fi;
fi;
train_data=$1;
output=$2;
if [ $# -eq 6 ]
then
	u_clk_eps=$3;
	u_buy_eps=$4;
	b_clk_eps=$5;  ## click eps
	b_buy_eps=$6;
fi;
awk '{ user[$1]; cnt[$1" "$3]++;}END{ for(u in user)print u"\t"cnt[u" "0]+0"\t"cnt[u" "1]+0"\t"cnt[u" "2]+0"\t"cnt[u" "3]+0"\t"0+cnt[u" "0]+cnt[u" "1]+cnt[u" "2]+cnt[u" "3] }' $train_data > "/tmp/user.cnt";
awk '{ user[$2]; cnt[$2" "$3]++;}END{ for(u in user)print u"\t"cnt[u" "0]+0"\t"cnt[u" "1]+0"\t"cnt[u" "2]+0"\t"cnt[u" "3]+0"\t"0+cnt[u" "0]+cnt[u" "1]+cnt[u" "2]+cnt[u" "3] }' $train_data > "/tmp/brand.cnt";

awk -v u_clk_eps="${u_clk_eps}" -v u_buy_eps="${u_buy_eps}" '{ if($2<u_clk_eps||$3<u_buy_eps) next;print $1;}' "/tmp/user.cnt" |sort -n > ${output}.user;
awk -v b_clk_eps="${b_clk_eps}" -v b_buy_eps="${b_buy_eps}" '{ if($2<b_clk_eps||$3<b_buy_eps) next;print $1;}' "/tmp/brand.cnt" |sort -n > ${output}.brand;

sort -t'	' -k1n ${train_data} > "/tmp/train_data";
mv "/tmp/train_data" ${train_data};

awk -v prefix="${output}" '{
	if(FILENAME==ARGV[1]){
		brands[$1]=FNR;
	}else if(FILENAME==ARGV[2]){
		users[$1]=FNR;
	}else if(FILENAME==ARGV[3]){
		if(!($1 in users) || !($2 in brands)) next;
		if($1!=last && last!=""){
			if(length(click)>0){
				content=last;
				for(i in click) content=content"\t"i" "click[i];
				print content > prefix".clk";
			}
			if(length(buy)>0){
				content=last;
				for(i in buy) content=content"\t"i" "buy[i];
				print content > prefix".buy";
			}
			delete click;
			delete buy;
		}
		last=$1;
		if($3==0)	click[$2]++;
		else if($3==1)	buy[$2]++;
	}
}END{
	if(length(click)>0){
		content=last;
		for(i in click) content=content"\t"i" "click[i];
		print content > prefix".clk";
	}
	if(length(buy)>0){
		content=last;
		for(i in buy) content=content"\t"i" "buy[i];
		print content > prefix".buy";
	}
}' ${output}.brand ${output}.user $train_data;

wc -l ${output}*
