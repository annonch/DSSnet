#!/bin/bash

# Define GSF time-series framework service to update
service=openPDC

# Define absolute path for script log
log=${PWD}/enable-security.log

# Define destination directory - do not modify value, installation script depends on format:
destDir=/opt/openPDC

if [ "$(id -u)" != "0" ]; then
    echo "ERROR: Operation must execute as root." 1>&2
    exit 1
fi

echo "WARNING: ${service} must not be running while enabling security, ensure service is stopped before continuing."
read -p "Are you ready to continue (y/N)? " -r -n 1
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Create log file
echo "${service} service security configuration" > ${log}
date >> ${log}

if [ ${OSTYPE} != ${OSTYPE#darwin} ]; then
    echo "Mac operating system detected..." >> ${log}
    isMac=1
else
    echo "Linux operating system assumed..." >> ${log}
    isMac=0
fi

# Build GSF POSIX library
cd gsf/Source/Tools/UnixTools/ >> ${log}
if [ $isMac -ne 0 ]; then
    sudo gcc -m32 -c -Wall -Werror -fpic GSF.POSIX.c >> ${log}
    sudo gcc -m32 -dynamiclib -undefined suppress -flat_namespace GSF.POSIX.o -o GSF.POSIX.so -lpam >> ${log}
else
    gcc -c -Wall -Werror -fpic GSF.POSIX.c >> ${log}
    gcc -shared -o GSF.POSIX.so GSF.POSIX.o -lpam -lpam_misc -lcrypt >> ${log}
fi
cp -v GSF.POSIX.so ${destDir} >> ${log}

# Secure remote interactions
sed -i.backup -e '/name="SecureRemoteInteractions"/ s/value="False"/value="True"/' ${destDir}/${service}.exe.config >> ${log}

echo
echo "${service} security enabled. To validate, add a user to the current"
echo "configuration, start the ${service} service, then run:"
echo "mono ${destDir}/${service}Console.exe"
