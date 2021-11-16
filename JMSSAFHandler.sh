#!/bin/bash
#############################################################################################
# File Description: Script to invoke the JMSSAFPauseResumeScript                            #
# File Name: JMSSAFHandler.sh                                                               #
# Author: Ahmad, Imran - uda446 date: 2020-05-04                                            #
# Version History:                                                                          #
# v01 - 2020-04-15 - Initial Script creation                                                #
# v01 - 2020-05-08 - added error handling, script initially final                           #
# v02 - 2021-04-02 - Wiacek, Tomasz: added function updateJMSQueuesSAFAgentSelectively,     #
#                    modified execution() - added SYSTEM param                              # 
#############################################################################################

#Setting ACTION variable (blank)
ACTION=$1
SYSTEM=$2

#Exit on error & unset variables
set -eu

#Config-variables
URL=t3://$(hostname):7001
PROG=JMSSAFHandler
DATE=`date '+%Y%m%d'`
HOUR=`date '+%H%M%S'`
export CONFIG_JVM_ARGS="-Djava.security.egd=file:/dev/./urandom -Dwlst.offline.log=disable"

#Path-Variables
WORKDIR=/opt/aia/OperationalScript/JMSSAFPauseResumeScript
WLST_HOME=/opt/aia/Middleware_WLS12C/oracle_common/common/bin
LOG_FOLDER=/opt/aia/OperationalScript/JMSSAFPauseResumeScript/log
LOG_FILE=${LOG_FOLDER}/${PROG}_${DATE}_${HOUR}.log

####################################################
################# Usage function ###################
####################################################
usage() {
  echo "#Description: "
  echo "- JMSSAFHandler.sh - Pause/Resume/Check queue consumtion"
  echo "#Syntax: sh JMSSAFHandler.sh <ACTION> <SYSTEM>"
  echo "#Actions: "
  echo " pause: To pause JMS Queues & SAF"
  echo " resume: To resume JMS Queues & SAF"
  echo " check: To check status of the JMS Queues & SAF"
  echo ""
  echo "#Example:"
  echo " sh JMSSAFHandler.sh resume"
  echo " sh JMSSAFHandler.sh resume brm"
  echo ""
  echo "If SYSTEM not provided then script will do the action for all JMS and SAF"
  echo "SYSTEM can be configured in conf dir."
  exit 1

} #end of usage

####################################################
######## updateJMSQueuesSAFAgent function ##########
####################################################
updateJMSQueuesSAFAgent()
{
  ${WLST_HOME}/wlst.sh ${WORKDIR}/jms_saf_util.py $ACTION ${URL}
  exitcode=$?
  if [[ $exitcode -ne 0 ]]; then
    echo "Error: exitcode $exitcode from wlst.sh"
    exit $exitcode
  fi

} #end of updateJMSQueuesSAFAgent

###############################################################
######## updateJMSQueuesSAFAgentSelectively function ##########
###############################################################
updateJMSQueuesSAFAgentSelectively()
{
  ${WLST_HOME}/wlst.sh ${WORKDIR}/jms_saf_util_selectively.py $ACTION ${URL} $SYSTEM
  exitcode=$?
  if [[ $exitcode -ne 0 ]]; then
    echo "Error: exitcode $exitcode from wlst.sh"
    exit $exitcode
  fi

} #end of updateJMSQueuesSAFAgentSelectively

####################################################
################ Execution function ################
####################################################
execution()
{
  if [[ -z "$SYSTEM" ]]; then
    case "$ACTION" in
      "pause") updateJMSQueuesSAFAgent
        ;;
      "resume") updateJMSQueuesSAFAgent
        ;;
      "check") updateJMSQueuesSAFAgent
        ;;
      *) usage
        ;;
     esac
  else
    echo "System selected: $SYSTEM"
    case "$ACTION" in
      "pause") updateJMSQueuesSAFAgentSelectively
        ;;
      "resume") updateJMSQueuesSAFAgentSelectively
        ;;
      "check") updateJMSQueuesSAFAgentSelectively
        ;;
      *) usage
        ;;
    esac
  fi
}

execution | tee $LOG_FILE 2>&1
