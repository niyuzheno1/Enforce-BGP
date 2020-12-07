#!/bin/bash
# Copyright Zach (Yuzhe) Ni 2020, GPL License 
time=(2017 00 00 0)
while [ $((time[0]++)) -lt 2018 ]; do
    year=$(printf "%04d" $((time[0])))
    #echo $year
    while [ $((time[1]++)) -lt 12 ]; do
        month=$(printf "%02d" $((time[1])))
        while [ $((time[2]++)) -lt 31 ]; do
            day=$(printf "%02d" $((time[2])))
            timestamp=0
            while [ $timestamp -le 2345 ]
            do
                tmpx=$(printf "%04d" $timestamp)
                url=$(printf "http://routeviews.org/bgpdata/%s.%s/UPDATES/updates.%s%s%s.%s.bz2" $year $month $year $month $day $tmpx)
                wget $url
                ((timestamp += 5))
            done
        done
        time[2]=0
        #echo $month
    done
    time[1]=0
done 
