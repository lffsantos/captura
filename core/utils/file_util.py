import csv
import os

__author__ = 'lucas'


def has_header(file, header):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if list(row) != header:
                raise ValueError('invalid header')

            return True


def add_header(file, header):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)


def create_file(file, header):
    if not os.path.exists(file):
        add_header(file, header)
    else:
        if not has_header(file, header):
            add_header(file, header)


