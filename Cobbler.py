#!/usr/bin/env python
#coding:utf-8
import time
import sys
import os
import shutil
import io
import commands
from optparse import OptionParser

print ("[INFO] ============================================================")
# 自动挂载光盘ISO镜像 ##
time.sleep(2)
path = '/mnt/cdrom'
def handleVersionFile():

    path = '/mnt/cdrom'
    str  = '/dev/sr0 /mnt/cdrom' #--------------------要查询的字符串
    str1 = 'mount /dev/cdrom /mnt/cdrom' #------------挂载语句
    str2 = 'umount /dev/cdrom' #----------------------卸载语句
    str3 = 'cat /proc/mounts' #-----------------------查询语句
    if  os.path.exists(path):# 判断目录是否存在
        time.sleep(2)
        if not os.listdir(path):
            print("[INFO] 挂载目录可以直接挂载")
            time.sleep(2)
            val = commands.getoutput(str1)
            file = commands.getoutput(str3)
            if str in file:
                 print ("[INFO] 挂载成功")
            else:
                 print ("[ERROR] 挂载失败，程序退出")
                 os._exit(0)

        else:
            print("[INFO] 挂载目录存在内容，卸载后重新挂载")
            time.sleep(2)
            val = commands.getoutput(str2)
            if not os.listdir(path):
                val = commands.getoutput(str1)
                file = commands.getoutput(str3)
                if str in file:
                     print ("[INFO] 挂载成功")
                else:
                     print ("[ERROR] 挂载失败，程序退出")
                     os._exit(0)
            else:
                print("[INFO] 挂载目录存在无法卸载内容，必须手工检查目录")
                time.sleep(2)
                allfile=[]
                def getallfile(path):
                    allfilelist=os.listdir(path)
                    for file in allfilelist:
                        filepath=os.path.join(path,file)
                        #判断是不是文件夹
                        if os.path.isdir(filepath):
                            getallfile(filepath)
                        allfile.append(filepath)
                    return allfile

                if __name__ == '__main__':

                   allfiles=getallfile(path)
                   for item in allfiles:
                       print ("[ERROR]"+"挂载目录存在 "+item)
                os._exit(0)
    else: # 没有就创建
        print ("[INFO] 挂载目录不存在，自动新建目录")
        os.mkdir(path)
        time.sleep(2)
        val = commands.getoutput(str1)
        file = commands.getoutput(str3)
        if str in file:
             print ("[INFO] 挂载成功")
        else:
             print ("[ERROR] 挂载失败，程序退出")
             os._exit(0)

if __name__ == "__main__":
    handleVersionFile()
time.sleep(2)
print ("[INFO] ------------------------------------------------------------")
# 备份yum源文件 ##
time.sleep(2)

os.chdir('/etc/yum.repos.d') #--------------------切换目录
def handleVersionFile():

    srcVersionFilePath = os.getcwd()+os.sep+"CentOS-Base.repo"
    dstVersionFilePath = os.getcwd()+os.sep+"CentOS-Base.repo.bak"

    srcProjectFilePath = os.getcwd()+os.sep+"CentOS-Base.repo"
    dstProjectFilePath = os.getcwd()+os.sep+"CentOS-Base.repo.bak"
    if not os.path.isfile(srcProjectFilePath):
        print("[WARR] CentOS-Base  源文件不存在，程序退出")
        #os._exit(0)
    else:
        time.sleep(2)
        if not os.path.isfile(dstProjectFilePath):
            print ('[INFO] CentOS-Base 开始拷贝')
            if os.path.exists(srcVersionFilePath):
                shutil.copyfile(srcVersionFilePath,dstVersionFilePath)
            if os.path.exists(srcProjectFilePath):
                shutil.copyfile(srcProjectFilePath,dstProjectFilePath)
                time.sleep(2)
            print ('[INFO] CentOS-Base  备份结束')
            os.remove(srcProjectFilePath)
            if os.path.isfile(srcProjectFilePath):
                os._exit(0)
        else:
            print("[WARR] CentOS-Base 备份文件已存在,程序退出")
            os._exit(0)
if __name__ == "__main__":
    handleVersionFile()

# 备份yum源文件##

