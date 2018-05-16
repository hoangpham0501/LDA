INSTALL HADOOP MULTI NODE CLUSTER
SLAVE

** Environment
# UBUNTU 14.04
# HADOOP 2.6.5
# JAVA JDK 7
# SSH
# RSYNC

* Java Development Kit:
# Update the source list
$ sudo apt-get update

# The OpenJDK project is the default version of Java that is provided from a supported Ubuntu repository.
$ sudo apt-get install default-jdk
$ java -version

# Install rsync for sharing hadoop source with rest all machines
$ sudo apt-get install rsync
$ sudo reboot

* Adding a dedicated Hadoop user
$ sudo addgroup hadoop
$ sudo adduser --ingroup hadoop hduser

* Installing SSH
$ sudo apt-get install ssh
$ which ssh
/usr/bin/ssh
$ which sshd
/usr/sbin/sshd

* Create and Setup SSH Certificates
$ su hduser
$ ssh-keygen -t rsa -P ""
$ cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys

* Disabling IPv6
$ sudo gedit /etc/sysctl.conf
Adding following line of codes at end of the file:
# disable ipv6
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1

We can also disable IPv6 only for Hadoop
$ sudo gedit conf/hadoop-env.sh
export HADOOP_OPTS = -Djava.net.preferIPv4Stack=true

*** Installation Steps
$ wget http://mirrors.sonic.net/apache/hadoop/common/hadoop-2.6.5/hadoop-2.6.5.tar.gz
$ tar xvzf hadoop-2.6.5.tar.gz
$ sudo mv hadoop-2.6.5 /usr/local/hadoop 
$ sudo chown -R hduser:hadoop hadoop

## Create Hadoop temp directories for Datanode at Slave machine
sudo mkdir -p /usr/local/hadoop_tmp/hdfs/datanode
## Again assign ownership of this Hadoop temp folder to Hadoop user
sudo chown hduser:hadoop -R /usr/local/hadoop_tmp/


**Setup Configuration Files
1. ~/.bashrc
$ sudo gedit ~/.bashrc
Append the following to the end of file
#HADOOP VARIABLES START
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export HADOOP_INSTALL=/usr/local/hadoop
export PATH=$PATH:$HADOOP_INSTALL/bin
export PATH=$PATH:$HADOOP_INSTALL/sbin
export HADOOP_MAPRED_HOME=$HADOOP_INSTALL
export HADOOP_COMMON_HOME=$HADOOP_INSTALL
export HADOOP_HDFS_HOME=$HADOOP_INSTALL
export YARN_HOME=$HADOOP_INSTALL
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_INSTALL/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_INSTALL/lib"
#HADOOP VARIABLES END

2. ./hadoop-env.sh
We need to set JAVA_HOME by modifying /usr/local/hadoop/etc/hadoop/hadoop-env.sh file
$ sudo gedit /usr/local/hadoop/etc/hadoop/hadoop-env.sh
Adding this command
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64

3. /usr/local/hadoop/etc/hadoop/core-site.xml:
sudo gedit /usr/local/hadoop/etc/hadoop/core-site.xml
Adding the configuration

<configuration>
	<property>
		<name>fs.default.name</name>
		<value>hdfs://master:9000</value>
	</property>
</configuration>

4. /usr/local/hadoop/etc/hadoop/mapred-site.xml
=> By default, the /usr/local/hadoop/etc/hadoop/ folder contains the /usr/local/hadoop/etc/hadoop/mapred-site.xml.template file which has to be renamed/copied with the name mapred-site.xml:

$ cp /usr/local/hadoop/etc/hadoop/mapred-site.xml.template /usr/local/hadoop/etc/hadoop/mapred-site.xml
$ sudo gedit /usr/local/hadoop/etc/hadoop/mapred-site.xml
Adding the configuration
<configuration>
	<property>
  		<name>mapreduce.framework.name</name>
      		<value>yarn</value>
	</property>
</configuration>

5. /usr/local/hadoop/etc/hadoop/hdfs-site.xml
$ sudo gedit /usr/local/hadoop/etc/hadoop/hdfs-site.xml
<configuration>
	<property>
		<name>dfs.replication</name>
		<value>2</value>
	</property>
	<property>
		<name>dfs.permissions</name>
		<value>false</value>
	</property>
	<property>
		<name>dfs.namenode.name.dir</name>
		<value>hdfs:///usr/local/hadoop_tmp/hdfs/namenode</value>
	</property>
	<property>
		<name>dfs.datanode.data.dir</name>
		<value>hdfs:///usr/local/hadoop_store/hdfs/datanode</value>
	</property>
</configuration>

6. /usr/local/hadoop/etc/hadoop/yarn-site.xml
$ sudo gedit /usr/local/hadoop/etc/hadoop/yarn-site.xml
<configuration>
	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
	<property>
		<name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
		<value>org.apache.hadoop.mapred.ShuffleHandler</value>
	</property>
	<property>
		<name>yarn.resourcemanager.resource-tracker.address</name>
		<value>master:8031</value>
	</property>
	<property>
		<name>yarn.resourcemanager.scheduler.address</name>
		<value>master:8030</value>
	</property>
	<property>
		<name>yarn.resourcemanager.address</name>
		<value>master:8032</value>
	</property>
</configuration>

** Editing the neccessary files
$ sudo gedit /etc/hosts
Adding following hostname and their IP
Ex:
192.168.0.1	master
192.168.0.2	slave1
192.168.0.3	slave2