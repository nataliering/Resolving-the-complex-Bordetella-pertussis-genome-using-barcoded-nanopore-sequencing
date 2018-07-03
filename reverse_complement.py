#!/usr/bin/python
import sys
import argparse
parser=argparse.ArgumentParser(
    description='''e.g. reverse_complement.py <draft_genome.fasta> <reverse_complemented_genome.fasta> ''',
    epilog="""code adapted from Damian Kao at https://www.biostars.org/p/14614/""")
parser.add_argument("inFile",type=argparse.FileType('r'))
parser.add_argument("outFile", type=argparse.FileType('w'))
args=parser.parse_args()

#inFile = open(sys.argv[1],'r')
#outFile = open(sys.argv[2], 'rw')
sys.stdout = args.outFile

nuc = {'A':'T','T':'A','G':'C','C':'G'}

def revComp(seq):
    rev = ''
    for i in range(len(seq) - 1,-1,-1):
        rev += nuc[seq[i]]

    return rev

header = ''
seq = ''
for line in args.inFile:
    if line[0] == ">":
        if header != '':
            print header
            print revComp(seq.upper())

        header = line.strip()
        seq = ''
    else:
        seq += line.strip()

print header
print revComp(seq.upper())

