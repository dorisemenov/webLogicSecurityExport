## ======================================================================================================
## OBIEEUserRoleextract.py - v 2018.06.19
## ======================================================================================================

## Usage:
## 1) set weblogic scripting environment
## 2) call weblogic scripting tool (wlst.sh/.cmd)

## example on Linux (using env var for convenience):
## export WLBIN=/APP1/middleware/oracle_common/common/bin/
## $WLBIN/setWlstEnv.sh
## $WLBIN/wlst.sh {script path}/OBIEEUserRoleExtract.py

## WLST supports only Python 2


# -------------------------------------------------------------------------------------------------------
# Export Users and container groups/roles
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
# Reads files:
#   OBIEEcredentials.txt
#
# Writes many files
# -------------------------------------------------------------------------------------------------------

from weblogic.management.security.authentication import UserReaderMBean
from weblogic.management.security.authentication import GroupReaderMBean

import sys
import glob, os
import socket
import sys, thread, time, threading
from java.lang import String
import errno
from datetime import datetime
#import wl
from sys import platform as _platform



# ==============================================================================================
#
#                               Begin Library Definitions
#
# ==============================================================================================


# Get Password from user without displaying to console
# -----------------------------------------------------------------------------
def getPass(stream=None):
  #System = os.system()
  console = System.console()
  if console is None:
    global p_stopMasking
    if not stream:
      stream = sys.stderr
    try:
      p_stopMasking = 0
      threading.Thread(target=_doMasking,args=(stream,)).start()
      password = raw_input()
      p_stopMasking = 1
    except Exception, e:
      p_stopMasking = 1
      print "Error Occured"
      print e
      exit()
  else:
    password = console.readPassword()
  return String.valueOf(password)


# internal - masking input
# -----------------------------------------------------------------------------
def _doMasking(stream):
  while not p_stopMasking:
    stream.write("\010*")
    #stream.write("\n")
    stream.flush()
    time.sleep(0.01)





# Connect - populate credentials from input
# -----------------------------------------------------------------------------
def promptedLogin():
  global username
  global password
  print 'Server: '+os.environ.get('SERVER')
  print 'Port:   '+os.environ.get('ADMIN_PORT')
  connectstr = 't3://'+os.environ.get('SERVER')+':'+os.environ.get('ADMIN_PORT')
  print '-----------------------------------------------------------'
  print 'Connecting to: '+connectstr
  print '-----------------------------------------------------------'
  print 'Enter username:'
  username = raw_input();
  print ''

  print 'Enter password (hidden):'
  password = getPass(sys.stdout)

  os.environ['FMW_ADMINUSER']=username
  os.environ['FMW_ADMINPWD']=password

  #print 'SERVER:        '+os.environ.get('SERVER')
  #print 'FMW_ADMINPORT: '+os.environ.get('FMW_ADMINPORT')
  #print 'FMW_ADMINUSER: '+os.environ.get('FMW_ADMINUSER')
  #print 'FMW_ADMINPWD:  '+os.environ.get('FMW_ADMINPWD')

  try:
    connect(os.environ.get('FMW_ADMINUSER'),os.environ.get('FMW_ADMINPWD'), connectstr)
  except Exception, err:
    raise
    sys.exit(1)


# Clear Screen
def clear():
    if _platform == "linux" or _platform == "linux2":
        # linux
        os.system('clear')
    #elif _platform == "darwin":
        # MAC OS X
    elif _platform == "win32":
        # Windows
        os.system('cls')
    elif _platform == "win64":
        # Windows 64-bit
        os.system('cls')