def handleVersionFile():

    srcVersionFilePath = os.getcwd()+os.sep+"CentOS-Media.repo"
    dstVersionFilePath = os.getcwd()+os.sep+"CentOS-Media.repo.bak"

    srcProjectFilePath = os.getcwd()+os.sep+"CentOS-Media.repo"
    dstProjectFilePath = os.getcwd()+os.sep+"CentOS-Media.repo.bak"
    if not os.path.isfile(srcProjectFilePath):
        print("[WARR] CentOS-Media 源文件不存在,程序退出")
        #os._exit(0)
    else:
        time.sleep(2)
        if not os.path.isfile(dstProjectFilePath):
            print ('[INFO] CentOS-Media 文件开始拷贝')
            if os.path.exists(srcVersionFilePath):
                shutil.copyfile(srcVersionFilePath,dstVersionFilePath)
            if os.path.exists(srcProjectFilePath):
                shutil.copyfile(srcProjectFilePath,dstProjectFilePath)
                time.sleep(2)
            print ('[INFO] CentOS-Media 文件备份结束')
        else:
            print("[WARR] CentOS-Media 备份文件已存在，程序退出")
            #os._exit(0)
if __name__ == "__main__":
    handleVersionFile()
time.sleep(2)

# 修改yum源文件 ##

def handleVersionFile():
 f = io.open('/etc/yum.repos.d/CentOS-Media.repo.bak','r',encoding='utf-8')
 f_new = io.open('/etc/yum.repos.d/CentOS-Media.repo','w',encoding='utf-8')

 for line in f:
    # 进行判断
    if "enabled=0" in line:
        line = line.replace('enabled=0','enabled=1')
        time.sleep(5)
    if "baseurl=file:///media/CentOS/" in line:
        line = line.replace('baseurl=file:///media/CentOS/','baseurl=file:///mnt/cdrom/')
    # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
    f_new.write(line)

 f.close()
 f_new.close()
 print ('[INFO] CentOS-Media 文件修改成功')


if __name__ == "__main__":
    handleVersionFile()

print ("[INFO] ------------------------------------------------------------")
# 关闭防护墙和SELINUX ##

time.sleep(2)

def handleVersionFile():
 val = commands.getoutput("service iptables stop")
 val = commands.getoutput("chkconfig iptables off")
 a = commands.getoutput('/etc/init.d/iptables status')
 b = commands.getoutput('setenforce 0')
 c = commands.getoutput('getenforce')
    # 进行判断
 if "iptables: Firewall is not running." in a:
        print("[INFO] IPTABLES 已关闭")
        time.sleep(2)
 else:
        print("[ERROR] IPTABLES 关闭失败，程序退出")
        time.sleep(2)
        os._exit(0)
    # 进行判断
 if "Disabled" in c:
        print("[INFO] SELINUX 已关闭")
        time.sleep(2)
 else:
        print("[ERROR] SELINUX 关闭失败，程序退出")
        time.sleep(2)
        os._exit(0)

if __name__ == "__main__":
    handleVersionFile()

time.sleep(2)
# 安装rpm依赖包 ##
print ("[INFO] ------------------------------------------------------------")
time.sleep(2)

os.chdir('/cobbler/') #--------------------切换目录
def handleVersionFile():
 print("[INFO] 开始安装依赖包，请勿停止程序")
 val = commands.getoutput('rpm -ivh perl-LockFile-Simple-0.207-2.el6.noarch.rpm')
 val = commands.getoutput(" yum install -y dhcp python-netaddr tftp-server mod_wsgi createrepo python-cheetah python-simplejson PyYAML syslinux genisoimage mod_ssl patch perl-LockFile-Simple perl-Compress-Zlib perl-Digest-SHA perl-libwww-perl cman ence-agents")

 a ='dhcp perl-LockFile-Simple python-netaddr tftp-server mod_wsgi createrepo python-cheetah python-simplejson PyYAML syslinux genisoimage mod_ssl patch perl-LockFile-Simple perl-Compress-Zlib perl-Digest-SHA perl-libwww-perl cman ence-agents'
 for package in a.split():
    # 进行判断
   str = 'rpm -qa|grep'+ ' ' +package
   a = commands.getoutput(str)
   if package in a:
        print("[INFO]"+" "+"RPM包 "+package+" "+"安装成功")
   else:
        print("[WARR]"+" "+"RPM包 "+package+" "+"安装失败")

 print("[INFO] RPM包 依赖包安装完毕，部分失败项需要手动检查安装")
 print ("[INFO] ------------------------------------------------------")
 val = commands.getoutput("rpm -ivh cobbler-2.6.11-1.el6.x86_64.rpm")
 val = commands.getoutput("rpm -ivh Django14-1.4.20-1.el6.noarch.rpm")
 val = commands.getoutput("rpm -ivh Django14-1.4.20-1.el6.src.rpm")
 val = commands.getoutput("rpm -ivh Django14-doc-1.4.20-1.el6.noarch.rpm")
 val = commands.getoutput("rpm -ivh cobbler-web-2.6.11-1.el6.noarch.rpm")
 a ='cobbler-2.6.11 cobbler-web-2.6.11'
 for package in a.split():
    # 进行判断
   str = 'rpm -qa|grep'+ ' ' +package
   a = commands.getoutput(str)
   if package in a:
        print("[INFO]"+" "+package+" "+"安装成功")
   else:
        print("[WARR]"+" "+package+" "+"安装失败")
        os._exit(0)

 time.sleep(2)
 str = 'rpm -ql cobbler'
 if os.system(str) !=0:
     print("Without the command")
 else:
     time.sleep(3)
     print("[INFO] Cobbler 主程序安装成功")
 time.sleep(2)

