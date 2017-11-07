# A dictionary for line rest frequencies in units of GHz
# Notation
# Atoms are lowerscripted; quantum numbers (e.g., J, N, F) are upperscripted
# l: lower scripted
# u: upper scripted
# c: comma
# 1o2: 1 over 2 = 1/2

freqdict  = {}

# Frequently observed lines at ALMA band 6

freqdict['c-c3h2_3l3c0to2l2c1'] = '216.27876' # c-C$_{3}$H$_{2}$ 3$_{3,0}$-2$_{2,1}$,  Eu = 19.5 K

freqdict['ccd_N3to2_J7o2to5o2_F9o2to7o2'] = '216.37283' # CCD N=3-2, J=7/2-5/2, F=9/2-7/2,  Eu = 20.8 K

freqdict['ccd_N3to2_J7o2to5o2_F7o2to5o2'] = '216.37332' # CCD N=3-2, J=7/2-5/2, F=7/2-5/2,  Eu = 20.8 K
                                                        # blended with N=3-2, J=7/2-5/2, F=5/2-3/2

freqdict['ccd_N3to2_J5o2to3o2_F7o2to5o2'] = '216.42832' # CCD N=3-2, J=5/2-3/2, F=7/2-5/2,  Eu = 20.8 K
                                                        # blended with N=3-2, J=5/2-3/2, F=5/2-3/2

freqdict['ccd_N3to2_J5o2to3o2_F3o2to1o2'] = '216.42876' # CCD N=3-2, J=5/2-3/2, F=3/2-1/2,  Eu = 20.8 K

freqdict['ch3cho_11l1c10to10l1c9_E'] = '216.58194' # CH3CHO 11$_{1,10}$-10$_{1,9}$ E,    Eu = 64.9 K

freqdict['ch3cho_11l1c10to10l1c9_A'] = '216.63022' # CH3CHO 11$_{1,10}$-10$_{1,9}$ A,   Eu = 64.8 K

freqdict['hdcs_7l0c7to6l0c6'] = '216.66243' # HDCS 7$_{0,7}$-6$_{0,6}$,  Eu = 41.6 K

freqdict['hdcs_7l2c6to6l2c5'] = '216.93137' # HDCS 7$_{2,6}$-6$_{2,5}$,  Eu = 77.6 K

freqdict['hdcs_7l2c5to6l2c4']  = '217.26369' # HDCS 7$_{2,5}$-6$_{2,4}$,  Eu = 77.6 K

freqdict['h2s_2l2c0to2l1c1']   = '216.71044' # H2S 2$_{2,0}$-2$_{1,1}$,  Eu = 84.0 K

freqdict['ch3oh_5l1c4to4l2c2'] = '216.94560' # CH3OH 5$_{1,4}$-4$_{2,2}$,  Eu = 55.9 K

freqdict['sio_5to4'] = '217.10498'  # SiO 5-4,  Eu = 31.3 K

freqdict['dcn_3to2'] = '217.23863'  # DCN 3-2,  Eu = 20.9 K

freqdict['13cn_N2to1_J3o2to3o2_Fone1to1_F2to1'] = '217.07280100'  # 13CN N=2-1, J=3/2-3/2, F1=1-1, F=2-1, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to3o2_Fone1to1_F2to2'] = '217.07423900'  # 13CN N=2-1, J=3/2-3/2, F1=1-1, F=2-2, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone1to0_F0to1'] = '217.26463900'  # 13CN N=2-1, J=3/2-1/2, F1=1-0, F=0-1, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone1to0_F1to1'] = '217.27768000'  # 13CN N=2-1, J=3/2-1/2, F1=1-0, F=1-1, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone2to1_F2to2'] = '217.28680400'  # 13CN N=2-1, J=3/2-1/2, F1=2-1, F=2-2, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone2to1_F1to1'] = '217.29082300'  # 13CN N=2-1, J=3/2-1/2, F1=2-1, F=1-1, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone2to1_F1to0'] = '217.29660500'  # 13CN N=2-1, N=2-1, J=3/2-1/2, F1=2-1, F=1-0, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone2to2_F2to2'] = '217.29893700'  # 13CN N=2-1, N=2-1, J=5/2-3/2, F1=2-2, F=2-2, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone2to1_F2to1'] = '217.30117500'  # 13CN N=2-1, J=3/2-1/2, F1=2-1, F=2-1, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone2to1_F3to2'] = '217.30319100'  # 13CN N= 2-1, J=3/2-1/2, F1=2-1, F= 3-2, Eu = 15.7 K

