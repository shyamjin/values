
#############################################
#release notes                              #
#############################################
2.0.1

Features :
*Download tool (for windows )
*test connection to machine
*forgot password
*improved unix security
*clean services - cleaning old data and old builds ,
*tunneling in machine management
*support deployment by build




#############################################
#installation from master to account server #
#############################################

steps:
o   inputs (toolName , version,
o	Create account branch on master from version
o	Create location folder (if not exists)
o   establish ssh keys
o	Clone tool branch Repository to location

o	Create customization branch on account
o	Update DB : time create ,tool , version , location , original branch
