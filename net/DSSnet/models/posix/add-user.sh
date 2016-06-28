#!/bin/sh

# Define GSF time-series framework service for which to add user
service=openPDC

# Define absolute path for script log
log=${PWD}/add-user.log

# Define destination directory - do not modify value, installation script depends on format:
destDir=/opt/openPDC

show_help ()
{
	echo "${service} add user script (SQLite only)"
	echo "    Options:"
	echo "        -h: Show help"
    echo "        -u: User to add (defaults to current user)"
	echo "        -r: Role for user (defaults to Administrator)"
}

while getopts "hu:r:" opt; do
	case "$opt" in
        h)
			show_help
			exit 0
			;;
        u)  user=$OPTARG
			;;
		r)  role=$OPTARG
	esac
done

if [ -z "$user" ]
then
	user=`whoami`

    if [ "${user}" = "root" ]; then
        echo "ERROR: Must specify a user to add when executing as root." 1>&2
        show_help
        exit 1
    fi
fi

if [ -z "$role" ]
then
	role=Administrator
fi

# Create log file
echo "${service} add user" > ${log}
date >> ${log}

# Add user to configuration database
echo "INSERT INTO UserAccount(Name, DefaultNodeID) VALUES('${user}', (SELECT ID FROM Node));" >> ${log}
sqlite3 -line ${destDir}/ConfigurationCache/${service}.db "INSERT INTO UserAccount(Name, DefaultNodeID) VALUES('${user}', (SELECT ID FROM Node));" >> ${log}

# Apply role to user in configuration database
echo "INSERT INTO ApplicationRole(ApplicationRoleID, UserAccountID) VALUES((SELECT ID FROM ApplicationRole WHERE Name = '${role}'), (SELECT ID FROM UserAccount WHERE Name = '${user}'));" >> ${log}
sqlite3 -line ${destDir}/ConfigurationCache/${service}.db "INSERT INTO ApplicationRoleUserAccount(ApplicationRoleID, UserAccountID) VALUES((SELECT ID FROM ApplicationRole WHERE Name = '${role}'), (SELECT ID FROM UserAccount WHERE Name = '${user}'));" >> ${log}