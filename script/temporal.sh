#!/bin/bash
awk 'BEGIN{min=2;max=0}{ for(i=3;i<=NF;i+=2) {$i=log($i+1); s1+=$i; s2+=$i*$i; ++n;if($i>max)max=$i; if($i<min)min=$i;}}END{ u=s1/n; d=s2/n-u*u; sd=sqrt(d/(n-1)); print "u="u" d="d" sd="sd" n="n" min="min" max="max;}' mat
