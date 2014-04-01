#!/bin/bash
if [ $# -lt 1 ]
then
    echo "usage:$0 train_data"
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
awk '{
    if(FILENAME==ARGV[1]){
        users[$1];
    }else if(FILENAME==ARGV[2]){
        items[$1];
    }else{
        if(!($1 in users) || !($2 in items)) next;
        if($3==0){
            uclk[$1]++;
            bclk[$2]++;
        }else{
            ubuy[$1]++;
            bbuy[$1]++;
        }
    }
}END{
    clk_sum=0;
    buy_sum=0;
    for(i in users){
        clk_sum+=uclk[i];
        buy_sum+=ubuy[i];
    }
    global_ave=buy_sum/clk_sum;
    ucontent="";
    for(i in users){
        if(uclk[i]+ubuy[i]<8) users[i]=gloabal_ave;
        if(uclk[i]==0) users[i]=0;
        users[i]=(ubuy[i]+0.01)/(uclk[i]+0.01);
        ucontent=ucontent==""? i"\t"users[i] : ucontent"\t"i"\t"users[i];
    }
    bcontent="";
    for(i in items){
        if(bclk[i]+bbuy[i]<8) items[i]=global_ave;
        if(bclk[i]==0) items[i]=0;
        items[i]=(bbuy[i]+0.01)/(bclk[i]+0.01);
        bcontent=bcontent==""? i"\t"items[i] : bcontent"\t"i"\t"items[i];
    }
    print global_ave > "/tmp/ave_para";
    print ucontent > "/tmp/ave_para";
    print bcontent > "/tmp/ave_para";
    print ucontent;
    print bcontent;
}' $userfile $itemfile $train_data | awk -v clk_weight="$clk_weight" '{
if(FILENAME==ARGV[1]){
    if(FNR==1){
        for(i=1;i<=NF;i+=2) users[$i]=$(i+1);
    }else{
        for(i=1;i<=NF;i+=2) items[$i]=$(i+1);
    }
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
        }
        last=$1;
        if($3>=1){
            score[$2]++;
        }else{
            score[$2]+=0.5*users[$1]+0.5*items[$2];
        }
    }
}END{
    #print "maxium buy brands:"maxBuy;
}' - $train_data  #> "/tmp/score_history";
echo "score file is /tmp/history_score";
#head /tmp/history_score