if __name__ == "__main__":
    handleVersionFile()

def handleVersionFile():
 print ("[INFO] ------------------------------------------------------------")
 time.sleep(2)
 val = commands.getoutput("cat /etc/httpd/conf/httpd.conf")
 str = "ServerName localhost:80"
    # 进行判断
 if str in val:
        print("[INFO] HTTP 配置已修改，重启服务")
        time.sleep(2)
        val = os.system('/etc/init.d/httpd restart')
        val = os.system('/etc/init.d/cobblerd restart')

 else:
        fp = open('/etc/httpd/conf/httpd.conf')
        lines = []
        for line in fp:
            lines.append(line)
        fp.close()

        val1 = commands.getoutput("sed -n '/#ServerName www.example.com:80/=' /etc/httpd/conf/httpd.conf")
        f = int(val1)
        lines.insert(f, str+'\n') # 在插入
        s = ''.join(lines)
        fp = open('/etc/httpd/conf/httpd.conf', 'w')
        fp.write(s)
        fp.close()
        val = commands.getoutput("cat /etc/httpd/conf/httpd.conf")
        if str in val:
            print("[INFO] HTTP 配置修改成功,重启服务")
            time.sleep(2)
            val = os.system('/etc/init.d/httpd restart')
            val = os.system('/etc/init.d/cobblerd restart')
        else:
            print("[WARR] HTTP 配置修改失败")


if __name__ == "__main__":
    handleVersionFile()

print ("[INFO] ------------------------------------------------------------")
time.sleep(2)
def handleVersionFile():
 val2 = commands.getoutput('cat /etc/cobbler/settings')
 str = 'ifconfig eth0|grep \'inet addr:\'|cut -d: -f2|cut -d " " -f1'
 hostname = commands.getoutput(str)
 if 'server: 127.0.0.1' in val2:
     val1 = commands.getoutput('sed -i \'s/server: 127.0.0.1/server: %s/\' /etc/cobbler/settings' %(hostname))
     val = commands.getoutput('grep "server: %s" /etc/cobbler/settings' %(hostname))
     if hostname in val:
         print("[INFO] SERVER 配置成功")
         time.sleep(2)
     else:
         os._exit(0)
 else:
     val = commands.getoutput('grep "server: %s" /etc/cobbler/settings' %(hostname))
     if hostname in val:
         print("[INFO] SERVER 已配置")
         time.sleep(2)
     else:
         os._exit(0)

if __name__ == "__main__":
    handleVersionFile()

def handleVersionFile():
 val_new = commands.getoutput('grep "disable" /etc/xinetd.d/tftp')
 if 'disable = no' in val_new:
     print("[INFO] TFTP 已配置,可以跳过")
     time.sleep(2)
 else:
     val = commands.getoutput('sed -i \'s/disable.*= yes/disable = no/g\' /etc/xinetd.d/tftp')
     val_new = commands.getoutput('grep "disable" /etc/xinetd.d/tftp')
     if 'no' in val_new:
         print("[INFO] TFTP 配置成功")
         time.sleep(2)
     else:
         print("[ERROR] TFTP 配置失败")
         os._exit(0)


if __name__ == "__main__":
    handleVersionFile()

