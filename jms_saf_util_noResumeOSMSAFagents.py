from java.lang import System
import javax
from javax import management
from javax.management import MBeanException
from javax.management import RuntimeMBeanException
import javax.management.MBeanException
from java.lang import UnsupportedOperationException
import traceback

ConfigFile='/opt/aia/config/domains/aiafp12c_domain/security/WeblogicConfigFile'
KeyFile='/opt/aia/config/domains/aiafp12c_domain/security/WeblogicKeyFile'

operation = sys.argv[1]
t3url = sys.argv[2]

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

def setJMSPauseConsumptionAtStartup():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------setJMSPauseConsumptionAtStartup--------------------------'
        print '-------------------------------------------------------------------------'
        print 'Obtaining serverConfig()'
        serverConfig();
        deployments = cmo.getDeployments();
        print 'Obtained Deployments'
        if (len(deployments) > 0):
            for deployment in deployments:
                deploymentName = deployment.getName();
                if deploymentName.find("AIAJMSServer") != -1:
                    print 'Found the JMS Server destination. Hence, setting the value of Pause Consumption on Start up'
                    print 'JMS Server Name : ' + deploymentName
                    edit()
                    startEdit()
                    cd('/Deployments/'+deploymentName)
                    cmo.setConsumptionPausedAtStartup('true');
                    save()
                    activate(block="true")
                    print 'Value of ConsumptionPausedAtStartup is set to true'
        print ''
        print '--------------------Value of ConsumptionPausedAtStartup is set to true for all JMS Servers------------'
        print ''
    except:
        print 'ERROR in executing setJMSPauseConsumptionAtStartup'
        dumpStack();
        traceback.print_exc()
        undo('true','y')
        stopExecution('Exception while editing the config MBean')
        sys.exit(1)

def unsetJMSPauseConsumptionAtStartup():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------unsetJMSPauseConsumptionAtStartup--------------------------'
        print '-------------------------------------------------------------------------'
        print 'Obtaining serverConfig()'
        serverConfig();
        deployments = cmo.getDeployments();
        print 'Obtained Deployments'
        if (len(deployments) > 0):
            for deployment in deployments:
                deploymentName = deployment.getName();
                if deploymentName.find("AIAJMSServer") != -1:
                    print 'Found the JMS Server destination. Hence, un-setting the value of Pause Consumption on Start up'
                    print 'JMS Server Name : ' + deploymentName
                    edit()
                    startEdit()
                    cd('/Deployments/'+deploymentName)
                    cmo.setConsumptionPausedAtStartup('false');
                    save()
                    activate(block="true")
                    print 'Value of ConsumptionPausedAtStartup is set to false'
        print ''
        print '--------------------Value of ConsumptionPausedAtStartup is set to false for all JMS Servers----------------'
        print ''
    except:
        print 'ERROR in executing unsetJMSPauseConsumptionAtStartup'
        dumpStack();
        traceback.print_exc()
        undo('true','y')
        stopExecution('Exception while editing the config MBean')
        sys.exit(1)

def setSAFForwardingPausedAtStartup():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------setSAFForwardingPausedAtStartup--------------------------'
        print '-------------------------------------------------------------------------'
        print 'Obtaining serverConfig()'
        serverConfig();
        safAgents = cmo.getSAFAgents();
        print 'Obtained SAFAgents'
        if (len(safAgents) > 0):
            for safAgent in safAgents:
                safAgentName = safAgent.getName();
                print 'safAgent Name : ' + safAgentName
                if safAgentName.find("SAFAgent") != -1:
                    print 'Found the SAF destination. Hence, setting the value of Pause Forwarding on Start up'
                    edit()
                    startEdit()
                    cd('/SAFAgents/'+safAgentName)
                    cmo.setForwardingPausedAtStartup(true);
                    save()
                    activate(block="true")
                    print 'Value of ForwardingPausedAtStartup is set to true'
        print ''
        print '--------------------Value of ForwardingPausedAtStartup is set to true for all SAF Agents------------'
        print ''
    except:
        print 'ERROR setting value setSAFForwardingPausedAtStartup as True'
        dumpStack();
        traceback.print_exc()
        undo('true','y')
        stopExecution('Exception while editing the config MBean')
        sys.exit(1)

def unsetSAFForwardingPausedAtStartup():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------unsetSAFForwardingPausedAtStartup--------------------------'
        print '-------------------------------------------------------------------------'
        print 'Obtaining serverConfig()'
        serverConfig();
        safAgents = cmo.getSAFAgents();
        print 'Obtained SAFAgents'
        if (len(safAgents) > 0):
            for safAgent in safAgents:
                safAgentName = safAgent.getName();
                print 'safAgent Name : ' + safAgentName
                if safAgentName.find("SAFAgent") != -1:
                    print 'Found the SAF destination. Hence, un-setting the value of Pause Forwarding on Start up'
                    edit()
                    startEdit()
                    cd('/SAFAgents/'+safAgentName)
                    cmo.setForwardingPausedAtStartup(false);
                    save()
                    activate(block="true")
                    print 'Value of ForwardingPausedAtStartup is set to false'
        print ''
        print '--------------------Value of ForwardingPausedAtStartup is set to false for all SAF Agents------------'
        print ''
    except:
        print 'ERROR setting value unsetSAFForwardingPausedAtStartup as False'
        dumpStack();
        traceback.print_exc()
        undo('true','y')
        stopExecution('Exception while editing the config MBean')
        sys.exit(1)

