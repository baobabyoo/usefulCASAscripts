import sys
sys.path.append('./')
from linebasecasa import *

thesteps = []
step_title = {
              0: 'Collect file names',
              1: 'Imaging',
              2: 'FITS output',
              3: 'moving over files'
             }

try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps


# Not actually producing images in debug mode -------------------
debug = False
# ---------------------------------------------------------------


# setting up which sources and spectral line to image -----------
fieldtoimage = [
                'G33.92+0.11'
               ]

linename     = 'ch3cn_12to11_K0'

datapath     = '../linedata/' 
mspath       = datapath + linename
# ---------------------------------------------------------------


# setting up imaging parameters ---------------------------------
spw          = '0'
imsize       = [3000, 3000]
cell         = '0.02arcsec'
stokes       = 'I'
uvtaper      = []  # example ['0.25arcsec']
robust       = 2.0
niter        = 1000000
pblimit      = 0.05
interactive  = True
threshold    = '3.0mJy'
# ---------------------------------------------------------------


# collecting visibility filenames
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  vis = os.listdir( mspath )
  print ( "Visibilities to image" )

  for vis_id in range( len(vis) ):
     print ( vis[vis_id] )
     vis[vis_id] = datapath + linename + '/' + vis[vis_id]


# Imaging
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


  # creating an directory to store line data ---------
  if (debug == False):
     os.system('rm -rf %s'%linename)  

  os.mkdir('./%s'%linename)
  # --------------------------------------------------



  # imaging ------------------------------------------
  if (debug == False):
     print ( "Start imaging %s"%linename)

     for field in fieldtoimage:

        imagename = field + '.' + linename
        os.system(' rm -rf ' + imagename + '*')

        tclean(
               vis = vis,
               selectdata = True,
                  field   = field,
                  spw     = spw,
               datacolumn = 'data',
               imagename  = imagename,
               imsize     = imsize,
               cell       = cell,
               stokes     = stokes,
               projection = 'SIN',
               specmode   = 'cubedata',
                  nchan         = -1,
                  start         = 0,
                  width         = 1,                  
                  outframe      = 'LSRK',
                  veltype       = 'radio',
                  interpolation = 'nearest',
               gridder       = 'mosaic',
                  pblimit    = 0.05,
               restfreq      = freqdict[linename]+'GHz',
               deconvolver   = 'clark',
               weighting     = 'briggs',
                  robust     = robust,
                  uvtaper    = uvtaper,
               niter         = niter,
               interactive   = interactive,
               threshold     = threshold,
               pbcor         = True
              )

  # --------------------------------------------------


mystep = 2
if(mystep in thesteps):

  if (debug == False):
     exportfits(
                imagename = imagename + '.image',
                fitsimage = imagename + '.image.fits',
                overwrite = True
               )

     exportfits(
                imagename = imagename + '.pb',
                fitsimage = imagename + '.pb.fits',
                overwrite = True
               )

     exportfits(
                imagename = imagename + '.image.pbcor',
                fitsimage = imagename + '.image.pbcor.fits',
                overwrite = True
               )


mystep = 3
if(mystep in thesteps):

  if (debug == False):
    if ( os.path.exists('./fits_images') == False ):
       os.mkdir('./%s'%'fits_images')

  os.system( 'mv ' + './*.fits ' + './fits_images/')
  os.system( 'mv ' + imagename + '* ' + linename )


