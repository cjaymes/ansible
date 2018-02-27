import argparse
import csv
import os
import re

parser = argparse.ArgumentParser(
    description='Read CSV output from STIGViewer and output to a YaML file as comments for Ansible')
parser.add_argument('mode', choices=['tasks', 'defaults'],
    help='Type of file to generate: tasks, defaults')
parser.add_argument('infile',
    type=argparse.FileType(mode='r', encoding='UTF-8'),
    help='The CSV file to read')
parser.add_argument('outfile',
    type=argparse.FileType(mode='w', encoding='UTF-8'),
    help='The YaML file to write')
args = parser.parse_args()

file_name = os.path.basename(args.infile.name)
# strip off the ext
file_name = os.path.splitext(file_name)[0]
file_name = re.sub('[- .]', '_', file_name.lower())

# pre-process csv lines
reader = csv.reader(args.infile)
rows = []
for row in reader:
    rows.append(row)
# consume the classification lines (first & last)
rows = rows[1:-1]
# save the header row, but don't output
header_row = rows[0]
rows = rows[1:]

for row in rows:
    vuln_id = re.sub('[- .]', '_', row[0].lower())
    vuln_id = 'stig_' + file_name + '_' + vuln_id
    if args.mode == 'tasks':
        for i in range(len(header_row)):
            field = header_row[i] + ': ' + row[i]
            field = re.sub('\n', '\n# ', field)
            #lines = [re.sub('\n\n', '\n#\n# ', x) for x in lines]
            args.outfile.write('# ' + field + '\n')
        args.outfile.write('- name: ' + vuln_id + '\n')
        args.outfile.write('  when: not ' + vuln_id + '_skip\n')
        args.outfile.write('\n\n')
    elif args.mode == 'defaults':
        args.outfile.write(vuln_id + '_skip: False\n')


args.infile.close()
args.outfile.close()
