#!/usr/bin/env python
"""Extract n random sequences from a fastq file.

Usage:
    %program <input_file> n <output_file>"""

# Importing modules
import sys
import re
import random

# Defining classes
class Fastq(object):
    """Fastq object with name and sequence
    """
    def __init__(self, name, seq, name2, qual):
        self.name = name
        self.seq = seq
        self.name2 = name2
        self.qual = qual
    def write_to_file(self, handle):
        handle.write("@" + self.name + "\n")
        handle.write(self.seq + "\n")
        handle.write("+" + self.name2 + "\n")
        handle.write(self.qual + "\n")

# Defining functions
def fastq_iterator(input_file):
    """Takes a fastq file infile and returns a fastq object iterator
    """
    with open(input_file) as f:
        while True:
            name = f.readline().strip()[1:]
            if not name:
                break
            seq = f.readline().strip()
            name2 = f.readline().strip()[1:]
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Parsing user input
try:
    fastq_file = sys.argv[1]  # Input fastq file
    number_wanted = int(sys.argv[2]) # Number of sequences wanted
    result_file = sys.argv[3] # Output fastq file
except:
    print __doc__
    sys.exit(0)

# Main
if __name__ == '__main__':
    fastq_sequences = fastq_iterator(fastq_file)
    index = 0
    retained = []
    for fastq in fastq_sequences:
        index += 1
        if index <= number_wanted:
            retained.append(fastq)
        else:
            rand = random.randrange(index)
            if rand < number_wanted:
                retained[random.randrange(number_wanted)] = fastq
    
    with open(result_file, "w") as outf:
        for s in retained:
            s.write_to_file(outf)

