from java.lang import System
import javax
from javax import management
from javax.management import MBeanException
from javax.management import RuntimeMBeanException
import javax.management.MBeanException
from java.lang import UnsupportedOperationException
import traceback
from java.io import File
from java.io import FileInputStream
from java.util import Properties
import conf 


ConfigFile='/opt/aia/config/domains/aiafp12c_domain/security/WeblogicConfigFile'
KeyFile='/opt/aia/config/domains/aiafp12c_domain/security/WeblogicKeyFile'
Domain='/opt/aia/config/domains/aiafp12c_domain'

operation = sys.argv[1]
t3url = sys.argv[2]
system = sys.argv[3]

def getQueues(system):
    try:
        q = eval("conf.%s.queues" % (system))
        return q
    except:
        return None

def getTopics(system):
    try:
        t = eval("conf.%s.topics" % (system))
        return t
    except:
        return None
    
def getSAFs(system):
    try:
        s = eval("conf.%s.safs" % (system))
        return s
    except:
        return None

def validConnect():
    try:
        print 'Connecting to Admin server ...'
        connect(userConfigFile=ConfigFile,userKeyFile=KeyFile,url=t3url)
        print 'Connection to Admin server OK'
        print ''
    except:
        print 'Connection to Admin server Error'
        print 'Possible causes of error :'
        print '   - Verify if Admin server running'
        print '   - Verify the presence of securefiles '+ConfigFile+' and '+KeyFile+''
        sys.exit(1)


def pauseJMSDestinations(confDestList):
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------PAUSE JMS DESTINATION--------------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        jmsRuntime = server.getJMSRuntime();
                        jmsServers = jmsRuntime.getJMSServers();
                        for jmsServer in jmsServers:
                                jmsServerName = jmsServer.getName()
                                destinations = jmsServer.getDestinations();
                                for destination in destinations:
                                        destName = destination.getName()
                                        if (destName.split('@')[-1] in confDestList or
                                            destName.split('!')[-1] in confDestList):
                                                destination.pauseConsumption()
                                                print 'File JMS '+destName+' : PAUSE OK'
        print ''
        print '--------------------JMS destination paused-------------------------------'
        print ''
    except:
        print 'ERROR Pause JMS'
        sys.exit(1)

def resumeJMSDestinations(confDestList):
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------RESUME JMS-------------------------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        jmsRuntime = server.getJMSRuntime();
                        jmsServers = jmsRuntime.getJMSServers();
                        for jmsServer in jmsServers:
                                jmsServerName = jmsServer.getName()
                                destinations = jmsServer.getDestinations();
                                for destination in destinations:
                                        destName = destination.getName()
                                        if (destName.split('@')[-1] in confDestList or
                                            destName.split('!')[-1] in confDestList):
                                                destination.resumeConsumption()
                                                print 'File JMS '+destName+' : RESUME OK'

        print ''
        print '--------------------RESUME JMS OK-----------------------------------------'
        print ''
    except:
        print 'ERROR RESUME JMS'
        sys.exit(1)


def checkIfJMSDestinationsActive(confDestList):
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------Check JMS -------------------------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        jmsRuntime = server.getJMSRuntime();
                        jmsServers = jmsRuntime.getJMSServers();
                        for jmsServer in jmsServers:
                                jmsServerName = jmsServer.getName()
                                destinations = jmsServer.getDestinations();
                                for destination in destinations:
                                        destName = destination.getName()
                                        if (destName.split('@')[-1] in confDestList or
                                            destName.split('!')[-1] in confDestList):
                                                if destination.isConsumptionPaused() :
                                                        print 'File JMS '+destName+' PAUSED'
                                                if destination.isConsumptionPaused() == false :
                                                        print 'File JMS '+destName+' RESUMED'
        print ''
        print '--------------------JMS VERIFIED------------------------------------------'
        print ''
    except:
        print 'ERROR JMS'
        sys.exit(1)

