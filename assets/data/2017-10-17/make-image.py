from ConfigParser import SafeConfigParser
config_parser = SafeConfigParser()
from optparse import OptionParser
import sys
#from casa import cl
from taskinit import *
from clean_cli import clean_cli as clean
from exportfits_cli import exportfits_cli as exportfits

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

def do_clean(settings_file=None):
    params = get_params(configfile=settings_file, section='clean')
    print params.imagename
    clean(vis=params.vis, imagename=params.imagename,
          mode=params.mode, niter=int(params.niter),
          threshold=params.threshold, psfmode=params.psfmode,
          imagermode=params.imagermode, ftmachine=params.ftmachine,
          imsize=int(params.imsize), cell=params.cell, stokes=params.stokes,
          weighting=params.weighting, robust=float(params.robust))
    im = params.imagename+'.image'
    exportfits(imagename=im,
               fitsimage=im+'.fits',
               overwrite=True)
    im = params.imagename+'.psf'
    exportfits(imagename=im,
               fitsimage=im+'.fits',
               overwrite=True)
    

if __name__=="__main__":
    if len(sys.argv)==1: 
        parser.print_help()
        dummy = sys.exit(0)
    else:
        do_clean(settings_file=options.settings)
    
               
               