# -------------------------------------------------------------------------------------------------------
# File Output management
# -------------------------------------------------------------------------------------------------------
def makeOutDir():
    print '\nProvide output directory (with Write access)'
    #if os.environ.get('SCRIPT_OUTDIR') is None:
    # os.environ.get('HOME')
    os.environ['SCRIPT_OUTDIR'] = '/home/userid/shared/output'
    print 'Default: ' + os.environ.get('SCRIPT_OUTDIR')
    print '\n[Enter] to accept default'
    od = raw_input("> ")
    if od <> '' : os.environ['SCRIPT_OUTDIR'] = od

    outdir = os.environ.get('SCRIPT_OUTDIR')+'/'+os.environ.get('SERVER')+'_'+os.environ.get('ADMIN_PORT')+datetime.now().strftime('_%Y%m%d_%H%M%S')

    try:
      print 'Make output dir if it doesnt already exist: ' + outdir
      os.mkdir(outdir)
      return outdir
    except OSError, e:
      if e.errno != errno.EEXIST:
        print '** FAILED TO WRITE DIRECTORY **'
        print outdir
        print '....starting over'
        makeOutDir()
        #raise  # This was not a "directory exist" error..


# Main definition - constants
menu_actions  = {}

# =======================
#     MENUS FUNCTIONS
# =======================

# Mnemonic
def menu_mnemonic():
    print "_______________________________________\n"
    print "  Choose OBIEE Application (mnemonic)"
    print "_______________________________________\n"
    print "1. Application 1"
    print "2. Application 2"
    print "\n0. Quit"

    choice = raw_input("> ")
    ch = choice.lower()
    print "selected: ["+choice+"]"
    if ch == '1':
        os.environ['MNEMONIC']='APP1'
        menu_APP1_env()
    elif ch == '2':
        os.environ['MNEMONIC']='APP2'
        menu_APP2_env()
    elif ch == '0':
        menu_actions[choice]()
    else:
        print "\n["+choice+"] is an invalid selection, try again"
        #choice = raw_input("> ")
        menu_mnemonic()
    return


# Menu APP1 Environment
def menu_APP1_env():
    print "_______________________________________\n"
    print "  Choose an environment for " + os.environ['MNEMONIC']
    print "_______________________________________\n"
    print "x. Sandbox       serversbx:7001"
    print "d. Development   serverdev:7001"
    print "s. SIT           serversit:7001"
    print "u. UAT           serveruat:7001"
    print "p. Production    serverprod:7001"
    print "r. Disaster Rec  serverdr:7001"
    print "\n0. Quit"
    choice = raw_input("> ")
    exec_menu_APP1_env(choice)


# Environment
def exec_menu_APP1_env(choice):
    ch = choice.lower()
    if ch == 'x':
        os.environ['SERVER']='serversbx'
        os.environ['ADMIN_PORT']='7001'
    elif ch == 'd':
        os.environ['SERVER']='serverdev'
        os.environ['ADMIN_PORT']='7001'
    elif ch == 's':
        os.environ['SERVER']='serversit'
        os.environ['ADMIN_PORT']='7001'
    elif ch == 'u':
        os.environ['SERVER']='serveruat'
        os.environ['ADMIN_PORT']='7001'
    elif ch == 'p':
        os.environ['SERVER']='serverprod'
        os.environ['ADMIN_PORT']='7001'
    elif ch == 'r':
        os.environ['SERVER']='serverdr'
        os.environ['ADMIN_PORT']='7001'
    elif ch == '':
        print "...going back"
        menu_actions['menu_mnemonic']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "\nInvalid selection, please try again.\n"
            menu_actions['menu_APP1_env']()
    return


# Menu APP2 Environment
def menu_APP2_env():
    print "_______________________________________\n"
    print "  Choose an environment for " + os.environ['MNEMONIC']
    print "_______________________________________\n"
    print "d. Development   serverdev2:7777"
    print "s. SIT           serversit2:7777"
    print "u. UAT           serveruat2:7777"
    print "p. Production    serverprod2:7777"
    print "r. Disaster Rec  serverdr2:7777"
    print "\n0. Quit"
    choice = raw_input("> ")
    exec_menu_APP2_env(choice)