def pauseJMSDestinations():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------PAUSE JMS SAF DESTINTION--------------------------'
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
                                        destinationName = destination.getName()
                                        destination.pauseConsumption()
                                        print 'File JMS '+destinationName+' : PAUSE OK'
        print ''
        print '--------------------JMS SAF destination paused-------------'
        print ''
    except:
        print 'ERROR Pause JMS SAF'
        sys.exit(1)

def resumeJMSDestinations():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------RESUME JMS SAF----------------------------'
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
                                        destinationName = destination.getName()
                                        destination.resumeConsumption()
                                        print 'File JMS '+destinationName+' : RESUME OK'

        print ''
        print '--------------------RESUME JMS SAF OK-----------------'
        print ''
    except:
        print 'ERROR RESUME JMS SAF'
        sys.exit(1)


def checkIfJMSDestinationsActive():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------Check JMS ------------------------------'
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
                                        destinationName = destination.getName()
                                        if destination.isConsumptionPaused() :
                                                print 'File JMS '+destinationName+' PAUSED'
                                        if destination.isConsumptionPaused() == false :
                                                print 'File JMS '+destinationName+' RESUMED'
        print ''
        print '--------------------JMS VERIFIED---------------------'
        print ''
    except:
        print 'ERROR JMS'
        sys.exit(1)

def pauseSAFAgents():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------pauseSAFAgents-------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        safRuntime = server.getSAFRuntime();
                        safAgents = safRuntime.getAgents();
                        for safAgent in safAgents:
                                safAgentName = safAgent.getName()
                                safAgent.pauseForwarding()
                                print 'SAFAgent '+safAgentName+' : pauseSAFAgents OK'

        print ''
        print '--------------------pauseSAFAgents Complete----------------'
        print ''
    except:
        print 'ERROR pauseSAFAgents'
        sys.exit(1)

def resumeSAFAgents():
    try:
        print '-------------------------------------------------------------------------'
        print '-------------------- resumeSAFAgents---------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        safRuntime = server.getSAFRuntime();
                        safAgents = safRuntime.getAgents();
                        for safAgent in safAgents:
                                safAgentName = safAgent.getName()
                                safAgent.resumeForwarding()
                                print 'SAFAgent '+safAgentName+' :  resumeSAFAgents OK'

        print ''
        print '-------------------- resumeSAFAgents-----------------'
        print ''
    except:
        print 'ERROR resumeSAFAgents'
        sys.exit(1)

def checkIfSAFAgentsActive():
    try:
        print '-------------------------------------------------------------------------'
        print '--------------------VERIFIFCATION SAF Agents-------------------------'
        print '-------------------------------------------------------------------------'
        print ''

        servers = domainRuntimeService.getServerRuntimes();
        if (len(servers) > 0):
                for server in servers:
                        safRuntime = server.getSAFRuntime();
                        safAgents = safRuntime.getAgents();
                        for safAgent in safAgents:
                                safAgentName = safAgent.getName()
                                if safAgent.isPausedForForwarding() :
                                        print 'SAFAgent '+safAgentName+' PAUSED'
                                if safAgent.isPausedForForwarding() == false :
                                        print 'SAFAgent '+safAgentName+' OPERATIONAL'

        print ''
        print '--------------------All SAFAgents are checked--------------------------'
        print ''
    except:
        print 'ERROR SAFAgents'
        sys.exit(1)

def usage():
        print '<<<<<<<<<<<<< Usage :                                                          >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< jms_saf_util.py <operation> <destination> <secureFile location>  >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< operation : <pause/resume/check>                                 >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< destination : <JMS/SAF>                                          >>>>>>>>>>>>'
        print '<<<<<<<<<<<<< Exemple: jms_saf_util.py pause JMS  >>>>>>>>>>>>'
        exit()

try:
        hideDumpStack("false")

        if operation == "pause":
            validConnect()
            setJMSPauseConsumptionAtStartup()
            setSAFForwardingPausedAtStartup()
            pauseJMSDestinations()
            pauseSAFAgents()
            exit()

        elif operation == "resume":
             validConnect()
             unsetJMSPauseConsumptionAtStartup()
             unsetSAFForwardingPausedAtStartup()
             resumeJMSDestinations()
             #resumeSAFAgents()
             exit()

        elif operation == "check":
            validConnect()
            checkIfJMSDestinationsActive()
            checkIfSAFAgentsActive()
            exit()

        else:
            print 'Incorrect Operation'
            usage()
            sys.exit(1)
except:
    print 'Verify the logic of the script'
