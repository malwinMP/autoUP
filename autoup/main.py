'''
Created on 17-04-2012

@author: Malwin
'''

import sys
import getopt
from src import screen_maker
from src import cfg



class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        cfg_dict = cfg.parse()
        sm = screen_maker
        try:
            opts, args = getopt.getopt(argv[1:], "i:t:uca:hs", ["help"])
            print args
        except getopt.error, msg:
            raise Usage(msg)
        for o, a in opts:
            if o == '-i':
                cfg_dict['path'] = a
            elif o == '-t':
                if a in cfg_dict['thumb_s_allowed']:
                    cfg_dict['thumb_size'] = a
            elif o == '-u':
                cfg_dict['upload'] = True
            elif o == '-c':
                cfg_dict['clean'] = True
            elif o == '-a':
                cfg_dict['screen_amount'] = int(a)
            elif o == '-s':
                pass
                #s_path = False # not implemented yet!            
        path, filename = sm.prepare_path(cfg_dict['path'])
        sm.process(path, filename, cfg_dict)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())