def pauseSAFAgents(confDestList):
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------pauseSAFAgents---------------------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        safRuntime = server.getSAFRuntime();
                        safAgents = safRuntime.getAgents();
                        for safAgent in safAgents:
                                safAgentName = safAgent.getName()
                                if safAgentName.split('@')[0] in confDestList:
                                    safAgent.pauseForwarding()
                                    print 'SAFAgent '+safAgentName+' : pauseSAFAgents OK'

        print ''
        print '--------------------pauseSAFAgents Complete----------------'
        print ''
    except:
        print 'ERROR pauseSAFAgents'
        sys.exit(1)

def resumeSAFAgents(confDestList):
    try:
        print '-------------------------------------------------------------------------'
        print '-------------------- resumeSAFAgents-------------------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        safRuntime = server.getSAFRuntime();
                        safAgents = safRuntime.getAgents();
                        for safAgent in safAgents:
                                safAgentName = safAgent.getName()
                                if safAgentName.split('@')[0] in confDestList:
                                    safAgent.resumeForwarding()
                                    print 'SAFAgent '+safAgentName+' :  resumeSAFAgents OK'

        print ''
        print '-------------------- resumeSAFAgents--------------------------------------'
        print ''
    except:
        print 'ERROR resumeSAFAgents'
        sys.exit(1)

def checkIfSAFAgentsActive(confDestList):
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------VERIFIFCATION SAF Agents-----------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        safRuntime = server.getSAFRuntime();
                        safAgents = safRuntime.getAgents();
                        for safAgent in safAgents:
                                safAgentName = safAgent.getName()
                                if safAgentName.split('@')[0] in confDestList:
                                    if safAgent.isPausedForForwarding() :
                                            print 'SAFAgent '+safAgentName+' PAUSED'
                                    if safAgent.isPausedForForwarding() == false :
                                            print 'SAFAgent '+safAgentName+' OPERATIONAL'

        print ''
        print '--------------------All SAFAgents are checked-----------------------------'
        print ''
    except:
        print 'ERROR SAFAgents'
        sys.exit(1)


def usage():
        print '<<<<<<<<<<<<< Usage :                                                       >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< jms_saf_util_selectively.py <operation> <url> <system>        >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< operation : <pause/resume/check>                              >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< url : <t3://$(hostname):7001>                                 >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< Exemple:                                                      >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< jms_saf_util_selectively.py pause t3://localhost:7001 brm     >>>>>>>>>>>>'
        exit()


def pause(system):
    queues = getQueues(system)
    print "Configured Queues: %s" % (str(queues))
    if queues:
        pauseJMSDestinations(queues)
    
    topics = getTopics(system)
    print "Configured Topics: %s" % (str(topics))
    if topics:
        pauseJMSDestinations(topics)
    
    safs = getSAFs(system)
    print "Configured SAFs: %s" % (str(safs))
    if safs:
        pauseSAFAgents(safs)
      
   
def myresume(system):
    #name 'resume' is restricted and can't be used in WLST thats why we use 'myresume'
    queues = getQueues(system)
    print "Configured Queues: %s" % (str(queues))
    if queues:
        resumeJMSDestinations(queues)
    
    topics = getTopics(system)
    print "Configured Topics: %s" % (str(topics))
    if topics:
        resumeJMSDestinations(topics)
    
    safs = getSAFs(system)
    print "Configured SAFs: %s" % (str(safs))
    if safs:
        resumeSAFAgents(safs)

def check(system):
    queues = getQueues(system)
    print "Configured Queues: %s" % (str(queues))
    if queues:
        checkIfJMSDestinationsActive(queues)
    
    topics = getTopics(system)
    print "Configured Topics: %s" % (str(topics))
    if topics:
        checkIfJMSDestinationsActive(topics)
    
    safs = getSAFs(system)
    print "Configured SAFs: %s" % (str(safs))
    if safs:
        checkIfSAFAgentsActive(safs)

try:
        hideDumpStack("false")

        if operation == "pause":
            validConnect()
            pause(system)
            exit()

        elif operation == "resume":
            validConnect()
            myresume(system)
            exit()

        elif operation == "check":
            validConnect()
            check(system)
            exit()

        else:
            print 'Incorrect Operation'
            usage()
            sys.exit(1)
except Exception, e:
    print 'Verify the logic of the script'
    print e
    
