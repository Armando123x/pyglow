import numpy
import os  

import dateutil.parser

from datetime import timedelta,datetime
from . import generate_kpap,get_kpap

class Indice(object):

    def __init__(self, dn, ):
        """
        :param dn: datetime of indice data
        """
        
        # Store datetime associated with indice:
        self.dn = dn
        # Assign to member variables:
        self.kp = numpy.nan
        self.ap = numpy.nan
        self.f107 = numpy.nan
        self.f107a = numpy.nan
        self.f107p = numpy.nan
        self.kp_daily = numpy.nan
        self.ap_daily = numpy.nan
        self.dst = numpy.nan
        self.ae = numpy.nan
        self.DIR_FILE=os.path.dirname(__file__)
        # AP values for MSIS:
        self.apmsis = [numpy.nan, ] * 7
        
        self.GEOPHYSICAL_INDICES=generate_kpap.fetch(False)
       
 
     
        
        
    def run(self): 
        
        """
        Calculates the geophysical indices
        """
        
        # Geophysical indices:
       
        
        struct = \
            get_kpap(self.GEOPHYSICAL_INDICES,self.dn)

        # Assign to member variables:
        self.kp = struct.kp
        self.ap = struct.ap
        self.f107 = struct.f107
        self.f107a = struct.f107a
        self.f107p = struct.f107p
        self.kp_daily = struct.kp_daily
        self.ap_daily = struct.ap_daily
        self.dst = struct.dst
        self.ae = struct.ae

        # AP values for MSIS:
        self.apmsis = get_apmsis(self.dn)

    def all_nan(self):
        """
        Returns a boolean indicating if all indices are NaN
        """

        all_nan = True
        all_nan &= numpy.isnan(self.kp)
        all_nan &= numpy.isnan(self.ap)
        all_nan &= numpy.isnan(self.f107)
        all_nan &= numpy.isnan(self.f107a)
        all_nan &= numpy.isnan(self.f107p)
        all_nan &= numpy.isnan(self.kp_daily)
        all_nan &= numpy.isnan(self.ap_daily)
        all_nan &= numpy.isnan(self.dst)
        all_nan &= numpy.isnan(self.ae)
        all_nan &= all(numpy.isnan(_) for _ in self.apmsis)

        return all_nan



def check_stored_indices(date0, date1):
    """
    Helper function to determine which dates do not have indices

    :param date0: String start date
    :param date1: String end date
    """

    # Parse input dates:
    dn0 = dateutil.parser.parse(date0)
    dn1 = dateutil.parser.parse(date1)

    # Find date range:
    dns = [dn0 + timedelta(days=kk) for kk in range((dn1-dn0).days)]

    print("Checking: input date range:")
    print("  {}".format(dn0.strftime("%Y-%m-%d")))
    print("  to")
    print("  {}".format(dn1.strftime("%Y-%m-%d")))

    have_all = True
    for dn in dns:

        # Instantiate indice class:
        indice = Indice(dn)

        # Find the indices:
        indice.run()

        # Are all the indices NaN?
        if indice.all_nan():
            status = "--- FAIL ---"
            failed = True
            have_all = False
        else:
            failed = False
            status = "OK"

        # Report:
        if failed:
            print("{}: {}".format(dn.strftime("%Y-%m-%d"), status))

    # Report only if there were no issues:
    if have_all:
        print(
            ">> We have all of the geophysical indices files between these "
            "dates."
        )

    return












#----------------------------------------- get_apmsis.py --------------------------------------------------------------
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
    out = numpy.nan*numpy.zeros(7)

    # (1) DAILY AP
 
    struct = get_kpap(GEOPHYSICAL_INDICES,dn=dn)
    out[0] = struct.daily_ap

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

#---------------------------------------- get_kpap.py ----------------------------------------------
def get_GEOPHYSICAL_table():
    return generate_kpap.fetch(False)


def get_kpap(GEOPHYSICAL_INDICES,dn):
    # Fetch geophysical indices (Global variable to make it fast):

    """
    Function: get_kpap(dn)
    ---------------------
    returns the geophysical indices for datetime object dn

    Inputs:
    --------
        dn : datetime object of the requested time

    Outputs:
    --------
        kp, ap, f107, f107a, f107p, daily_kp, daily_ap, dst, ae

    History:
    --------s
        7/21/12 Created, Timothy Duly (duly2@illinois.edu)

    """
    dn_floor = datetime(dn.year, dn.month, dn.day)
    day_index = (dn_floor - generate_kpap.EPOCH).days
    hour_index = int(numpy.floor(dn.hour/3.))
    
    
    try:
        
        kp = GEOPHYSICAL_INDICES[hour_index, day_index]
        ap = GEOPHYSICAL_INDICES[hour_index+8, day_index]
        f107 = GEOPHYSICAL_INDICES[16, day_index]
        f107a = GEOPHYSICAL_INDICES[17, day_index]
        f107p = GEOPHYSICAL_INDICES[16, day_index-1]
        daily_kp = GEOPHYSICAL_INDICES[18, day_index]
        daily_ap = GEOPHYSICAL_INDICES[19, day_index]
        
        dst = GEOPHYSICAL_INDICES[20+dn.hour, day_index]
        ae = GEOPHYSICAL_INDICES[44+dn.hour, day_index]
        
        
    except IndexError:
        
        day=numpy.shape(GEOPHYSICAL_INDICES)[1]
        
        kp = GEOPHYSICAL_INDICES[hour_index, day-1]
        ap = GEOPHYSICAL_INDICES[hour_index+8, day-1]
        f107 = GEOPHYSICAL_INDICES[16, day-1]
        f107a = GEOPHYSICAL_INDICES[17, day-1]
        f107p = GEOPHYSICAL_INDICES[16, day-2]
        daily_kp = GEOPHYSICAL_INDICES[18, day-1]
        daily_ap = GEOPHYSICAL_INDICES[19, day-1]
        
        
        dst = GEOPHYSICAL_INDICES[20+dn.hour, day-1]
        ae = GEOPHYSICAL_INDICES[44+dn.hour, day-1]
        
        # print("\nNo se cuentan con suficientes valores de los indices Kp y Ap para el dia deseado.\
        #       Se calcula con el día máximo disponible {}".format(str(generate_kpap.get_last_value())))

      
    class struct(object):
        def __init__(self):
            self.kp = None
            self.ap = None
            self.f107 = None
            self.f107a = None
            self.f107p = None
            self.daily_kp = None
            self.daily_ap = None
            self.dst = None
            self.ae = None

    obj = struct()
    obj.kp   = kp
    obj.ap   = ap
    obj.f107 = f107
    obj.f107a = f107a
    obj.f107p = f107p
    obj.daily_ap = daily_ap
    obj.daily_kp = daily_kp
    obj.dst = dst
    obj.ae = ae
    # return kp, ap, f107, f107a, f107p, daily_kp, daily_ap, dst, ae
    return obj
