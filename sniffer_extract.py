"""Total Phase A2B Bus Monitor Log Extraction.

Usage: 
    sniffer_extract [options]

Options:
  -h --help                       Show this screen.
  --version                       Show version.
  --logs_dir=<str>                Directory containing log directories [default: ./]
  --boardno=<str>                 board serial no traced on log directories [default: *]
  --slave0=<str>                  LPS or PPS to specify slave0 used [default: (LPS|PPS)]
  --expno=<str>                   experiment serial no to extract logs. * to extract all experiments [default: .*]
  --dir=<bool>                    False if logs_dir contain log files [default: True]
  --verbosity=<level>               Verbosity level of message [default: low]

Arguments:
    level: high
           low
"""
import os
import re
import pandas as pd
from docopt import docopt
import itertools


def extract_logs (logs_dir=None, boardno=None, slave0=None, expno=None, dir=None, verbosity=None):
    assert logs_dir!=None, "logs_dir is NONE"
    assert boardno!=None, "boardno is NONE"
    assert slave0!=None, "slave0 is NONE"
    assert expno!=None, "exp no is NONE"
    srch_str = boardno + "_" + expno + "_" + slave0
    print (srch_str)
    for name in list(filter(lambda x: (os.path.isdir(x) and re.match(srch_str,x)) , os.listdir(logs_dir))):
        files = os.path.join(logs_dir,name)
        cnt = 0
        for file in os.listdir(files):
            cnt += 1
            if (os.path.isfile(os.path.join(files,file))):
                df = pd.read_csv(os.path.join(files,file), keep_default_na=False)
                re_error_str = "Error: DSMISSED\[([0-9]*)\] DSHDCNTERR\[([0-9]*)\] DSCRCERR\[([0-9]*)\] USMISSED\[([0-9]*)\] USHDCNTERR\[([0-9]*)\] USCRCERR\[([0-9]*)\] USICRCERR\[([0-9]*)\].?"
                df_extract = df[df['text'].str.startswith('Error')]
                error_cnt = dict([('dsmissed', 0), ('dshdcnterr', 0), ('dscrcerr', 0), ('usmissed', 0), ('ushdcnterr', 0), ('uscrcerr', 0), ('usicrcerr', 0)])
                time_st = dict([('dsmissed', ''), ('dshdcnterr', ''), ('dscrcerr', ''), ('usmissed', ''), ('ushdcnterr', ''), ('uscrcerr', ''), ('usicrcerr', '')])
                for (timest,err) in (zip(df_extract['timestamp'].tolist(),df_extract['text'].tolist())) :
                    err_extract = re.match(re_error_str,err)
                    if (error_cnt['dsmissed']<int(err_extract.group(1))):
                        error_cnt['dsmissed'] = int(err_extract.group(1))
                        time_st['dsmissed'] = timest
                    if (error_cnt['dshdcnterr']<int(err_extract.group(2))):
                        error_cnt['dshdcnterr'] = int(err_extract.group(2))
                        time_st['dshdcnterr'] = timest
                    if (error_cnt['dscrcerr']<int(err_extract.group(3))):
                        error_cnt['dscrcerr'] = int(err_extract.group(3))
                        time_st['dscrcerr'] = timest
                    if (error_cnt['usmissed']<int(err_extract.group(4))):
                        error_cnt['usmissed'] = int(err_extract.group(4))
                        time_st['usmissed'] = timest
                    if (error_cnt['ushdcnterr']<int(err_extract.group(5))):
                        error_cnt['ushdcnterr'] = int(err_extract.group(5))
                        time_st['ushdcnterr'] = timest
                    if (error_cnt['uscrcerr']<int(err_extract.group(6))):
                        error_cnt['uscrcerr'] = int(err_extract.group(6))
                        time_st['uscrcerr'] = timest
                    if (error_cnt['usicrcerr']<int(err_extract.group(7))):
                        error_cnt['usicrcerr'] = int(err_extract.group(7))
                        time_st['usicrcerr'] = timest
                if verbosity=='low':
                    print ('{0}{1}   <>   DS: {2:>10}   <>   US: {3:>10}'.format(name, str(cnt), str(error_cnt['dsmissed']), str(error_cnt['usmissed'])))
                if verbosity=='high':
                    print ('{0}{1}   <>   TS: {2:>10}   <>   DS: {3:>10}   <>   TS: {4:>10}   <>   US: {5:>10}'.format(name, str(cnt), time_st['dsmissed'], str(error_cnt['dsmissed']), time_st['usmissed'], str(error_cnt['usmissed'])))

def main():
    args = docopt(__doc__, version='Total Phase A2B Bus Monitor Log Extraction v1.0 release.')
    extract_logs (logs_dir=args['--logs_dir'], boardno=args['--boardno'], slave0=args['--slave0'], expno=args['--expno'], verbosity=args['--verbosity'])
if __name__ == '__main__':
    main()