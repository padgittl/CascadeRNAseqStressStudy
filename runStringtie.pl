#!/usr/bin/perl -w
use strict;
$|=1;

my $StringTie = "stringtie";
my $usage = "Usage:\n$0 <tissue-specific, sorted bam file> <annotation gff file>\n";
my $bamfile = $ARGV[0] or die $usage;
my $annotationFile = $ARGV[1] or die $usage;
my $queue = "nucleotide";

my($prefix) = $bamfile =~ /([^\/]*)\.bam/ or die "Could not parse file\n";
my $output = $prefix . ".gtf";
my $outTab = $prefix . ".tab";
my $errFile = $prefix . ".err";
my $scriptFile = $prefix . ".sh";
# my $options = "$bamfile -j 2 -o $output --fr -A $outTab";
my $options = "$bamfile -j 2 -e -G $annotationFile -o $output --fr -A $outTab";
my $command = "$StringTie $options";

open(SCRIPT,">$scriptFile") or die "Could not open $scriptFile for writing.\n";
print SCRIPT "#!/bin/bash

#\$ -cwd                # Current working directory
#\$ -S /bin/bash        # Shell 
#\$ -N $prefix          # Job name
#\$ -j y                # merge output and error
#\$ -o $errFile         # Stout name
#\$ -q $queue           # use nucleotide queue 
#\$ -l mem_free=10G     # specify max memory
#\$ -V                  # Preserve environmental variables

CMD=\"$command\"
\$CMD

";
close(SCRIPT);

system("qsub $scriptFile");
