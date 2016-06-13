#!/usr/bin/perl
##########################
#  channon@hawk.iit.edu  #
##########################

# this file converts a load config file from the 
# power application style to the IED to be read 
# in from the coordinator

my $fnn = $ARGV[0];

open (my $MYFILE, $fnn)
    or die "Could not read file '$fnn' $!";
while(my $line = <$MYFILE>) {
    chomp $line;
    if($line =~ /^[#]/){
	print "#\n";
    }
    else{
	my($s,$e,$d,$p,$ip)=split /,/, $line;
	my($ipa,$ipb,$ipc,$ipd)=split /\./, $ip;
	print "LOAD ";
	print "$ipd ";
	print "$ip ";
	print "$p ";
	print "$s ";
	print "$d\n";
    }
}
