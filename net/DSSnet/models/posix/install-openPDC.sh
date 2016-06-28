#!/bin/bash

# Define GSF time-series framework service to be installed
service=openPDC

# Define stable release version
stableVersion="2.1"

# Define absolute path for script log
log=${PWD}/install-${service}.log

# Define destination directory
destDir=/opt/${service}

# Define flag to install GEP tester
installGEPTester=1

# Define root install address
address="http://www.gridprotectionalliance.org"

# Define flag to use nightly build
useNightlyBuild=0

# Define flag to preserve source code
preserveSourceCode=0

show_help ()
{
	echo "${service} installation script"
	echo "    Options:"
	echo "        -h: Show help"
	echo "        -n: Use nightly builds"
	echo "        -p: Preserve source code"
	echo "        -d: Install destination (defaults to ${destDir})"
    echo "        -u: Uninstall service"
}

uninstall ()
{
    if [ -d ${destDir} ]; then
        echo
        echo "WARNING: This will completely remove ${service} service, configuration and any archived data. Ensure all data and configuration in ${destDir} is backed up, as it will be deleted."
        read -p "Are you sure you want to continue (y/N)? " -r -n 1
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    echo
    echo "Uninstalling ${service} service..."

    # Update log with uninstall information
    echo "Uninstalling ${service} service..." >> ${log}
    date >> ${log}

    # Unregister service
    echo "Executing service unregister, see register-${service}.log for details..." >> ${log}
    bash register-${service}.sh -u >> ${log}
    
    # Make sure service is not running
    pkill -f ${service}.exe >> ${log}
    
    # Clear temporary folders and scripts
    echo "Clearing temporary folders and scripts..." >> ${log}
    rm -rv gsf >> ${log}    
    rm -rv ${service} >> ${log}
    rm -rv config >> ${log}
    rm -v ${service}.sh >> ${log}
    rm -v register-${service}.sh >> ${log}
    rm -v enable-security.sh >> ${log}
    rm -v add-user.sh >> ${log}
    
    # Remove installation folder
    echo "Deleting installation folder..." >> ${log}
    rm -rv ${destDir} >> ${log}

    echo "${service} service uninstalled..."
}

if [ "$(id -u)" != "0" ]; then
    echo "ERROR: Operation must execute as root." 1>&2
    exit 1
fi

# Get user input
OPTIND=1

while getopts "hinpd:u" opt; do
    case "$opt" in
		h)
			show_help
			exit 0
			;;
		i)  address="http://172.21.1.150"
			;;
		n)  useNightlyBuild=1
			;;
		p)  preserveSourceCode=1
			;;
		d)  destDir=$OPTARG
		    ;;
        u)
            uninstall
            exit 0
            ;;
    esac
done

if [ -d ${destDir} ]; then
    echo
	echo "WARNING: ${destDir} directory already exists. Ensure configuration in ${destDir} is backed up, as it will be overwritten."
	read -p "Are you sure you want to continue (y/N)? " -r -n 1
	if [[ ! $REPLY =~ ^[Yy]$ ]]; then
		exit 1
	fi
else
	mkdir ${destDir}
fi

# Create log file
echo "${service} service installation" > ${log}
date >> ${log}

