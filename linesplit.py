# Script for splitting line data to the present working directory
"""
   Purpose:
      Splitting spectral line data from the calibrated,
      uv continuum subtracted CASA ms.


   Version:
      v0: Created by Baobab Liu on 2017Oct16. 
          This version is based on CASA 5.0.0-218
      v0.1: Updated on 2017Oct28. Switched over to CASA 5.1.1

   Usage:
      Include the line rest frequencies in the file linebasecasa.py.
      Then edit the Section "Spectral line table" to setup the starting
      channel, channel width, and number of channels for individual lines.
      It is possible to make identical setup using loops.


   Problem:
      When a line is detected in two spectral windows, the present version
      cannot make the sensible decision.

"""
import sys
sys.path.append('./')

from linebasecasa import *  # importing line database
import importlib            # the lib to permit reloading module
import os.path
import numpy as np
import math

# Calibration

thesteps = []
step_title = {
               0: 'Split spectral line data',
              }

debugging = True


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
vlsrdict  = {}
phaserefdict = {}

# the specified lines to be splitted from the measurement sets
linetosplit  = [
                # done splitting
                 'h30alpha', 
                 'he30alpha',
                 'c30alpha',
                 '13cs_5to4',
                 'sio_5to4',
                # to be splitted
                'c-c3h2_3l3c0to2l2c1',
                'ccd_N3to2_J7o2to5o2_F9o2to7o2',
                'ccd_N3to2_J7o2to5o2_F7o2to5o2',
                'ccd_N3to2_J5o2to3o2_F7o2to5o2',
                'ccd_N3to2_J5o2to3o2_F3o2to1o2',
                'ch3cho_11l1c10to10l1c9_E',
                'ch3cho_11l1c10to10l1c9_A',
                'hdcs_7l0c7to6l0c6',
                'hdcs_7l2c6to6l2c5',
                'hdcs_7l2c5to6l2c4',
                'h2s_2l2c0to2l1c1',
                'ch3oh_5l1c4to4l2c2',
                'dcn_3to2',
                '13cn_N2to1_J3o2to3o2_Fone1to1_F2to1',
                '13cn_N2to1_J3o2to3o2_Fone1to1_F2to2',
                '13cn_N2to1_J3o2to1o2_Fone1to0_F0to1',
                '13cn_N2to1_J3o2to1o2_Fone1to0_F1to1',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F2to2',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F1to1',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F1to0',
                '13cn_N2to1_J5o2to3o2_Fone2to2_F2to2',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F2to1',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F3to2',
                '13cn_N2to1_J3o2to1o2_Fone1to0_F2to1',
                '13cn_N2to1_J5o2to3o2_Fone2to2_F3to3',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F3to2',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F2to1',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F2to2',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F1to1',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F4to3',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F2to1',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F2to2',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F3to3',
                't-c2h5oh_5l3c3-4l2c2',
                'c-hccch_6l1c6-5l0c5',
                'c-hccch_5l1c4-4l2c3',
                'ch3cn_12to11_K4',
                'ch3cn_12to11_K3',
                'ch3cn_12to11_K2',
                'ch3cn_12to11_K1',
                'ch3cn_12to11_K0',
                'ocs_19to18',
                'n2dp_3to2',
                'ch3och3_13l0c13to12l1c12_EE',
                'h2c34S_7l1c7to6l1c6'
               ]


narrowline = [
              '13cs_5to4',
              'ch3cn_12to11_K4',
              'ch3cn_12to11_K3',
              'ch3cn_12to11_K2',
              'ch3cn_12to11_K1',
              'ch3cn_12to11_K0',
              'n2dp_3to2'  # may need to do this one again. not sure if the velocity range of spw 0 is sufficient
             ]

broadline  = [
              'sio_5to4'
             ]

