import argparse
import csv
import re
import textwrap

parser = argparse.ArgumentParser(
    description='Read CSV output from STIGViewer and output to a YaML file as comments for Ansible')
parser.add_argument('infile', type=argparse.FileType(mode='r', encoding='UTF-8'),
                   help='The CSV file to read')
parser.add_argument('outfile', type=argparse.FileType(mode='w', encoding='UTF-8'),
                   help='The YaML file to write')
args = parser.parse_args()

reader = csv.reader(args.infile)
rows = []
for row in reader:
    rows.append(row)

# consume the classification lines (first & last)
rows = rows[1:-1]
header_row = rows[0]
rows = rows[1:]

for row in rows:
    for i in range(len(header_row)):
        field = header_row[i] + ': ' + row[i]
        field = re.sub('\n', '\n# ', field)
        #lines = [re.sub('\n\n', '\n#\n# ', x) for x in lines]
        args.outfile.write('# ' + field + '\n')
    args.outfile.write('\n\n')

args.infile.close()
args.outfile.close()