# Environment
def exec_menu_APP2_env(choice):
    ch = choice.lower()
    if ch == 'd':
        os.environ['SERVER']='serverdev2'
        os.environ['ADMIN_PORT']='7777'
    elif ch == 's':
        os.environ['SERVER']='serversit2'
        os.environ['ADMIN_PORT']='7777'
    elif ch == 'u':
        os.environ['SERVER']='serveruat2'
        os.environ['ADMIN_PORT']='7777'
    elif ch == 'p':
        os.environ['SERVER']='serverprod2'
        os.environ['ADMIN_PORT']='7777'
    elif ch == 'r':
        os.environ['SERVER']='serverdr2'
        os.environ['ADMIN_PORT']='7777'
        print "\nInvalid selection, please try again.\n"
    elif ch == '':
        print "...going back"
        menu_actions['menu_mnemonic']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "\nInvalid selection, please try again.\n"
            menu_actions['menu_APP2_env']()
    return



def print_envvars():
    #clear()
    print "_______________________________________\n"
    print "    Chosen environment for "+os.environ.get('MNEMONIC')
    print "_______________________________________\n"
    print '     SERVER:   '+os.environ.get('SERVER')
    print ' ADMIN_PORT:   '+os.environ.get('ADMIN_PORT')

# Exit program
def exit():
    sys.exit()




# =============================================================================
#
#                                       Begin Code
#
# =============================================================================

# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'menu_mnemonic': menu_mnemonic,
    'menu_APP1_env': menu_APP1_env,
    'menu_APP2_env': menu_APP2_env,
    '0': exit,
}



menu_mnemonic()
print_envvars()
print "\n\nOK {[y]/n)?"
choice = raw_input("> ")
if choice == 'n':
    menu_mnemonic()


# Create output directory
outdir = makeOutDir()

# Connect, prompt for credentials
promptedLogin()


# -------------------------------------------------------------------------------------------------------
# Set parameter preferences for WL API calls. These could be in a details.properties file
# or hard-coded, as we have done here.
# -------------------------------------------------------------------------------------------------------

# OPTION: details.properties file - for use in unit testing
#propInputStream = FileInputStream("details.properties")
#configProps = Properties()
#configProps.load(propInputStream)
#configProps.get("user.name.wildcard")
#configProps.get("maximum.to.return")

# OPTION: hardcode since these values won't change in the real world usage and having another file such as
# details.properties only unnecessarily complicates things.
userNameWildcard="*"
maximumToReturn=0

fn_userrolesDBG     = outdir+'/user-roles.DBG'
fnAppRoleOut        = outdir+'/AppRoleListWLS.out'
fn_WLGroups         = outdir+'/WLGroups.out'


#==============================================================================
# Web Logic Security
#==============================================================================

realm = cmo.getSecurityConfiguration().getDefaultRealm()
atns = realm.getAuthenticationProviders()

# -----------------------------------------------------------------------------
# Web Logic Global Roles
# -----------------------------------------------------------------------------
print '--------------------------------'
print 'Getting WL Global Roles:'
print '--------------------------------'

rm=cmo.getSecurityConfiguration().getDefaultRealm().lookupRoleMapper("XACMLRoleMapper")

fnWLGRprefix = outdir+'/WLglobalrole'
print 'Getting Web Logic Global Roles'
role = ['Admin', 'AdminChannelUser', 'Anonymous', 'AppTester', 'CrossDomainConnector', 'Deployer', 'Monitor','Operator', 'OracleSystemRole']
for r in role:
    print '...'+r
    expr = rm.getRoleExpression(None,r);
    f = open(fnWLGRprefix+'-'+r, 'w')
    f.write(expr)
    f.close()

print ''




# -----------------------------------------------------------------------------
# DefaultAuthenticator
#
# Web Logic Group Members - EFFECTIVE roles (including indirect or inherited role assignments)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
fGM_userrolesDBG = open(fn_userrolesDBG, 'w')
fGM_userrolesDBG.write('Parent Type,Parent,Member Type,Member\n')