def handleVersionFile():
 val_new = commands.getoutput('grep "disable" /etc/xinetd.d/rsync')
 if 'no' in val_new:
     print("[INFO] RSYNC 已配置,可以跳过")
     time.sleep(2)
 else:
     val = commands.getoutput('sed -i \'s/disable.*= yes/disable = no/g\' /etc/xinetd.d/rsync')
     val_new = commands.getoutput('grep "disable" /etc/xinetd.d/rsync')
     if 'disable = no' in val_new:
         print("[INFO] RSYNC 配置成功")
         time.sleep(2)
     else:
         print("[ERROR] RSYNC 配置失败")
         os._exit(0)


if __name__ == "__main__":
    handleVersionFile()





print ("[INFO] ------------------------------------------------------------")

def handleVersionFile():
    path  = '/cobbler/load1/'
    path1 = '/var/lib/cobbler/loaders/'
    str  = 'cp /cobbler/load1/* /var/lib/cobbler/loaders/'

    if  os.path.exists(path):# 判断目录是否存在
        if not os.listdir(path):
            os.exit(0)
        else:
            if not os.listdir(path1):
                val = commands.getoutput(str)
                if not os.listdir(path1):
                    print("[ERROR] LOAD 文件拷贝失败，程序退出")
                    os._exit(0)
                else:
                    print("[INFO] LOAD 文件拷贝完成")
                    time.sleep(3)
            else:
                val = commands.getoutput('rm -rf /var/lib/cobbler/loaders/*')
                val = commands.getoutput(str)
                if not os.listdir(path1):
                    print("[ERROR] LOAD 文件拷贝失败，程序退出")
                    os._exit(0)
                else:
                    print("[INFO] LOAD 文件重新拷贝完成")
                    time.sleep(3)

    else:
        os.exit(0)


if __name__ == "__main__":
    handleVersionFile()

time.sleep(2)
os.chdir('/cobbler/') #切换目录
def handleVersionFile():

    val1 = commands.getoutput('rpm -ivh debmirror-2.14-2.el6.noarch.rpm')
    val2 = commands.getoutput('rpm -qa|grep debmirror')
    if 'debmirror' in val2:
        print("[INFO] Debmirror 安装成功")
        time.sleep(3)
    else:
        print("[WARR] Debmirror 安装失败")
        os._exit(0)
if __name__ == "__main__":
    handleVersionFile()

print ("[INFO] ------------------------------------------------------------")
time.sleep(2)
def handleVersionFile():

    val1 = commands.getoutput('openssl passwd -1 -salt \'admin@administrator\' \'thinker\'')
    str1 = val1.replace('/','\/')
    val = commands.getoutput('sed -i \'s/default_password_crypted:.*\'/\'default_password_crypted: \\"%s\\" /\' /etc/cobbler/settings' %(str1))
    val2 = commands.getoutput('grep -n default_pass /etc/cobbler/settings')
    if val1 in val2:
        print("[INFO] 系统密码设置成功")
        time.sleep(2)
        val = commands.getoutput('cat /etc/cobbler/settings')
        if 'manage_dhcp: 1' in val:
            if 'pxe_just_once: 0' in val:
                print("[INFO] DHCP 文件设置成功")
                time.sleep(3)
            else:
                val = commands.getoutput('sed -i \'s/pxe_just_once: 0/pxe_just_once: 1/\' /etc/cobbler/settings')
                print("[INFO] DHCP 文件设置成功")
                time.sleep(3)
        else:
            val = commands.getoutput('sed -i \'s/manage_dhcp: 0/manage_dhcp: 1/g\' /etc/cobbler/settings')
            if 'pxe_just_once: 0' in val:
                print("[INFO] DHCP 文件设置成功")
                time.sleep(3)
            else:
                val = commands.getoutput('sed -i \'s/pxe_just_once: 0/pxe_just_once: 1/\' /etc/cobbler/settings')
                print("[INFO] DHCP 文件设置成功")
                time.sleep(3)
    else:
        os._exit(0)

if __name__ == "__main__":
    handleVersionFile()

