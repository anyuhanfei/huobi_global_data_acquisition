#!/bin/bash

screen -S k -X quit
screen -S data -X quit

sleep 1s

screen -Sdm k
screen -x -S k -p 0 -X stuff "cd /root/huobi_global_data_acquisition-master/\n"
screen -x -S k -p 0 -X stuff "python3 kline_index.py\n"

screen -Sdm data
screen -x -S data -p 0 -X stuff "cd /root/huobi_global_data_acquisition-master/\n"
screen -x -S data -p 0 -X stuff "python3 data_index.py\n"
