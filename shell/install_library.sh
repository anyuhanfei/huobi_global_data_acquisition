#!/bin/bash
#安装python第三方库
libs=(requests pymysql DBUtils redis)

pip3 install --upgrade pip
for i in ${libs[@]};
	do
		echo " ---------- 正在安装 ---------------> $i "
		pip3 install $i;
		while [ $? -ne 0 ];
			do
				echo " ---------- 安装失败，重新安装 ---------------> $i "
				pip3 install $i;
			done
    done