print 'WLS: Users in Groups...processing'

DefaultAuthr = cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider('DefaultAuthenticator')

f = open(outdir+'/WLuserlist.out', 'w')
f.write('Web Logic User\n')
userList = DefaultAuthr.listUsers("*", 100)

print '======================================================================'
print 'Below are the List of USERS which are in DefaultAuthenticator'
print '======================================================================'
num = 1
while DefaultAuthr.haveCurrent(userList):
    print num,' - '+ DefaultAuthr.getCurrentName(userList)
    f.write(str(num)+' - '+ DefaultAuthr.getCurrentName(userList)+'\n')
    DefaultAuthr.advance(userList)
    num = num+1
print '======================================================================'
f.close()




# List WL Groups in a single file
# -----------------------------------------------------------------------------
f_WLGroups = open(fn_WLGroups, 'w')
curWLGroups =  DefaultAuthr.listGroups("*",int(maximumToReturn))
while DefaultAuthr.haveCurrent(curWLGroups):
  nextGroup = DefaultAuthr.getCurrentName(curWLGroups)
  print 'WL Group: ' + nextGroup
  f_WLGroups.write(nextGroup+'\n')

  # List WL Users as members of Groups
  # -----------------------------------------------------------------------------
  group = DefaultAuthr.getCurrentName(curWLGroups)

  fnWLGroupMembersOut = outdir+'/WLGroup-'+group+'.out'
  fWLGroupMembersOut = open(fnWLGroupMembersOut, 'w')
  fWLGroupMembersOut.write('')

  #if false:
  #  # ==================================================================================
  #  # TECHNIQUE 1 - listAllUsersInGroup
  #  # ==================================================================================
  #  usersInGroup = DefaultAuthr.listAllUsersInGroup(group,"*",int(maximumToReturn))
  #
  #  # Get users of each WL Group and write to an out file by the Group name
  #  #orig_stdout = sys.stdout
  #  for user in usersInGroup:
  #    fGM_userrolesDBG.write('WLGroup,'+group+',WLUser,'+user+'\n')
  #    fWLGroupMembersOut.write(user+'\n')
  #
  #  else:

  # ==================================================================================
  # TECHNIQUE 2 - listGroupMembers
  # includes members who are of type {User, Group}
  # ==================================================================================
  members = DefaultAuthr.listGroupMembers(group,"*",0)

  while DefaultAuthr.haveCurrent(members):
    user = DefaultAuthr.getCurrentName(members)
    # Check if this member is a Group (if so, record it as a Group, else it must be a user)
    if DefaultAuthr.groupExists(user):
      print 'WL Group: ' + nextGroup + ',WLGroup,'+user
      fGM_userrolesDBG.write('WLGroup,'+group+',WLGroup,'+user+'\n')
      fWLGroupMembersOut.write(user+',WLGroup\n')
    else:
      print 'WL Group: ' + nextGroup + ',WLUser,'+user
      fGM_userrolesDBG.write('WLGroup,'+group+',WLUser,'+user+'\n')
      fWLGroupMembersOut.write(user+',WLUser\n')
    DefaultAuthr.advance(members)

  fWLGroupMembersOut.close()
  DefaultAuthr.advance(curWLGroups)
DefaultAuthr.close(curWLGroups)
print 'WLS: Users in Groups...complete'


#==============================================================================
# Fusion Middleware Security
#==============================================================================

# -----------------------------------------------------------------------------
# Fusion Middleware Application Role Members
# -----------------------------------------------------------------------------
# Output standard user-role list which needs to be parsed

print 'FMW: Application Roles in app stripe obi...getting'
orig_stdout = sys.stdout
fAppRoleOut = file(fnAppRoleOut, 'w')
sys.stdout = fAppRoleOut
try:
  listAppRoles(appStripe="obi")
except Exception, err:
  print 'ERROR: %sn' % str(err)
  #raise
  sys.exit(1)
