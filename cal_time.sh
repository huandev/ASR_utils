#!/bin/bash

tic=`date +%s.%N`
sleep 2
toc=`date +%s.%N`
time_run=$((#10$toc - #10$tic))
echo "$time_run s"
