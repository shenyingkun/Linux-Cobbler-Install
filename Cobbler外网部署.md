# Cobbler 部署安装Centos 6.9（例）

## 一．检查系统环境 

    [root@cobbler ~]# getenforce 检查selinux

    [root@cobbler ~]# /etc/init.d/iptables status 检查防火墙

挂载iso镜像制作yum源

    echo "mount -o loop CentOS-6.9-x86_64-bin-DVD1.iso /mnt/CentOS/" >>/etc/rc.local 

    echo "mount -o loop CentOS-6.9-x86_64-bin-DVD1.iso /mnt/cdrom/" >>/etc/rc.local

安装epel源

    [root@cobbler ~]# wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo

## 二．安装cobbler

    [root@cobbler ~]# yum install cobbler cobbler-web pykickstart httpd dhcp tftp-server -y

    [root@cobbler ~]# rpm -ql cobbler 

    [root@cobbler cobbler]# /etc/init.d/httpd restart    #启动apache服务     

    [root@cobbler cobbler]# /etc/init.d/cobblerd restart    #启动cobbler服务

错误1:

    Starting httpd: httpd: apr_sockaddr_info_get() failed for cobbler

    httpd: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName

#遇见报错需要修改apache的配置文件，添加一行

    [root@cobbler cobbler]# vim /etc/httpd/conf/httpd.conf  

    ServerName localhost:80

## 三．修改程序参数

检查cobbler安装环境

    [root@cobbler cobbler]#cobbler check

修改cobbler环境

(1)修改/etc/cobbler/settings文件中的server参数

    [root@cobbler cobbler]#sed -i 's/server: 127.0.0.1/server: 192.168.64.131/' /etc/cobbler/settings

(1)修改/etc/cobbler/settings文件中的next_server参数 

    sed -i 's/next_server: 127.0.0.1/next_server: 192.168.64.131/' /etc/cobbler/settings

    [root@cobbler cobbler]#grep "server: 192.168.64.131" settings

(1)修改/etc/xinetd.d/tftp文件中的disable参数修改为 disable = no

    [root@cobbler cobbler]#sed -i 's/disable.*= yes/disable = no/g' /etc/xinetd.d/tftp

(1)执行 cobbler get-loaders 命令

    [root@cobbler cobbler]#cobbler get-loaders

(1)修改rsync配置文件；

    [root@cobbler cobbler]#sed -i s/"disable.*= yes"/"disable = no"/g /etc/xinetd.d/rsync 

(1)安装debmirror 

    [root@cobbler cobbler]#yum install -y  debmirror

错误1:

    3 : comment out 'dists' on /etc/debmirror.conf for proper debian support4 : comment out 'arches' on /etc/debmirror.conf for proper debian support

    [root@cobbler cobbler]# vim /etc/debmirror.conf

    28 #@dists="sid"; 30 #@arches="i386";
 
(1)生成密码来取代默认的密码

    [root@cobbler cobbler]# openssl passwd -1 -salt 'admin@administrator' 'thinker'

    [root@cobbler cobbler]#

    sed -i s/'default_password_crypted:.*'/'default_password_crypted: "$1$renjunji$G7LpR5255qFguHrw7E0KP\/"'/g /etc/cobbler/settings

    [root@cobbler cobbler]# grep -n default_pass /etc/cobbler/settings

(1)安装cman fence-agents

    [root@cobbler cobbler]# yum install -y cman ence-agents

(1)其他一些没有提示报错的小修改

    [root@cobbler cobbler]# sed -i 's/manage_dhcp: 0/manage_dhcp: 1/g' /etc/cobbler/settings

    [root@cobbler cobbler]# sed -i 's/pxe_just_once: 0/pxe_just_once: 1/' /etc/cobbler/settings

## 四．配置DHCP

    [root@linux-node1 ~]# vim /etc/cobbler/dhcp.template

    subnet 192.168.64.0 netmask 255.255.255.0 { 
 
    option domain-name-servers 223.5.5.5; 

    option routers 192.168.64.1;     

    range dynamic-bootp 192.168.64.100 192.168.64.250;

    option subnet-mask 255.255.255.0;

    next-server 192.168.64.131;

    filename "/data/sys/kickstart/ks.cfg";

    next-server 192.168.64.131;

    filename "pxelinux.0";

    }

    [root@cobbler cobbler]# cobbler sync

## 五．开机启动

    [root@cobbler cobbler]# echo "/etc/init.d/httpd restart" >>/etc/rc.local 

    [root@cobbler cobbler]# echo "/etc/init.d/xinetd restart" >>/etc/rc.local     
 
    [root@cobbler cobbler]# echo "/etc/init.d/cobblerd restart" >>/etc/rc.local   
    
    [root@cobbler cobbler]# echo "/etc/init.d/dhcpd restart" >>/etc/rc.local 

## 六．导入镜像

    [root@cobbler ~]# cobbler import --path=/mnt/ --name=CentOS-6.9-x86_64 --arch=x86_64

7.查看镜像列表

    [root@cobbler ~]# cobbler distro list

    [root@cobbler ~]# cobbler sync

    [root@cobbler kickstarts]# cobbler profile report --name=CentOS-6.9-x86_64 

Centos 默认关联文件sample_end.ks ，修改/var/lib/cobbler/kickstarts/sample_end.ks

# Cobbler 部署安装Ubuntu14（例）

## 一．导入镜像

    [root@cobbler ~]# cobbler import --path=/mnt/ --name=Ubuntu14 --arch=x86_64

    echo " mount -o loop lubuntu-14.04-alternate-amd64.iso /mnt/cdrom1/" >>/etc/rc.local

## 二．查看镜像列表

    [root@cobbler ~]# cobbler distro list

    [root@cobbler ~]# cobbler sync

    [root@cobbler kickstarts]# cobbler profile report --name= Ubuntu14-x86_64

Ubuntu默认关联文件sample.seed，修改文件/var/lib/cobbler/kickstarts/sample.seed

# Cobbler 部署安装Esxi5.1（例）

## 一．导入镜像

    [root@cobbler ~]# cobbler import --path=/mnt/ --name=Esxi5.1 --arch=x86_64

    echo " mount -o loop lubuntu-14.04-alternate-amd64.iso /mnt/cdrom1/" >>/etc/rc.local

## 二．查看镜像列表

    [root@cobbler ~]# cobbler distro list

    [root@cobbler ~]# cobbler sync

    [root@cobbler kickstarts]# cobbler profile report --name= Ubuntu14-x86_64

Esxi5默认关联文件sample_esxi5.ks，修改文件/var/lib/cobbler/kickstarts/sample_esxi5.ks

# Cobbler 部署安装红帽6.4（例）

## 一．导入镜像

    [root@cobbler ~]# cobbler import --path=/mnt/ --name=Esxi5.1 --arch=x86_64

    echo " mount -o loop Red\ Hat\ Enterprise\ 6.5\ x86_64.iso /mnt/cdrom3/" >>/etc/rc.local

## 二．查看镜像列表

    [root@cobbler ~]# cobbler distro list

    [root@cobbler ~]# cobbler sync

    [root@cobbler kickstarts]# cobbler profile report --name= Ubuntu14-x86_64

红帽默认关联文件sample_end.ks ，修改/var/lib/cobbler/kickstarts/sample_end.ks