narrowline_coarse  = [
                'c-c3h2_3l3c0to2l2c1',
                'ccd_N3to2_J7o2to5o2_F9o2to7o2',
                'ccd_N3to2_J7o2to5o2_F7o2to5o2',
                'ccd_N3to2_J5o2to3o2_F7o2to5o2',
                'ccd_N3to2_J5o2to3o2_F3o2to1o2',
                'ch3cho_11l1c10to10l1c9_E',
                'ch3cho_11l1c10to10l1c9_A',
                'hdcs_7l0c7to6l0c6',
                'hdcs_7l2c6to6l2c5',
                'hdcs_7l2c5to6l2c4',
                'h2s_2l2c0to2l1c1',
                'ch3oh_5l1c4to4l2c2',
                'dcn_3to2',
                '13cn_N2to1_J3o2to3o2_Fone1to1_F2to1',
                '13cn_N2to1_J3o2to3o2_Fone1to1_F2to2',
                '13cn_N2to1_J3o2to1o2_Fone1to0_F0to1',
                '13cn_N2to1_J3o2to1o2_Fone1to0_F1to1',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F2to2',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F1to1',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F1to0',
                '13cn_N2to1_J5o2to3o2_Fone2to2_F2to2',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F2to1',
                '13cn_N2to1_J3o2to1o2_Fone2to1_F3to2',
                '13cn_N2to1_J3o2to1o2_Fone1to0_F2to1',
                '13cn_N2to1_J5o2to3o2_Fone2to2_F3to3',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F3to2',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F2to1',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F2to2',
                '13cn_N2to1_J5o2to3o2_Fone2to1_F1to1',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F4to3',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F2to1',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F2to2',
                '13cn_N2to1_J5o2to3o2_Fone3to2_F3to3',
                't-c2h5oh_5l3c3-4l2c2',
                'c-hccch_6l1c6-5l0c5',
                'c-hccch_5l1c4-4l2c3',
                'ocs_19to18',
                'ch3och3_13l0c13to12l1c12_EE',
                'h2c34S_7l1c7to6l1c6'
             ]

rrl = ['h30alpha', 'he30alpha', 'c30alpha']



for line in narrowline:
   nchandict[line] =  80
   startdict[line] =  '100.0 km/s'
   widthdict[line] =  '0.18' # km/s

for line in broadline:
   nchandict[line] =  140
   startdict[line] =  '8.0km/s'
   widthdict[line] =  '1.4' # km/s

for line in narrowline_coarse:
   nchandict[line] =  10
   startdict[line] =  '100.0km/s'
   widthdict[line] =  '1.4' # km/s

for line in rrl:
   nchandict[line] =  140
   startdict[line] =  '8.0km/s'
   widthdict[line] =  '1.4' # km/s





fieldtosplit = [
                'G33.92+0.11'
               ]

vlsrdict['G33.92+0.11'] = 107.6

phaserefdict['G33.92+0.11'] = {
                               'rah': 18.0,
                               'ram': 52.0,
                               'ras': 50.272,
                               'decd': 0.0,
                               'decm': 55.0,
                               'decs': 29.604
                              }

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







# a function to return a string for ra and dec, which is required for evaluating dopper velocity by the spwpick function
def get_radecstr(field, phaserefdict):

   ra = phaserefdict[field]['rah'] + phaserefdict[field]['ram'] / 60.0 + phaserefdict[field]['ras'] / 3600.0
   ra = ra * 15.0
   ra_str = str(ra) + 'deg'

   if ( phaserefdict[field]['decd'] >= 0.0 ):
     dec = phaserefdict[field]['decd'] + phaserefdict[field]['decm'] / 60.0 + phaserefdict[field]['decs'] / 3600.0
   else:
     dec = phaserefdict[field]['decd'] - phaserefdict[field]['decm'] / 60.0 - phaserefdict[field]['decs'] / 3600.0

   dec_str = str(dec) + 'deg'

   radec_str = ra_str + ' ' + dec_str
   return radec_str






