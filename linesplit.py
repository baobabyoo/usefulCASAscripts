# Script for splitting line data to the present working directory
"""
   Purpose:
      Splitting spectral line data from the calibrated,
      uv continuum subtracted CASA ms.


   Version:
      v0: Created by Baobab Liu on 2017Oct16. 
          This version is based on CASA 5.0.0-218

   Usage:
      Include the line rest frequencies in the file linebasecasa.py.
      Then edit the Section "Spectral line table" to setup the starting
      channel, channel width, and number of channels for individual lines.
      It is possible to make identical setup using loops.


   Problem:
      When a line is detected in two spectral windows, the present version
      cannot make the sensible decision.

"""
from linebasecasa import *  # importing line database

# Calibration

thesteps = []
step_title = {
               0: 'Split spectral line data',
              }


try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps

##### Spectral line table ##########################
nchandict = {}
startdict = {}
widthdict = {}

# the specified lines to be splitted from the measurement sets
linetosplit  = [
                # 'h30alpha', 
                # 'he30alpha'
                'c30alpha',
                # '13cs_5to4',
               ]

molecular = ['13cs_5to4']


rrl = ['h30alpha', 'he30alpha', 'c30alpha']
for line in rrl:
   nchandict[line] =  140
   startdict[line] =  '8.0km/s'
   widthdict[line] =  '1.4km/s'


fieldtosplit = [
                'G33.92+0.11'
               ]
####################################################


##### DATA I/O #####################################
pathdict    = {}
visdict     = {}

# ACA data taken in cycle-1
DATApath = '/scigarfs/opsw/work/hlu/DATA'
subpath_cycle1aca = '/G33p92/2012.1.00387.S/cal_2017Oct/7m/calibrated_ms/'

pathdict['aca_ms1'] = DATApath + subpath_cycle1aca
pathdict['aca_ms2'] = DATApath + subpath_cycle1aca
pathdict['aca_ms3'] = DATApath + subpath_cycle1aca
pathdict['aca_ms4'] = DATApath + subpath_cycle1aca

visdict['aca_ms1'] = 'uid___A002_X8081ba_X2f08.ms.split.cal.contsub'
visdict['aca_ms2'] = 'uid___A002_X8081ba_X32b1.ms.split.cal.contsub'
visdict['aca_ms3'] = 'uid___A002_X8081ba_X3635.ms.split.cal.contsub'
visdict['aca_ms4'] = 'uid___A002_X8081ba_X55f.ms.split.cal.contsub'


# main array data taken in cycle-1
DATApath = '/scigarfs/opsw/work/hlu/DATA'
subpath_cycle112m = '/G33p92/2012.1.00387.S/cal_2017Oct/12m/calibrated_ms/'

pathdict['12m_ms1'] = DATApath + subpath_cycle112m 
pathdict['12m_ms2'] = DATApath + subpath_cycle112m

visdict['12m_ms1'] = 'uid___A002_X80199b_Xb2.ms.split.cal.contsub'
visdict['12m_ms2'] = 'uid___A002_X8081ba_X31e3.ms.split.cal.contsub'


# main array data taken in cycle-2
DATApath = '/scigarfs/opsw/work/hlu/DATA'
subpath_cycle412m = '/G33p92/2016.1.00362.S/cal/calibrated_ms/'

pathdict['12m_ms3'] = DATApath + subpath_cycle412m
pathdict['12m_ms4'] = DATApath + subpath_cycle412m

visdict['12m_ms3'] = 'uid___A002_Xc384d6_X192d.ms.split.cal.contsub'
visdict['12m_ms4'] = 'uid___A002_Xc384d6_X1fb8.ms.split.cal.contsub'


vistosplit = [
              'aca_ms1', 
              'aca_ms2', 
              'aca_ms3', 
              'aca_ms4',
              '12m_ms1',
              '12m_ms2',
              '12m_ms3',
              '12m_ms4'
             ]

###################################################








### Stokes  clean images of the polarization calibrator
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


  for line in linetosplit:
     for field in fieldtosplit:

        print ( "###########  Splitting :", line, 'at', freqdict[line]+'GHz', ", source: ", field, "###############")
        print ( "parameters (start, width, nchan) :", startdict[line], widthdict[line], nchandict[line])

        # creating a directory for storing the splitted line data
        os.system('rm -rf %s'%line)
        os.mkdir('./%s'%line)

        for vis in vistosplit:

           # Deciding in which spw is the selected line (without considering doppler velocity yet)
           ms.open(pathdict[vis] + visdict[vis])  

           # get all spectral window IDs other than those associated with square law detectors  
           spwInfo = ms.getspectralwindowinfo()
           # print ( spwInfo )
           for window in spwInfo:
              # print ( spwInfo[window]['SpectralWindowId'], "\n" )
              # print ( spwInfo[window]['Chan1Freq'] )  # Hz
              # print ( spwInfo[window]['TotalWidth'] ) # Hz
              # print ( spwInfo[window]['ChanWidth']  ) # Hz
              # print ( "\n" )

              linefreq = float( freqdict[line] ) * 1e9
              if ( spwInfo[window]['ChanWidth'] > 0.0 ):
                 bandlow = spwInfo[window]['Chan1Freq']
                 bandup  = spwInfo[window]['Chan1Freq'] + spwInfo[window]['TotalWidth']
              else:
                 bandlow = spwInfo[window]['Chan1Freq']
                 bandup  = spwInfo[window]['Chan1Freq'] + spwInfo[window]['TotalWidth']

              if (
                  ( linefreq > bandlow )
                   and
                  ( linefreq < bandup )
                 ):
                 yourspw = spwInfo[window]['SpectralWindowId']
                 print ( line, ' is in spectral window :', yourspw )

           ms.close()


           # defining output filename
           outputvis = visdict[vis] + '.' + line
           print ("Splitting visibility: ", outputvis)

           os.system('rm -rf ' + outputvis )

           # do the actual line splitting
           mstransform(
              vis       = pathdict[vis] + visdict[vis],
              outputvis = outputvis,
              field     = field,
              spw       = str(yourspw),
              correlation = '',
              datacolumn  = 'data',
              keepflags   = True,
              regridms    = True,
                  mode  = 'velocity',
                  nchan = nchandict[line],
                  start = startdict[line],
                  width = widthdict[line],
                  # nspw  = 1,
                  interpolation = 'linear',
                  restfreq      = freqdict[line]+'GHz',
                  outframe      = 'LSRK',
                  veltype       = 'radio',
              docallib     = False,
              douvcontsub = False
              )

           os.system('mv ' + outputvis + ' ./%s/'%line)
