#!/usr/bin/perl
#
# perl program to parse tcp dump to find time of self healing
#
####################
#
#
#
# 
use strict;
use warnings;
#
my $filename = $ARGV[0];
#
open(my $fh, '<:encoding(UTF-8)', $filename)
    or die "could not open '$filename' $!";
#
my $odd = 1;
my $up_down = 1;
###


my $time = 0;

my $time_min = 0;
my $time_sec = 0.0;
my $time_hour = 0;

my $old_time = 0;

my $old_time_min = 0;
my $old_time_sec = 0;
my $old_time_hour = 0;

my $old_total_time = 0;
my $total_time = 0;
my $dif = 0;
#


while(my $row = <$fh>) {
    $odd = $odd + 1;
    chomp $row;
    if($odd % 2 == 0) {
	$old_time = $time;
	$old_time_min = $time_min;
	$old_time_sec = $time_sec;
	$old_time_hour= $time_hour;
	$time = substr $row, 0, 15;
	
        # 6-9 converted to double
	$time_sec = substr $time, 6, 9;
        # 3 -2 converted to int
	$time_min = substr $time ,3, 2;
	# 0 -2 hour
	$time_hour= substr $time, 0,2;

	$old_total_time= ($old_time_hour *3600 + $old_time_min * 60 + $old_time_sec);
	$total_time= ($time_hour *3600 + $time_min * 60 + $time_sec);
	#print "old time = $old_time_hour: $old_time_min :  $old_time_sec \n";
	#print "new time = $time_hour: $time_min :  $time_sec \n";
	#print "$old_total_time - $total_time \n";
	$dif = $total_time - $old_total_time;
	#print "$dif\n";	
		
	if ($dif > 2) {
	    if($old_time_min == 0 && $old_time_sec == 0) {
		
	    }
	    else {
		$up_down +=1;
		if($up_down % 2 ==0) {
		    #print "down took $dif\n";
		    print "$dif\n";
		}
		else {
		    #print "up took $dif\n";
		}
		#print "$row\n";
		    
	    }
	}
    }
#    print "$row\n";
}

