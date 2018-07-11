# Cobbler 部署安装Centos 6.9（例）
## 一．检查系统环境
    [root@cobbler ~]# getenforce # 检查SELINUX
    [root@cobbler ~]# setenforce 0 # 关闭SELINUX 
    [root@cobbler ~]# /etc/init.d/iptables stop # 关闭防火墙
    [root@cobbler ~]# chkconfig iptables off # 设置防火墙不开机启动
    [root@cobbler ~]# echo "mount -o loop CentOS-6.9-x86_64-bin-DVD1.iso /mnt/cdrom/" >>/etc/rc.local # 挂载iso镜像制作yum源，配置源
## 二．安装cobbler
    [root@cobbler ~]# yum install -y mod_wsgi createrepo python-cheetah python-simplejson PyYAML syslinux genisoimage mod_ssl ## 安装依赖服务
    [root@cobbler ~]# rpm –ivh cobbler-2.6.11-1.el6.x86_64.rpm ## 安装cobbler主程序，注意先后顺序
    [root@cobbler ~]# rpm -ivh Django14-1.4.20-1.el6.noarch.rpm ## 依赖包
    [root@cobbler ~]# rpm -ivh Django14-1.4.20-1.el6.src.rpm ## 依赖包
    [root@cobbler ~]# rpm -ivh Django14-doc-1.4.20-1.el6.noarch.rpm ## 依赖包
    [root@cobbler ~]# rpm –ivh cobbler-web-2.6.11-1.el6.noarch.rpm
    [root@cobbler ~]# rpm -ql cobbler
    [root@cobbler ~]# /etc/init.d/httpd restart    #启动apache服务
    错误1:
    Starting httpd: httpd: apr_sockaddr_info_get() failed for cobbler
    httpd: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName

    [root@cobbler ~]# vim /etc/httpd/conf/httpd.conf  #遇见报错需要修改apache的配置文件，添加一行
    ServerName localhost:80
    [root@cobbler ~]# /etc/init.d/cobblerd restart    #启动cobbler服务
## 三．修改程序参数

    [root@cobbler ~]# cobbler check ## 检查cobbler安装环境
    (1)修改cobbler参数
    [root@cobbler ~]# sed -i 's/server: 127.0.0.1/server: 192.168.64.132/' /etc/cobbler/settings
    [root@cobbler ~]# sed -i 's/next_server: 127.0.0.1/next_server: 192.168.64.132/' /etc/cobbler/settings
    [root@cobbler ~]# sed -i 's/disable.*= yes/disable = no/g' /etc/xinetd.d/tftp
    [root@cobbler ~]# grep "server: 192.168.64.132" /etc/cobbler/settings
    (2)下载get-loaders文件导入/var/lib/cobbler/loaders/路径下
    (3)修改rsync配置文件；
    [root@cobbler ~]# sed -i s/"disable.*= yes"/"disable = no"/g /etc/xinetd.d/rsync
    (1)下载debmirror安装
    [root@cobbler ~]# rpm -ivh perl-LockFile-Simple-0.207-2.el6.noarch.rpm ## 依赖包
    [root@cobbler ~]# rpm –ivh debmirror-2.14-2.el6.noarch.rpm
    (1)生成密码来取代默认的密码
    [root@cobbler ~]# openssl passwd -1 -salt 'admin@administrator' 'thinker'
    [root@cobbler ~]# sed -i s/'default_password_crypted:.*'/'default_password_crypted: "$1$renjunji$G7LpR5255qFguHrw7E0KP\/"'/g   /etc/cobbler/settings
    [root@cobbler ~]# grep -n default_pass /etc/cobbler/settings
    (1)安装cman fence-agents
    [root@cobbler cobbler]# yum install -y cman ence-agents
    (1)其他一些没有提示报错的小修改，用cobbler管理DHCP，修改242行manage_dhcp: 0
    [root@cobbler ~]# sed -i 's/manage_dhcp: 0/manage_dhcp: 1/g' /etc/cobbler/settings
    [root@cobbler ~]# sed -i 's/pxe_just_once: 0/pxe_just_once: 1/' /etc/cobbler/settings
## 四．配置DHCP
    [root@cobbler ~]# vim /etc/cobbler/dhcp.template
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
## 五．开机启动
    [root@cobbler ~]# echo "/etc/init.d/httpd restart" >>/etc/rc.local
    [root@cobbler ~]# echo "/etc/init.d/xinetd restart" >>/etc/rc.local
    [root@cobbler ~]# echo "/etc/init.d/cobblerd restart" >>/etc/rc.local
    [root@cobbler ~]# echo "/etc/init.d/dhcpd restart" >>/etc/rc.local
## 六．导入镜像
    [root@cobbler ~]# cobbler import --path=/mnt/ --name=CentOS-6.9-x86_64 --arch=x86_64
## 七．查看镜像列表
    [root@cobbler ~]# cobbler distro list
    [root@cobbler ~]# cobbler sync
    [root@cobbler ~]# cobbler profile report --name=CentOS-6.9-x86_64
## 八．重启服务
    [root@cobbler ~]# /etc/init.d/httpd restart
    [root@cobbler ~]# /etc/init.d/cobblerd restart
    [root@cobbler ~]# /etc/init.d/xinetd start
