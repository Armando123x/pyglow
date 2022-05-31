from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from datetime import datetime
import numpy as np

from . import generate_kpap


#GEOPHYSICAL_INDICES = generate_kpap.fetch()

def get_GEOPHYSICAL_table():
    return generate_kpap.fetch()

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
        
        x,day=np.shape(GEOPHYSICAL_INDICES)
        
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

      


    return kp, ap, f107, f107a, f107p, daily_kp, daily_ap, dst, ae
