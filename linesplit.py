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
import importlib            # the lib to permit reloading module
import os.path
import numpy as np


# Calibration

thesteps = []
step_title = {
               0: 'Split spectral line data',
              }

debugging = False


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
                # 'c30alpha',
                '13cs_5to4',
                # 'sio_5to4'
               ]

narrowline = ['13cs_5to4']
for line in narrowline:
   nchandict[line] =  80
   startdict[line] =  '100.0 km/s'
   widthdict[line] =  '0.17' # km/s


broadline  = ['sio_5to4']
for line in broadline:
   nchandict[line] =  140
   startdict[line] =  '8.0km/s'
   widthdict[line] =  '1.4' # km/s


rrl = ['h30alpha', 'he30alpha', 'c30alpha']
for line in rrl:
   nchandict[line] =  140
   startdict[line] =  '8.0km/s'
   widthdict[line] =  '1.4' # km/s


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


# main array data taken in cycle-4
DATApath = '/scigarfs/opsw/work/hlu/DATA'
subpath_cycle412m = '/G33p92/2016.1.00362.S/cal/calibrated_ms/'

pathdict['12m_ms3'] = DATApath + subpath_cycle412m
pathdict['12m_ms4'] = DATApath + subpath_cycle412m

visdict['12m_ms3'] = 'uid___A002_Xc384d6_X192d.ms.split.cal.contsub'
visdict['12m_ms4'] = 'uid___A002_Xc384d6_X1fb8.ms.split.cal.contsub'


# a black list to describe which spw of a certain ms file should not be readed
blacklist_file = 'g33p92_blacklist.txt'

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






# a function to pick the appropriate spectral window to split
def spwpick(msname, restfreq, velwidth=0.0, maskedspw=[]):
   """
   Purpose:
      From the input ms, based on the specified rest frequency,
      specify the spectral window to be split.

      Need to allow setting a black list.
      When a desired velwidth is not specified, just avoid picking
      spectral window in the black list. When a desired velwidth is specified,
      avoid the black list and pick the spectal window of which the channel width
      is less than the desired velwidth.


   Input:
      manam [string]: the name (or path+name) of the CASA measurement set to be split.
      restfreq [float]: rest frequency in unit of Hz.
      velwidth [float]: channel width in km/s (optional)
      maskedspw [string array]: an array like ['0','1','2'] of masked spectral windows of the
                                input CASA measurement set


   Return:
      yourspw [integer]: the spectral window ID to be split.
                         return -1 if the line is not covered by any spw

   """

   # physical constants
   c_kmpers = 299792.458  # light speed in km/s

   # evaluate the corresponding requested channel width in Frequency (in Hz)
   velwidth_f = float(velwidth)
   req_Hzwidth = restfreq * ( 
                             float(velwidth) / c_kmpers 
                            ) 

   # Deciding in which spw is the selected line (without considering doppler velocity yet)
   ms.open(msname)

   # get all spectral window IDs other than those associated with square law detectors  
   spwInfo = ms.getspectralwindowinfo()

   # make the black list here by editing spwInfo:
   # print ( spwInfo )

   # initialize return
   yourspw    = -1
   spwHzwidth = 0.0

   for window in spwInfo:
      if ( window not in maskedspw ):
      # print ( spwInfo[window]['SpectralWindowId'], "\n" )
      # print ( spwInfo[window]['Chan1Freq'] )  # Hz
      # print ( spwInfo[window]['TotalWidth'] ) # Hz
      # print ( spwInfo[window]['ChanWidth']  ) # Hz
      # print ( "\n" )


         if ( spwInfo[window]['ChanWidth'] > 0.0 ):
            bandlow = spwInfo[window]['Chan1Freq']
            bandup  = spwInfo[window]['Chan1Freq'] + spwInfo[window]['TotalWidth']
         else:
            bandlow = spwInfo[window]['Chan1Freq'] - spwInfo[window]['TotalWidth']
            bandup  = spwInfo[window]['Chan1Freq']

         if (
             ( restfreq > bandlow )
             and
             ( restfreq < bandup )
            ):


            # check whether a desired velocity channel width is specified as an input
            if ( req_Hzwidth != 0.0 ):

               if ( req_Hzwidth > spwInfo[window]['ChanWidth'] ):

                  # if a spectral window has been assigned previously in the loop
                  if ( spwHzwidth != 0.0 ):

                     # update the spectral window selection to the better velocity resolution one
                     if (
                          spwHzwidth > spwInfo[window]['ChanWidth']
                        ):
                        yourspw = spwInfo[window]['SpectralWindowId']

                  else:
                     yourspw = spwInfo[window]['SpectralWindowId']
                     spwHzwidth = spwInfo[window]['ChanWidth']

            else:
               yourspw = spwInfo[window]['SpectralWindowId']

   ms.close()
   return yourspw








