from os import listdir
from os.path import isfile, join
import re
import fileinput
import sys

mypath = '.'
datafiles = [f for f in listdir(mypath) 
             if isfile(join(mypath, f)) and f.startswith('pagecounts')]

rex = re.compile(r'pagecounts-(\d{4})(\d{2})(\d{2})-.*')

for datafile in datafiles:
    print('Handling file {}'.format(datafile))
    s = rex.fullmatch(datafile)
    datetime = '-'.join([s.group(i) for i in range(1, 4)])
    with fileinput.input(datafile, inplace=True) as f:
            for line in f:
                sys.stdout.write('{} {}'.format(datetime, line))