if [ ${OSTYPE} != ${OSTYPE#darwin} ]; then
    echo "Mac operating system detected..." >> ${log}
    isMac=1
else
    echo "Linux operating system assumed..." >> ${log}
    isMac=0
fi

# Download other installation scripts
echo
echo Downloading additional installation scripts...
echo

# Remove scripts if they exist already so new destination directory can be applied
if [ -f ${service}.sh ]; then
    rm -v ${service}.sh >> ${log}
fi
wget ${address}/Products/${service}/Scripts/${service}.sh >> ${log}

if [ -f register-${service}.sh ]; then
    rm -v register-${service}.sh >> ${log}
fi
wget ${address}/Products/${service}/Scripts/register-${service}.sh >> ${log}

if [ -f enable-security.sh ]; then
    rm -v enable-security.sh >> ${log}
fi
wget ${address}/Products/${service}/Scripts/enable-security.sh >> ${log}

if [ -f add-user.sh ]; then
    rm -v add-user.sh >> ${log}
fi
wget ${address}/Products/${service}/Scripts/add-user.sh >> ${log}

if [ $isMac -ne 0 ]; then
    if [ -f ${service}.plist ]; then
        rm -v ${service}.plist >> ${log}
    fi
    wget ${address}/Products/${service}/Scripts/mac/${service}.plist >> ${log}
fi

echo Updating installation scripts with proper paths...
echo

# Regex escape destination directory
escapedDestDir=`echo "${destDir}" | sed -e 's/[\\/&]/\\\\&/g'`
    
# Regex escape mono-service executable
escapedMonoService=`which mono-service | sed -e 's/[\\/&]/\\\\&/g'`

# Apply destination directory to installation scripts
sed -i~ -e "s/#DESTDIR#/${escapedDestDir}/" -e "s/#MONOSERVICE#/${escapedMonoService}/" ${service}.sh >> ${log}
rm -v ${service}.sh~ >> ${log}

sed -i~ -e "s/#DESTDIR#/${escapedDestDir}/" register-${service}.sh >> ${log}
rm -v register-${service}.sh~ >> ${log}

sed -i~ -e "s/#DESTDIR#/${escapedDestDir}/" enable-security.sh >> ${log}
rm -v enable-security.sh~ >> ${log}

sed -i~ -e "s/#DESTDIR#/${escapedDestDir}/" add-user.sh >> ${log}
rm -v add-user.sh~ >> ${log}

if [ $isMac -ne 0 ]; then
    sed -i~ -e "s/#DESTDIR#/${escapedDestDir}/" ${service}.plist >> ${log}
    rm -v ${service}.plist~ >> ${log}
fi

# Download GSF source
echo Downloading Grid Solutions Framework source code...
echo
mkdir -v gsf >> ${log}
cd gsf

if [ $useNightlyBuild -ne 0 ]; then
	wget ${address}/NightlyBuilds/GridSolutionsFramework/Beta/GridSolutionsFramework.Source.zip >> ${log}
else
	wget ${address}/Products/${service}/Releases/${stableVersion}/POSIX/gsf/Source.zip >> ${log}
fi

# Extract GSF source
echo Extracting Grid Solutions Framework source code...
echo
unzip Source.zip -d Source >> ${log}
rm -v Source.zip >> ${log}
cd ..

# Download host application source
echo Downloading ${service} source code...
echo
mkdir -v ${service} >> ${log}
cd ${service}

if [ $useNightlyBuild -ne 0 ]; then
	wget ${address}/NightlyBuilds/${service}/Source.zip >> ${log}
else
	wget ${address}/Products/${service}/Releases/${stableVersion}/POSIX/${service}/Source.zip >> ${log}
fi

# Extract host application source
echo Extracting ${service} source code...
echo
unzip Source.zip -d Source >> ${log}
rm -v Source.zip >> ${log}
cd ..

# Clear out existing GSF dependencies (prevents possible compile with Windows binaries)
rm -v ${service}/Source/Dependencies/GSF/*.*  >> ${log}

# Download POSIX configuration files
echo Downloading default POSIX configuration for ${service}...
echo
wget ${address}/Products/${service}/Scripts/POSIXConfig.zip >> ${log}

# Extract POSIX configuration files
echo Extracting default POSIX configuration for ${service}...
echo
unzip POSIXConfig.zip >> ${log}
cp -v config/${service}.exe.config config/${service}Shell.exe.config >> ${log}
rm POSIXConfig.zip

# Build GSF source
echo Building Grid Solutions Framework for Mono...
echo
cd gsf/Source
sh buildmono.sh >> ${log}
cd ../..

# Update host application GSF dependencies
echo Updating ${service} GSF depencencies with Mono libraries...
echo
cp -v gsf/Build/Output/Mono/Libraries/* ${service}/Source/Dependencies/GSF  >> ${log}

# Build host application
echo Building ${service} for Mono...
echo
cd ${service}/Source
sh buildmono.sh >> ${log}
cd ../..

# Install host application
echo Installing ${service}...
echo
cp -rv ${service}/Build/Output/Mono/Applications/${service}/* ${destDir} >> ${log}
cp -v ${service}/Source/Applications/${service}/${service}/Sample1344.PmuCapture ${destDir}/ >> ${log}
mkdir -v "${destDir}/Database Scripts" >> ${log}
cp -rv ${service}/Source/Data/* "${destDir}/Database Scripts" >> ${log}
cp -rv ${service}/Source/Dependencies/GSF/* ${destDir}/ >> ${log}
cp -v ${service}/Source/Applications/${service}/${service}Setup/ConfigCrypter.exe* ${destDir}/ >> ${log}
cp -v ${service}/Source/Applications/${service}/${service}Setup/HistorianPlaybackUtility.exe* ${destDir}/ >> ${log}
cp -v ${service}/Source/Applications/${service}/${service}Setup/DataMigrationUtility.exe* ${destDir}/ >> ${log}
cp -v gsf/Build/Output/Mono/Tools/MonoGenCert/MonoGenCert.exe ${destDir}/ >> ${log}

# Only copy executable for configuration editor, config file is updated on POSIX for this tool
cp -v ${service}/Source/Applications/${service}/${service}Setup/ConfigurationEditor.exe ${destDir}/ >> ${log}

# Create TLS keys and certificates
echo Creating transport layer security keys and certificates...
echo
cd ${destDir}
mono MonoGenCert.exe ${service} >> ${log}
cd - > /dev/null

if [ $installGEPTester -ne 0 ]; then
	# Install GEP tool
	echo Installing GEP Subscription Tester...
	echo
	cd ${service}/Source/Applications/${service}/${service}Setup/
	unzip "GEP Subscription Tester.zip" >> ${log}

	if [ $isMac -ne 0 ]; then
		cp -rv "GSF Graph Lines/Mac/" ${destDir}/GEPTester >> ${log}
		chmod -R +x ${destDir}/GEPTester
	else
		cp -rv "GSF Graph Lines/Linux/" ${destDir}/GEPTester >> ${log}
		chmod -v +x ${destDir}/GEPTester/GraphLines.x86 >> ${log}
		chmod -v +x ${destDir}/GEPTester/GraphLines.x86_64 >> ${log}
	fi

	chmod -vR ugo+rw ${destDir}/GEPTester >> ${log}
	cd - > /dev/null
fi

# Copy POSIX configuration files to host application installation folder
echo Applying default POSIX configuration to ${service} installation...
echo
cp -v config/* ${destDir}/  >> ${log}

# Create a configuration cache folder
mkdir ${destDir}/ConfigurationCache >> ${log}

# Move the SQLite configuration database to the configuration cache folder (this location matches openPDC configuration and will allow safer remote access)
mv ${destDir}/${service}.db ${destDir}/ConfigurationCache

if [ $preserveSourceCode -eq 0 ]; then
	echo Deleting temporary installation files...
	echo
	rm -rv gsf >> ${log}
	rm -rv ${service} >> ${log}
	rm -rv config >> ${log}
fi

echo "${service} installation complete. To start application, run:"
echo "sudo mono ${destDir}/${service}.exe -RunAsConsole"
