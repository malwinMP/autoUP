'''
Created on 17-04-2012

@author: Malwin
'''

import ConfigParser


def parse():
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(open('config'))
    cfg_dict = {}
    cfg_dict['username'] = config.get('Imagebam user', 'username')
    cfg_dict['password'] = config.get('Imagebam user', 'password')
    # [Imagebam addresses] section
    cfg_dict['url_login'] = config.get('Imagebam addresses', 'url_login')
    cfg_dict['url_upload'] = config.get('Imagebam addresses', 'url_upload')
    # [Settings] section
    cfg_dict['screen_amount'] = config.getint('Settings', 'screen_amount_default')
    cfg_dict['thumb_size'] = config.getint('Settings', 'thumb_size_default')
    cfg_dict['screen_path_default'] = config.get('Settings', 'screen_path_default')
    cfg_dict['upload'] = config.getboolean('Settings', 'upload')
    cfg_dict['clean'] = config.getboolean('Settings', 'clean')
    # [Imagebam options] section
    cfg_dict['thumb_s_allowed'] = config.get('Imagebam options', 'thumb_s_allowed').split(',')
    # end of cfg
    cfg_dict['s_path'] = True
    return cfg_dict