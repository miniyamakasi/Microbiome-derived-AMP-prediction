#!/usr/bin/env perl
use strict;
use warnings;

# Extract FASTA records whose identifiers occur in the first column of a
# tab-separated PSORTb filtering table.
#
# Usage:
#   perl extract_psort_seq_lq.pl selected_ids.tsv input.fasta output.fasta

@ARGV == 3 or die "Usage: perl $0 <selected_ids.tsv> <input.fasta> <output.fasta>\n";
my ($id_file, $fasta_file, $output_file) = @ARGV;

open my $ID, '<', $id_file or die "Cannot open $id_file: $!\n";
my %keep;
while (my $line = <$ID>) {
    chomp $line;
    $line =~ s/\r$//;
    next if $line =~ /^\s*$/;
    my ($id) = split /\t/, $line, 2;
    $id =~ s/^\s+|\s+$//g;
    next if $id eq '';
    next if lc($id) =~ /^(sequence[_ ]?id|seq[_ ]?id|id)$/;
    $keep{$id} = 1;
}
close $ID;

open my $IN, '<', $fasta_file or die "Cannot open $fasta_file: $!\n";
open my $OUT, '>', $output_file or die "Cannot write $output_file: $!\n";

my ($header, @sequence_lines);
my ($written, $read) = (0, 0);

sub emit_record {
    return unless defined $header;
    my ($id) = $header =~ /^>(\S+)/;
    die "Malformed FASTA header: $header\n" unless defined $id;
    $read++;
    if (exists $keep{$id}) {
        print {$OUT} $header, "\n", @sequence_lines;
        $written++;
    }
}

while (my $line = <$IN>) {
    $line =~ s/\r\n?/\n/g;
    chomp $line;
    if ($line =~ /^>/) {
        emit_record();
        $header = $line;
        @sequence_lines = ();
    } else {
        next if $line =~ /^\s*$/;
        die "Sequence encountered before first FASTA header\n" unless defined $header;
        $line =~ s/\s+//g;
        push @sequence_lines, $line . "\n";
    }
}
emit_record();

close $IN;
close $OUT;

warn "Selected IDs: " . scalar(keys %keep) . "; FASTA records read: $read; records written: $written\n";
