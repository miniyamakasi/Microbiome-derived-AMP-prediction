#!/usr/bin/perl
use strict;
use warnings;

my %id;

open(IN,"type.txt");

while(<IN>)
{
    chomp;
    my @a=split(/\t/);

    $id{$a[0]}=1;
}
close IN;

my %cut;

foreach my $f(
    "SignalPredResult_summary.signalp5",
    "SignalPredResult2_summary.signalp5"
)
{
    open(IN,$f);

    while(<IN>)
    {
        next if /^#/;

        chomp;

        my @a=split(/\t/);

        my $name=$a[0];

        next unless exists $id{$name};

        if(/(\d+)-(\d+)/)
        {
            $cut{$name}=$2;
        }
    }

    close IN;
}

my %seq;

$/=">";

open(IN,"protein.fasta");

while(<IN>)
{
    chomp;

    next if $_ eq "";

    my @a=split(/\n/);

    my $head=shift @a;

    my ($id)=split(/\s+/,$head);

    my $seq=join("",@a);

    $seq{$id}=$seq;
}

close IN;

$/="\n";

open(OUT,">signal_cut.fasta");

foreach my $id(keys %cut)
{
    my $seq=$seq{$id};

    my $cutsite=$cut{$id};

    my $mature=substr(
        $seq,
        $cutsite
    );

    print OUT ">$id\n$mature\n";
}

close OUT;