#!/bin/bash

st=`date +%s`

#---------------------------------------------------------------
#---------------------------------------------------------------
GREEN='\x1b[32m'
BLUE='\x1b[34m'
RED='\x1B[31m'
NC='\033[0m'

bold=$(tput bold)
NORMAL=$(tput sgr0)

measthrTCP () {
ssh -i ~/.ssh/awscluster.pem ubuntu@10.0.14.12	 /bin/bash << EOF
iperf3 -c 10.0.1.71 -t 100 > iperf.log
tail -3 iperf.log | head -1 > avg.log
scp -i ~/.ssh/awscluster.pem avg.log ubuntu@10.0.1.71:/home/ubuntu/benchmark/iperf.log
EOF
}

measplUDP () {
ssh -i ~/.ssh/awscluster.pem ubuntu@10.0.14.12	 /bin/bash << EOF
iperf3 -c 10.0.1.71 -u -b 1G -t 100 > iperf.log
tail -3 iperf.log | head -1 > avg.log
scp -i ~/.ssh/awscluster.pem avg.log ubuntu@10.0.1.71:/home/ubuntu/benchmark/iperf.log
EOF

}

for ((ite=0;ite<$1;ite++))
do
	log=./iperf.log

	if [ -f $log ]; then
	  echo removing TCP $log
	  rm $log
	fi
	measthrTCP
	value=`cat ./iperf.log`
	echo $value | awk '{print $7}' >> hourly.TCP.log.txt
	sleep 3
done
for ((ite=0;ite<$1;ite++))
do
	log=./iperf.log

	if [ -f $log ]; then
	  echo removing UDP $log
	  rm $log
	fi
	measplUDP
	value=`cat ./iperf.log`
	echo $value | awk '{print $12}' | sed 's/[^0-9.]//g' >> hourly.UDP.log.txt
	sleep 3
done


log=./lat.log

if [ -f $log ]; then
  echo removing $log
  rm $log
fi

ping -c 100 10.0.14.12 | awk -F '[:=]'  'NR!=1 {print $5}' >> $log

avg=$(cat $log | sed 's/[^.0-9][^.0-9]*/ /g')
echo $avg >> hourly.lat.log.txt

sleep 2

et=`date +%s`
rt=$((et-st))

mv hourly.TCP.log.txt $2TCP.txt
mv hourly.UDP.log.txt $2UDP.txt
mv hourly.lat.log.txt $2LAT.txt

echo "$rt seconds"
