#!/bin/bash

# Define GSF time-series framework service to register
service=openPDC

# Define absolute path for script log
log=${PWD}/register-${service}.log

# Define destination directory - do not modify value, installation script depends on format:
destDir=/opt/openPDC

# Define flag to unregister service
unregister=0

show_help ()
{
	echo "${service} register service script"
	echo "    Options:"
	echo "        -h: Show help"
    echo "        -u: Unregister service"
}

# Get user input
OPTIND=1

while getopts "hu" opt; do
    case "$opt" in
		h)
			show_help
			exit 0
			;;
		u)  unregister=1
    esac
done

if [ "$(id -u)" != "0" ]; then
    echo "ERROR: Operation must execute as root." 1>&2
    exit 1
fi

# Create log file
echo "${service} service registration" >> ${log}
date >> ${log}

if [ ${OSTYPE} != ${OSTYPE#darwin} ]; then
    echo "Mac operating system detected..." >> ${log}
    isMac=1
else
    echo "Linux operating system assumed..." >> ${log}
    isMac=0
fi

if [ $unregister -ne 0 ]; then
    echo Stopping ${service}...
    echo
    ${destDir}/${service} stop
    
    echo       
    echo "Unregistering ${service} service..."
    echo
    
    echo "Unregistering ${service} service..." >> ${log}
    
    if [ $isMac -ne 0 ]; then
        launchctl unload /Library/LaunchDaemons/${service}.plist >> ${log}
        rm -v /Library/LaunchDaemons/${service}.plist >> ${log}
    else
        update-rc.d -f ${service} remove
        rm -v ${destDir}/${service} >> ${log}
        rm -v /etc/init.d/${service} >> ${log}
        echo
    fi    

    echo "${service} service unregistered."
else
    echo "WARNING: ${service} must not be running while registering service as a daemon, ensure service is stopped before continuing."
    read -p "Are you ready to continue (y/N)? " -r -n 1
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi

    echo Registering ${service} service to auto-start...
    echo

    if [ $isMac -ne 0 ]; then
        cp -v ${service}.sh ${destDir}/${service} >> ${log}
        chmod -v +x ${destDir}/${service} >> ${log}
        cp -v ${service}.plist /Library/LaunchDaemons >> ${log}
        launchctl load /Library/LaunchDaemons/${service}.plist >> ${log}
    else
        cp -v ${service}.sh /etc/init.d/${service} >> ${log}
        chmod -v +x /etc/init.d/${service} >> ${log}
        update-rc.d ${service} defaults >> ${log}
        ln -sv /etc/init.d/${service} ${destDir}/${service} >> ${log}
        ${destDir}/${service} start
        echo
    fi

    echo "${service} service registration complete. To validate, run:"
    echo "mono ${destDir}/${service}Console.exe"
fi
