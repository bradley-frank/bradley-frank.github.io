from ConfigParser import SafeConfigParser
config_parser = SafeConfigParser()
from optparse import OptionParser
import sys
#from casa import cl
from taskinit import *
from exportfits_cli import exportfits_cli as exportfits

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

parser.add_option("--settings", "-s", type = 'string', dest = 'settings', default=None, 
    help = "Settings file to make the dummy image.[None]");
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

def get_sources(configfile=None, section='sources'):
    config_parser = SafeConfigParser()
    config_parser.read(configfile)
    #params = Bunch()
    ra = []
    dec = []
    flux = []
    bmaj = []
    bmin = []
    bpa = []
    for p in config_parser.items(section):
        ra.append(p[1].split(',')[0])
        dec.append(p[1].split(',')[1])
        flux.append(p[1].split(',')[2])
        bmaj.append(p[1].split(',')[3])
        bmin.append(p[1].split(',')[4])
        bpa.append(p[1].split(',')[5])
    return ra, dec, flux, bmaj, bmin, bpa
        
def make_model(settings_file=None):
    if settings_file==None:
        print "Please provide settings file."
        sys.exit(0)
    else:
        settings = get_params('dummy-settings.txt', 'observation')
        sources = get_sources('dummy-settings.txt')

        observation = get_params("dummy-settings.txt", 'observation')

        cl.done()

        ra, dec, flux, bmaj, bmin, bpa = get_sources("dummy-settings.txt")

        for i in range(0,len(ra)):
            direction = "J2000 "+ra[i]+" "+dec[i]
            cl.addcomponent(dir=direction, flux=float(flux[i]), freq='1420MHz', shape="Gaussian",
                           majoraxis=str(bmaj[i])+'arcmin', minoraxis=str(bmin[i])+'arcmin',
                           positionangle=str(bpa[i])+'deg')


        ia.fromshape(observation.filename+'.im',
                     [int(observation.imsize),int(observation.imsize), 1, 1], 
                     overwrite=True)

        cs=ia.coordsys()
        cs.setunits(['rad','rad','','Hz'])
        cell_rad=qa.convert(qa.quantity(observation.pixelsize),"rad")['value']

        cs.setincrement([-cell_rad,cell_rad],'direction')

        cs.setreferencevalue([qa.convert(observation.ra,'rad')['value'],
                              qa.convert(observation.dec,'rad')['value']],
                              type="direction")

        cs.setreferencevalue(observation.reffreq,'spectral')
        cs.setincrement(observation.freqint,'spectral')
        ia.setcoordsys(cs.torecord())
        ia.setbrightnessunit("Jy/pixel")
        ia.modify(cl.torecord(),subtract=False)

        #exportfits(imagename=observation.filename+'.im',fitsimage=observation.filename+'.fits',overwrite=True)
        exportfits(imagename=observation.filename+'.im',fitsimage=observation.filename+'.fits',
                   velocity=False,optical=False,bitpix=-32,minpix=0,maxpix=-1,
                   overwrite=True,dropstokes=False,stokeslast=True,history=True,dropdeg=False) 
        
if __name__=="__main__":
    if len(sys.argv)==1: 
        parser.print_help()
        dummy = sys.exit(0)
    else:
        make_model(settings_file=options.settings)