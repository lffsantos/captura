import csv

__author__ = 'lucas'


def has_header(file, header):
    try:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if list(row) != header:
                    raise ValueError('invalid header')

                return True
    except FileNotFoundError:
        raise FileNotFoundError()


def add_header(file, header):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)


def create_file(file, header):
    if not has_header(file, header):
        add_header(file, header)