freqdict['13cn_N2to1_J3o2to1o2_Fone1to0_F2to1'] = '217.30492700'  # 13CN N= 2-1, J=3/2-1/2, F1=1-0, F=2-1, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone2to2_F3to3'] = '217.30611700'  # 13CN N=2-1, J=5/2-3/2, F1= 2-2, F= 3-3, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone2to1_F3to2'] = '217.42856320'  # 13CN N=2-1, J=5/2-3/2, F1= 2-1, F=3-2, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone2to1_F2to1'] = '217.43635040'  # 13CN N=2-1, J=5/2-3/2, F1=2-1, F=2-1, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone2to1_F2to2'] = '217.43770200'  # 13CN N=2-1, J=5/2-3/2, F1=2-1, F=2-2, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone2to1_F1to1'] = '217.44372200'  # 13CN N=2-1, J=5/2-3/2, F1= 2-1, F=1-1, Eu = 15.7 K
                                                                  # blended with N=2-1, J=5/2-3/2, F1=2-1, F=1-0

freqdict['13cn_N2to1_J5o2to3o2_Fone3to2_F4to3'] = '217.46715000'  # 13CN N=2-1, J=5/2-3/2, F1=3-2, F=4-3, Eu = 15.7 K
                                                                  # blended with N=2-1, J=5/2-3/2, F1=3-2, F=3-2

freqdict['13cn_N2to1_J5o2to3o2_Fone3to2_F2to1'] = '217.46915100'  # 13CN N=2-1, J=5/2-3/2, F1=3-2, F=2-1, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone3to2_F2to2'] = '217.48055900'  # 13CN N=2-1, J=5/2-3/2, F1=3-2, F=2-2, Eu = 15.7 K

freqdict['13cn_N2to1_J5o2to3o2_Fone3to2_F3to3'] = '217.48360600'  # 13CN N=2-1, J=5/2-3/2, F1=3-2, F=3-3, Eu = 15.7 K

freqdict['t-c2h5oh_5l3c3-4l2c2'] = '217.80369'  # t-C$_{2}$H$_{5}$OH 5$_{3,3}$-4$_{2,2}$, Eu = 23.9 K

freqdict['c-hccch_6l1c6-5l0c5']  = '217.82215'  # c-HCCCH 6$_{1,6}$-5$_{0,5}$,  Eu = 38.6 K

freqdict['c-hccch_5l1c4-4l2c3']  = '217.94005'  # c-HCCCH 5$_{1,4}$-4$_{2,3}$,  Eu = 35.4 K

freqdict['c18o_2to1']            =  '219.56035680'    # C18O J=2-1,  Eu = 15.80580 K

freqdict['so3Sigma_6l5to5l4']    =  '219.94944200'    # SO $^{3}\Sigma$ 6(5)-5(4),  Eu = 34.98470 K

freqdict['13co_2to1']   =  '220.39867650'    # 13CO J=2-1,  Eu = 15.86618 K

freqdict['ch3cn_12to11_K4'] = '220.67929'  # CH$_{3}$CN J=12-11, K=4,  Eu = 183.1

freqdict['ch3cn_12to11_K3'] = '220.70902'  # CH$_{3}$CN J=12-11, K=3,  Eu = 133.2

freqdict['ch3cn_12to11_K2'] = '220.73026'  # CH$_{3}$CN J=12-11, K=2,  Eu = 97.4 K

freqdict['ch3cn_12to11_K1'] = '220.74301'  # CH$_{3}$CN J=12-11, K=1,  Eu = 76.0 K

freqdict['ch3cn_12to11_K0'] = '220.74726'  # CH$_{3}$CN J=12-11, K=0,  Eu = 68.9 K

freqdict['co_2to1']   =  '230.53800000'    # 12CO J=2-1,  Eu = 16.59608 K

freqdict['ocs_19to18'] = '231.06099'  # OCS J=19-18,  Eu = 110.9 K

freqdict['13cs_5to4']   = '231.22069'  # $^{13}$CS 5-4

freqdict['n2dp_3to2'] = '231.32185660'  # N$_{2}$D$^{+}$ 3-2,  Eu = 22.2 K 

freqdict['h30alpha']    = '231.90093'

freqdict['ch3och3_13l0c13to12l1c12_EE'] = '231.98782'  # CH$_{3}$OCH$_{3}$  13$_{0,13}$-12$_{1,12}$ EE,  Eu = 80.9 K
                                                       # blended with the AA, AE, and EA species which are within 0.2 MHz

freqdict['he30alpha']   = '231.99543'

freqdict['c30alpha']    = '232.016636'

freqdict['h2c34S_7l1c7to6l1c6'] = '232.75471'  # H$_{2}$C$^{34}$S  7$_{1,7}$-6$_{1,6}$,  Eu = 57.9 K