sys.stdout = orig_stdout

# -----------------------------------------------------------------------------
# Read List of App Roles output to parse it into a clean list of App Roles.
# Place in a list in memory.
# -----------------------------------------------------------------------------
print 'FMW: Application Roles in app stripe obi...parsing raw output'
fAppRoleOut.seek(0)
i=0
listAppRole = []
for line in fAppRoleOut:
  newline = line.replace("[ [Principal Clz Name : oracle.security.jps.service.policystore.ApplicationRole, Principal Name : ", "")
  iComma = newline.find(',')
  listAppRole.append(newline[:iComma])
  i=i+1
fAppRoleOut.close()

# -----------------------------------------------------------------------------
# Read App Role list to get members.
# WLS command listAppRoleMembers dumps to standard output.
# Must capture output and parse for members which can be users, groups or other App Roles.
# -----------------------------------------------------------------------------

listAppRole.sort()

for approle in listAppRole:
  # For each App Role in list, dump members to a file for parsing
  # replace std out so output of listAppRoleMembers goes to file instead of console
  orig_stdout = sys.stdout
  fnAppRoleMembersOut = outdir+'/AppRole-'+approle+'.out'
  fAppRoleMembersOut = open(fnAppRoleMembersOut, 'w')
  sys.stdout = fAppRoleMembersOut
  listAppRoleMembers(appStripe="obi", appRoleName=approle)
  sys.stdout = orig_stdout

  print 'AppRole: ' + approle

  # parse the file for members
  fAppRoleMembersOut.seek(0)
  for line in fAppRoleMembersOut:
    newlineU = line.replace("[Principal Clz Name : weblogic.security.principal.WLSUserImpl, Principal Name : ","")

    # CHECK FOR: not user
    if newlineU[0] == "[":
      newlineG = newlineU.replace("[Principal Clz Name : weblogic.security.principal.WLSGroupImpl, Principal Name : ","")

      # CHECK FOR: not group
      if newlineG[0] == "[":
        newlineA = newlineG.replace("[Principal Clz Name : oracle.security.jps.service.policystore.ApplicationRole, Principal Name : ","")

        # CHECK FOR: not Application Role (Fusion Middleware)
        if newlineA[0] == "[":
          # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          #  Internal
          # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          newlineI = newlineA.replace("[Principal Clz Name : oracle.security.jps.internal.core.principals.JpsAuthenticatedRoleImpl, Principal Name : ","")
          iComma = newlineI.find(',')
          print 'AppRole,'+approle+',INTERNAL,'+newlineI[:iComma]
          fGM_userrolesDBG.write('AppRole,'+approle+',INTERNAL,'+newlineI[:iComma]+'\n')

        else:
          # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          #   Application Role
          # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          iComma = newlineA.find(',')
          print 'AppRole,'+approle+',AppRole,'+newlineA[:iComma]
          fGM_userrolesDBG.write('AppRole,'+approle+',AppRole,'+newlineA[:iComma]+'\n')

      else:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #   Group (Web Logic)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        iComma = newlineG.find(',')
        print 'AppRole,'+approle+',WLGroup,'+newlineG[:iComma]
        fGM_userrolesDBG.write('AppRole,'+approle+',WLGroup,'+newlineG[:iComma]+'\n')

    else:
      # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      #   User
      # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      iComma = newlineU.find(',')
      print 'AppRole,'+approle+',WLUser,'+newlineU[:iComma]
      fGM_userrolesDBG.write('AppRole,'+approle+',WLUser,'+newlineU[:iComma]+'\n')

  fAppRoleMembersOut.close()

fGM_userrolesDBG.close()


orig_stdout = sys.stdout
fResourcePermissions = open(outdir+"/OBIstripeResourcePermissions.txt", 'w')
sys.stdout = fResourcePermissions
listResourceTypes(appStripe="obi")
sys.stdout = orig_stdout