### Stokes  clean images of the polarization calibrator
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


   # read blacklist file
  num_blackitems = 0
  if ( os.path.isfile('./' + blacklist_file) == True ):
     print ( 'Black list file exist' )
     blacklistvalid = True

     try:
       temp1, temp2 = np.loadtxt(
                              blacklist_file,
                              dtype    = 'string',
                              comments = '#',
                              skiprows = 0,
                              usecols  = (0, 1),
                              unpack   = True
                             )
     except: 
        print ( "Black list file contains no valid statements" )
        blacklistvalid = False

     if ( blacklistvalid == True ):
        # to avoid the filename to be broken down into a list when there is only one item in the blacklist
        num_blackitems = len( temp2 ) 

        if ( num_blackitems == 1 ):
           blackspw    = []
           blackmsfile = []
           blackspw.append(temp2)
           blackmsfile.append(temp1)
        else:
           blackspw    = temp2
           blackmsfile = temp1
           del temp2
           del temp1 

        for blackid in range( num_blackitems ):
           print ("black listed spw ", blackspw[blackid], ' for ', blackmsfile[blackid])



  for line in linetosplit:
     for field in fieldtosplit:

        print ( "###########  Splitting :", line, 'at', freqdict[line]+'GHz', ", source: ", field, "###############")
        print ( "parameters (start, width, nchan) :", startdict[line], widthdict[line]+'km/s', nchandict[line])

        # creating a directory for storing the splitted line data
        os.system('rm -rf %s'%line)
        os.mkdir('./%s'%line)

        for vis in vistosplit:

           # obtain the black listed spws
           num_maskedspw = 0

           if ( num_blackitems != 0 ):

              maskedspw = []
              for blackid in range( num_blackitems ):
                 if (  blackmsfile[blackid] == visdict[vis]):
                    maskedspw.append( blackspw[blackid] )
              num_maskedspw = len( maskedspw )

           # picking the right spectral window
           msname   = pathdict[vis] + visdict[vis]
           linefreq = float( freqdict[line] ) * 1e9

           if ( num_maskedspw == 0 ):           
              yourspw = spwpick(msname, linefreq, widthdict[line])
           else:
              yourspw = spwpick(msname, linefreq, widthdict[line], maskedspw)


           if (
               yourspw != -1 
              ):
              print ( line, ' is in spectral window :', yourspw )

              # defining output filename
              outputvis = visdict[vis] + '.' + line
              print ("Splitting visibility: ", outputvis)

              os.system('rm -rf ' + outputvis )

              if ( debugging != True):

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
                        width = widthdict[line] + 'km/s',
                        # nspw  = 1,
                        interpolation = 'linear',
                        restfreq      = freqdict[line]+'GHz',
                        outframe      = 'LSRK',
                        veltype       = 'radio',
                    docallib     = False,
                 douvcontsub = False
                 )

                 os.system('mv ' + outputvis + ' ./%s/'%line)

           else:
              print ('Warning !:' + line, ' is not covered in ' + visdict[vis])

