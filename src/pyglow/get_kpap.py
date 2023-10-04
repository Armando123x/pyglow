from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from datetime import datetime
import numpy as np

from . import generate_kpap



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
    hour_index = int(np.floor(dn.hour/3.))
    
    
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
        
        day=np.shape(GEOPHYSICAL_INDICES)[1]
        
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
