#!/usr/bin/perl

use warnings;

#filename

my $fnn = $ARGV[0];
#my $pause = $ARGV[1];
my $resume = $ARGV[1];


open(my $MYFILE, $fnn)
    or die "could not open file '$fnn' $!";

open(my $rfh, '>' , $resume); 
#open(my $pfh, '>' , $pause);


while (my $line = <$MYFILE>) {
    # if line = resume
    if($line =~ /resume/){
	if($line =~ /,(.*)$/){
	    print $rfh $1, "\n";
	}
    }
    if($line =~/pause/){
	if($line =~ /,(.*)$/){
	    print $rfh $1, "\n";
	}
    }
}

#close $pfh;
close $rfh;
close $MYFILE;
