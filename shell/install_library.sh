#!/bin/bash
# 安装python,screen
# 判断服务器类型, 当前可判断类型: Ubuntu/Debian, RHEL/CentOS/Fedora, OpenSUSE, ArchLinux
is_debian = `apt-get | wc -l | head -n 2 | tail -n 1`
if $is_debian > 1
then
	apt-get install python3
	apt-get install screen
fi
is_contos = `yum | wc -l | head -n 2 | tail -n 1`
if $is_contos > 1
then
	yum install python3
	yum install screen
fi
is_opensuse = `zypper | wc -l | head -n 2 | tail -n 1`
if $is_opensuse > 1
then
	zypper install python3
	zypper install screen
fi
is_archLinux = `pacman | wc -l | head -n 2 | tail -n 1`
if $is_archLinux > 1
then
	pacman install python3
	pacman install screen
fi

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
