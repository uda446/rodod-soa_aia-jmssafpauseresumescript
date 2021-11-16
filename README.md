# Information
This is a script to support tasks as PAUSE/RESUME/CHECK the status of
JMS and SAF queues/servers/agents.

# Prerequisites
````
1. 
Make sure that WebLogic ConfigFile and KeyFile is available on the server.
/opt/aia/config/domains/aiafp12c_domain/security/WeblogicConfigFile
/opt/aia/config/domains/aiafp12c_domain/security/WeblogicKeyFile

2. If files is not present in section 1. is not present please follow this section otherwise proceed to section 3.

2a: Start the WebLogic Scripting Tool (WLST)
cd /opt/aia/Middleware_WLS12C/oracle_common/common/bin
./wlst.sh

2b: Connect to the server AdminServer/NodeManager
wls:/offline>connect('weblogic','<PASSWORD>','t3://<HOSTNAME>:7001')

2c: Generate ConfigFile & KeyFile while connected to the AdminServer/NodeManager
wls:/aiafp12c_domain/serverConfig/>storeUserConfig('/opt/aia/config/domains/aiafp12c_domain/security/WeblogicConfigFile', '/opt/aia/config/domains/aiafp12c_domain/security/WeblogicKeyFile')

2d: Exit the WLST.
wls:/aiafp12c_domain/serverConfig/> exit()
````
# Usage of this Script
````
sh JMSSAFHandler.sh <action> <system>

Actions:
 pause: pause JMS Queue & SAF
 resume: resume JMS Queue & SAF
 check: verify status of JMS & SAF

System: (optional)
 brm
 siebel
 osm
 uim
 gesb
 kafka
 aia
 + others if any configured in conf dir
````

# 13/04/2021 - Tomasz Wiacek (aat817)
New functionalities have been added to the JMSSAFPauseResumeScript to have a possibility to pause/resume/check JMS (queues/topics/SAFs) for selected external system. For example when we will have an incident on BRM we are be able to easily pause the JMS queues and topic related to BRM only. This means that rest of other flows like from Siebel to OSM or from OSM to UIM etc. can still work. The same during OSM purging operation and so on. Thanks to this in some cases we can reduce impact on services and decrease number of backlog jms messages during long downtimes. It also gives a possibility to resume queues in more control manner system by system which might be useful in the future in case of big jms backlog.

Usage of the new script is very simillar to the previous version. To tell the script that you want do an action on the specified system only just add its name at the end of the command i.e.:
````
$ cd /opt/aia/OperationalScript/JMSSAFPauseResumeScript
$ ./JMSSAFHandler.sh pause brm
$ ./JMSSAFHandler.sh resume brm
$ ./JMSSAFHandler.sh check brm
Curently available system names: brm, siebel, osm, uim, gesb, kafka, aia
````

Configuration of each system is placed in  /opt/aia/OperationalScript/JMSSAFPauseResumeScript/conf:
brm.py  gesb.py  kafka.py  osm.py  siebel.py  uim.py  aia.py
Each configuration file contains list of associated queues, topic and SAFs. In case of new system added or destination extention they can be easily added to the configuration. 

When the system name is not specified (i.e. ./JMSSAFHandler.sh resume) the script works the same as before -  it pause or resume all JMS destinations.

The 'aia' is used to pause/resume all SOA and AIA internal queues. When everything was paused and you want to resume the queues for one system only or all systems but one by one you must rember to resume the aia (internal queues) as first. i.e.:
````
$ ./JMSSAFHandler.sh resume aia
$ ./JMSSAFHandler.sh resume brm
$ ./JMSSAFHandler.sh resume siebel
[...]
$ ./JMSSAFHandler.sh resume
````
IMPROTANT:
pausing specified system is not a persistent change, the JMS destinations will be resumed automatically after managed server restart. It is because there is no ability to pause single JMS destination at startup. It can be done on JMS Server level only which means pause consumption at startup for all JMS destinations = all systems. In case you want to have JMS destination paused persistently also after the restart (i.e. during deployment) please use the script the same way as before: 
````
./JMSSAFHandler.sh pause
./JMSSAFHandler.sh resume
````
