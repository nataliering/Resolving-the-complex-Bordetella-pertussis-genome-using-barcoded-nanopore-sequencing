
#! /bin/bash

if [ "$1" == "-h" ] ; then
    echo "Usage: summary_stats.sh <in_fasta> <out_prefix(will be .txt)>"
    exit 0
fi

if [ "$1" == "--help" ] ; then
    echo "Usage: summary_stats.sh <in_fasta> <out_prefix(will be .text)>"
    exit 0
fi

seq_length.py $1 | cut -f 2 | all_stats.sh
#seq_length.py $1 | cut -f 2 | all_stats.sh > $2.txt
