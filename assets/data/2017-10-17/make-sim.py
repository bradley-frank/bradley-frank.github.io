from ConfigParser import SafeConfigParser
config_parser = SafeConfigParser()
from optparse import OptionParser
import sys
#from casa import cl
from taskinit import *
from simobserve_cli import simobserve_cli as simobserve

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

parser.add_option("--settings", "-s", type = 'string', dest = 'settings', default=None, 
    help = "Settings file to make the observation.[None]");
(options, args) = parser.parse_args() 

class Bunch:
    '''
    Dummy container for the parameters.
    '''
    def __init__(self, **kwds): 
            self.__dict__.update(kwds)

def get_params(configfile=None, section=None):
    if configfile!=None:
        config_parser = SafeConfigParser()
        config_parser.read(configfile)
        params = Bunch()
        for p in config_parser.items(section):
            setattr(params, p[0], p[1])
    else:
        print "Need settings file!"
    return params

def make_pointing_file(settings_file=None):
    observation = get_params(configfile=options.settings, section='observation')
    header = "#Epoch\tRA\tDEC\tTIME[sec]\n"
    direction = "J2000"+"\t"+observation.ra+"\t"+observation.dec+"\t"+observation.integration+"\n"
    f = open('pointing.txt', 'w')
    f.writelines(header)
    f.writelines(direction)
    f.close()

def observe(settings_file=None):
    observation = get_params(configfile=options.settings, section='observation')
    simobserve(project=observation.project, skymodel=observation.skymodel,
               setpointings=False, ptgfile='pointing.txt',
               antennalist=observation.config, totaltime=observation.totaltime,
               overwrite=True,graphics='none')
    
if __name__=="__main__":
    if len(sys.argv)==1: 
        parser.print_help()
        dummy = sys.exit(0)
    else:
        make_pointing_file(settings_file=options.settings)
        observe(settings_file=options.settings)
    
