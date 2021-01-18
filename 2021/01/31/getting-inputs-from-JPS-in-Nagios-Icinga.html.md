---
author: Muhammad Najmi Ahmad Zabidi 
title: 'Using JPS with NRPE'
tags: linux, monitoring, nrpe, nagios, icinga 
gh_issue_number: 1655
---


### Problem statement
We encountered an issue when executing the NRPE from Icinga's head server. Usually the NRPE-related call should not be an issue to be executed on the target server as they will be declared in the sudoers file 


### Test



# sudo -s -u nagios /usr/local/lib/nagios/plugins/check_lucene_indexing_deprecated 
/usr/local/lib/nagios/plugins/check_lucene_indexing_deprecated: line 11: /var/log/jetty9/jvm.log: Permission denied
/usr/local/lib/nagios/plugins/check_lucene_indexing_deprecated: line 13: kill: (7541) - Operation not permitted

root@herbie.do.ridgetopresearch.com:~# sudo -s -u nagios jps -l
29112 sun.tools.jps.Jps
root@herbie.do.ridgetopresearch.com:~# jps -l
7541 /usr/share/jetty9/start.jar
29131 sun.tools.jps.Jps


So we create a cronjob, which should be executed for every 10 minutes

*/10 * * * * /root/bin/fetch_lucene_pid.sh

The cron script contains the following details:
 

PID_TARGET=/var/run/nrpe-lucene.pid
THREADS_TARGET=/var/run/nrpe-lucene-thread.txt

/usr/bin/jps -l | grep "start.jar" | cut -d' ' -f1 1>$PID_TARGET 2>/dev/null

#ln -s /var/run/nrpe-lucene.pid /var/run/nrpe-lucene-dup.pid

PID=$(cat $PID_TARGET)

re='^[0-9]+$'

if  [[ -z $PID ]]  || ! [[ $PID =~ $re ]]  ; then
exit 0
fi

THREADS=$(/usr/bin/jstack $PID | grep -A 2 "ProjectIndexer\|ConsultantIndexer" | grep -c "java.lang.Thread.State: WAITING (parking)")

echo $THREADS > $THREADS_TARGET


So instead of running the `jps` command directly as nagios, we let the system run (as root) to run jps and dump the result onto a file. NRPE-based script later will read the output and feed the result to the dashboard. 



