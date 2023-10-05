from __future__ import print_function
from __future__ import absolute_import
import numpy 
from datetime import timedelta

from .get_kpap import get_kpap,get_GEOPHYSICAL_table



def get_apmsis(dn):
    GEOPHYSICAL_INDICES = get_GEOPHYSICAL_table()
    """
    Function: get_apmsis(dn)
    ---------------------
    returns an array of calculated ap indices suitable for MSIS.
    MSIS requires an array of ap values, described in nrlmsise00.f.
    This Python function formulates the various ap values for MSIS. From the
    fortran subroutine, we see that:

        AP - MAGNETIC INDEX(DAILY) OR WHEN SW(9)=-1. :
           - ARRAY CONTAINING:
             (1) DAILY AP
             (2) 3 HR AP INDEX FOR CURRENT TIME
             (3) 3 HR AP INDEX FOR 3 HRS BEFORE CURRENT TIME
             (4) 3 HR AP INDEX FOR 6 HRS BEFORE CURRENT TIME
             (5) 3 HR AP INDEX FOR 9 HRS BEFORE CURRENT TIME
             (6) AVERAGE OF EIGHT 3 HR AP INDICIES FROM 12 TO 33 HRS
                 PRIOR   TO CURRENT TIME
             (7) AVERAGE OF EIGHT 3 HR AP INDICIES FROM 36 TO 57 HRS
                 PRIOR  TO CURRENT TIME

    Inputs:
    --------
        dn : datetime object of the requested time

    Outputs:
    --------
        out : a 1x7 array of the caclulated ap indices

    History:
    --------
        7/21/12 Created, Timothy Duly (duly2@illinois.edu)

    """
    out = float('nan')*numpy.zeros(7)

    # (1) DAILY AP
 
    struct = get_kpap(GEOPHYSICAL_INDICES,dn=dn)
    out[0] = struct.ap_daily

    # (2) 3 HR AP INDEX FOR CURRENT TIME
    out[1] = struct.ap

    # (3) 3 HR AP INDEX FOR 3 HRS BEFORE CURRENT TIME
    struct= get_kpap(GEOPHYSICAL_INDICES,
                                          dn=dn+timedelta(hours=-3))
    out[2] = struct.ap

    # (4) 3 HR AP INDEX FOR 6 HRS BEFORE CURRENT TIME
    struct= get_kpap(GEOPHYSICAL_INDICES,
                                          dn=dn+timedelta(hours=-6))
    out[3] = struct.ap

    # (5) 3 HR AP INDEX FOR 9 HRS BEFORE CURRENT TIME
    struct = get_kpap(GEOPHYSICAL_INDICES,
                                          dn=dn+timedelta(hours=-9))
    out[4] = struct.ap

    # (6) AVERAGE OF EIGHT 3 HR AP INDICIES FROM 12 TO 33 HRS
    #     PRIOR   TO CURRENT TIME

    temp = numpy.zeros(8)
    for n in range(8):
        temp[n]= get_kpap(GEOPHYSICAL_INDICES,dn=dn+timedelta(hours=-12-3*n)).ap
 

    out[5] = numpy.nan if all(numpy.isnan(temp)) else numpy.nanmean(temp)

    # (7) AVERAGE OF EIGHT 3 HR AP INDICIES FROM 36 TO 57 HRS
    #     PRIOR  TO CURRENT TIME

    temp = numpy.zeros(8)
    for n in range(8):
        temp[n] = get_kpap(GEOPHYSICAL_INDICES,dn=dn+timedelta(hours=-36-3*n)).ap
 

    out[6] = numpy.nan if all(numpy.isnan(temp)) else numpy.nanmean(temp)

    return out