# a function to pick the appropriate spectral window to split
def spwpick(msname, restfreq, radec_str, vlsr_kmpers=0.0, velwidth=0.0, maskedspw=[]):
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
      radec_str [string]: the RA and DEC of the field for doppler tracking
      vlsr_kmpers [float]: velocity in the LSRK frame, in unit of km/s
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
   msmd.open(msname)

   # get all spectral window IDs other than those associated with square law detectors  
   spwInfo = ms.getspectralwindowinfo()

   ###############################################################################
   scanInfo  = ms.getscansummary()
   num_scan  = len( scanInfo.keys() )
   begintime = 0.0
   # deriving the averaged begin time from all scans
   for scan in scanInfo.keys():
      begintime += scanInfo[scan]['0']['BeginTime'] / num_scan
   # print( begintime )

   # define a coordinate system for executing frequency frame transformation
   csys = cs.newcoordsys(direction=True, spectral=True)  
    # print csys.summary(list=False)  
   
   # reset the spectral reference to topocentric coordinate system
   csys.setreferencecode('TOPO', 'spectral', True) 

   # reset the epoch to the epoch of the observing time
   ep = csys.epoch()
   ep['m0']['value'] = begintime
   csys.setepoch(ep)
   ep = csys.epoch()

   # reset the observatory to the actual telescope name
   telescope_names = msmd.observatorynames() # 'ALMA'
   csys.settelescope( telescope_names[0] )

   # obtain target source direction
   # sourcedirs = msmd.sourceidsfromsourcetable()
   # print('#####', sourcedirs , '#####')

   # reset the direction to target source coordinate
   csys.setdirection (refcode='J2000', proj='SIN', projpar=[0,0],  
                   refpix=[0, 0], refval=radec_str)

   # reset the reference frequency
   csys.setreferencevalue(type='spec', value=(restfreq) ) 
   csys.setrestfrequency( qa.quantity(str(restfreq / 1e9) + 'GHz') )
   # print ( csys.referencecode('spectral', True) )
   # ['REST', 'LSRK', 'LSRD', 'BARY', 'GEO', 'TOPO', 'GALACTO', 'LGROUP', 'CMB', 'Undefined']

   # specify converting a pixel to LSRK world
   pixel = [0,0,0]
   csys.setconversiontype(spectral='LSRK')
   world_lsrk = csys.toworld(pixel, format='n')

   # evaluating the approximated frequency offset due to doppler tracking
   doppler_freq = world_lsrk['numeric'][2] - restfreq


   # print csys.referencecode(type='spectral')
   # print csys.projection()
   # print csys.referencepixel()
   # print csys.referencevalue(format='s')
   # print csys.restfrequency()
   # print csys.summary(list=False)
    
#   ###############################################################################

   # initialize return
   yourspw    = -1
   spwHzwidth = 0.0

   redshifted_freq = restfreq * math.sqrt(
                                       ( 1.0 - ( vlsr_kmpers / c_kmpers ) ) /
                                       ( 1.0 + ( vlsr_kmpers / c_kmpers ) )
                                         )

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

         # converting from topocentric velocity frame to lsrk
         bandlow = bandlow + doppler_freq
         bandup  = bandup  + doppler_freq

         if (
             ( redshifted_freq > bandlow )
             and
             ( redshifted_freq < bandup )
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
   msmd.done()
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

        print ( "\n")
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
           radec_str = get_radecstr(field, phaserefdict)

           if ( num_maskedspw == 0 ):           
              yourspw = spwpick(msname, linefreq, radec_str, vlsrdict[field], widthdict[line])
           else:
              yourspw = spwpick(msname, linefreq, radec_str, vlsrdict[field], widthdict[line], maskedspw)


           if (
               yourspw != -1 
              ):
              print ( line, ' is in spectral window :', yourspw )

              # defining output filename
              outputvis = visdict[vis] + '.' + line + '.' + field
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

