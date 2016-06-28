#!/bin/bash
### BEGIN INIT INFO
# Provides:          openPDC
# Required-Start:    $remote_fs $syslog $network $time
# Required-Stop:     $remote_fs $syslog $network $time
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# X-Interactive:     false
# Short-Description: openPDC
# Description:       Grid Protection Alliance openPDC
### END INIT INFO

# Define GSF time-series framework service to operate
service="openPDC"

# Define destination directory - do not modify value, installation script depends on format:
destDir=/opt/openPDC

# Define location of mono-service executable - do not modify value, installation script depends on format:
monoService=/usr/bin/mono-service

# Define the lock file for the service
pidFile="/var/run/${service}.pid"

# Define the Mono service launch command
command="${monoService} -m:${service} -l:${pidFile} ${destDir}/${service}.exe -RunAsService"

# Define time-out, in integer seconds, to wait for lock file management
timeout=10

if [ ! -x ${monoService} ]; then
    monoService=`which mono-service`
    
    if [ ! -x ${monoService} ]; then
        echo "ERROR: Unable to find mono-service executable." 1>&2
        exit 1
    fi
fi

if [ "$(id -u)" != "0" ]; then
    echo "ERROR: Operation must execute as root." 1>&2
    exit 1
fi

start()
{
    if [ -f $pidFile ]; then
        echo "ERROR: ${service} service appears to already be running, lock file ${pidFile} exists - cannot start." 1>&2
        exit 1
    else
        cd ${destDir}
        $command
        count=0

        while [ ! -f $pidFile ] && [ $count -lt $timeout ]
        do
            sleep 1
            let count=count+1
        done
        
        if [ -f $pidFile ]; then
            echo "${service} service started with process ID `cat $pidFile`..."
        else
            echo "WARNING: ${service} service start requested, but lock file does not exist after ${timeout} seconds..."
        fi
    fi
}

pause()
{
    if [ -f $pidFile ]; then
        kill -USR1 `cat "$pidFile"`
        echo "${service} service paused..."
    else
        echo "ERROR: ${service} service does not appear to be running, lock file ${pidFile} does not exist - cannot pause." 1>&2
        exit 1
    fi
}

resume()
{
    if [ -f $pidFile ]; then
        kill -USR2 `cat "$pidFile"`
        echo "${service} service resumed..."
    else
        echo "ERROR: ${service} service does not appear to be running, lock file ${pidFile} does not exist - cannot resume." 1>&2
        exit 1
    fi
}

stop()
{
    if [ -f $pidFile ]; then
        kill `cat "$pidFile"`
        count=0

        while [ -f $pidFile ] && [ $count -lt $timeout ]
        do
            sleep 1
            let count=count+1
        done
        
        if [ -f $pidFile ]; then
            echo "WARNING: ${service} service stop requested, but lock file still exists after ${timeout} seconds..."
        else
            echo "${service} service stopped."
        fi
    else
        echo "ERROR: ${service} service does not appear to be running, lock file ${pidFile} does not exist - cannot stop." 1>&2
        exit 1
    fi
}

case "$1" in
    start)
        start
        exit 0
    ;;
    stop)
        stop
        exit 0
    ;;
    pause)
        pause
        exit 0
    ;;
    resume)
        resume
        exit 0
    ;;
    reload|restart|force-reload)
        stop
        start
        exit 0
    ;;
    **)
        echo "USAGE: $0 {start|stop|pause|resume|restart}" 1>&2
        exit 1
    ;;
esac