def handleVersionFile():
   str = 'ifconfig eth0|grep \'inet addr:\'|cut -d: -f2|cut -d " " -f1'
   hostname = commands.getoutput(str)
   str1 = 'subnet 192.168.190.0 netmask 255.255.255.0 {'
   str2 = 'option domain-name-servers 223.5.5.5;'
   str3 = 'option routers 192.168.190.1;'
   str4 = 'range dynamic-bootp 192.168.190.100 192.168.190.250;'
   str5 = 'option subnet-mask 255.255.255.0;'
   str6 = 'next-server %s;'%(hostname)
   str7 = 'filename "/data/sys/kickstart/ks.cfg";'
   str8 = 'next-server %s;'%(hostname)
   str9 = 'filename "pxelinux.0";'
   str10 = '}'

   list = [str1,str2,str3,str4,str5,str6,str7,str8,str9,str10]
   #sep = ','
   #fl=open('/etc/cobbler/dhcp.template', 'w')
   #fl.write('\n'.join(list))
   #fl.close()

   val = commands.getoutput("cat /etc/cobbler/dhcp.template")
   #str = "AlertScriptsPath=/etc/zabbix/alertscripts"
    # 进行判断
   if str7 in val:
        print("[INFO] DHCP 配置文件已修改，可以跳过")
        time.sleep(2)
   else:
        fp = open('/etc/cobbler/dhcp.template')
        lines = []
        for line in fp:
            lines.append(line)
        fp.close()

        val1 = commands.getoutput("sed -n '/#for dhcp_tag in $dhcp_tags.keys():/=' /etc/cobbler/dhcp.template")
        f = int(val1)-1
        str = '\n'.join(list)
        lines.insert(f, str+'\n') # 在插入
        s = ''.join(lines)
        fp = open('/etc/cobbler/dhcp.template', 'w')
        fp.write(s)
        fp.close()
        print("[INFO] DHCP 配置文件修改成功")
        time.sleep(2)

if __name__ == "__main__":
    handleVersionFile()

print ("[INFO] ------------------------------------------------------------")
time.sleep(2)

def handleVersionFile():

  c = commands.getoutput('cat /etc/rc.local')
  if "cobblerd" in c:
      print ("[INFO] 配置文件 cobblerd 已存在需要配置的内容，可以跳过")
      val = os.system('/etc/init.d/cobblerd restart')
      time.sleep(2)
  else:
      val = os.system('echo "/etc/init.d/cobblerd restart" >>/etc/rc.local')
      val = os.system('/etc/init.d/cobblerd restart')
      print ("[INFO] 配置文件 cobblerd 成功")
      time.sleep(2)
  if "httpd" in c:
      print ("[INFO] 配置文件 httpd 已存在需要配置的内容，可以跳过")
      val = os.system('/etc/init.d/httpd restart')
      time.sleep(2)
  else:
      val = os.system('echo "/etc/init.d/httpd restart" >>/etc/rc.local')
      val = os.system('/etc/init.d/httpd restart')
      print ("[INFO] 配置文件 httpd 成功")
      time.sleep(2)
  if "xinetd" in c:
      print ("[INFO] 配置文件 xinetd 已存在需要配置的内容，可以跳过")
      val = os.system('/etc/init.d/xinetd restart')
      time.sleep(2)
  else:
      val = os.system('echo "/etc/init.d/xinetd restart" >>/etc/rc.local')
      val = os.system('/etc/init.d/xinetd restart')
      print ("[INFO] 配置文件 xinetd 成功")
      time.sleep(2)
  if "dhcpd" in c:
      print ("[INFO] 配置文件 dhcpd 已存在需要配置的内容，可以跳过")
      ##val = os.system('/etc/init.d/xinetd restart')
      time.sleep(2)
  else:
      val = os.system('echo "/etc/init.d/xinetd restart" >>/etc/rc.local')
      ##val = os.system('/etc/init.d/xinetd restart')
      print ("[INFO] 配置文件 dhcpd 成功")
      time.sleep(2)


if __name__ == "__main__":
    handleVersionFile()

print ("[INFO] ------------------------------------------------------------")
time.sleep(2)
def handleVersionFile():
  print ("[INFO] 开始导入系统镜像文件，请勿停止程序")
  val = commands.getoutput('cobbler import --path=/mnt/cdrom --name=CentOS-6.9-x86_64 --arch=x86_64')
  if 'TASK COMPLETE' in val:
      print("[INFO] 导入系统镜像成功")
      time.sleep(2)
      val = os.system('cobbler sync')
      time.sleep(2)
      val = os.system('cobbler distro list')
      time.sleep(2)
      val = os.system('cobbler profile report --name=CentOS-6.9-x86_64')
  else:
      print("[ERROR] 导入系统镜像失败")
      os._exit(0)

if __name__ == "__main__":
    handleVersionFile()
