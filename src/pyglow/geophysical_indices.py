import os
import numpy
import datetime as dt


from pathlib import Path
from .constants import nan
from . import generate_kpap
from .get_kpap import get_kpap
from datetime import timedelta
from .get_apmsis import get_apmsis
from .indice_maintenance import update_indices



verbose = False

class Indice(object):

    def __init__(self, dn, ):
        """
        :param dn: datetime of indice data
        """
        
        # Store datetime associated with indice:
        self.dn = dn
        # Assign to member variables:
        self.kp = nan
        self.ap = nan
        self.f107 = nan
        self.f107a = nan
        self.f107p = nan
        self.kp_daily = nan
        self.ap_daily = nan
        self.dst = nan
        self.ae = nan

        
        self.DIR_FILE=os.path.dirname(__file__)
        # AP values for MSIS:
        self.apmsis = [nan, ] * 7
        
        self.GEOPHYSICAL_INDICES=generate_kpap.fetch(False)
 
        
 
            
            
 
        
    def run(self): 
        
        """
        Calculates the geophysical indices
        """
        
        # Geophysical indices:
       
        
        kp, ap, f107, f107a, f107p, kp_daily, ap_daily, dst, ae = \
            get_kpap(self.GEOPHYSICAL_INDICES,self.dn)

        # Assign to member variables:
        self.kp = kp
        self.ap = ap
        self.f107 = f107
        self.f107a = f107a
        self.f107p = f107p
        self.kp_daily = kp_daily
        self.ap_daily = ap_daily
        self.dst = dst
        self.ae = ae

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



# def check_stored_indices(date0, date1):
#     """
#     Helper function to determine which dates do not have indices

#     :param date0: String start date
#     :param date1: String end date
#     """

#     # Parse input dates:
#     dn0 = dateutil.parser.parse(date0)
#     dn1 = dateutil.parser.parse(date1)

#     # Find date range:
#     dns = [dn0 + timedelta(days=kk) for kk in range((dn1-dn0).days)]

#     print("Checking: input date range:")
#     print("  {}".format(dn0.strftime("%Y-%m-%d")))
#     print("  to")
#     print("  {}".format(dn1.strftime("%Y-%m-%d")))

#     have_all = True
#     for dn in dns:

#         # Instantiate indice class:
#         indice = Indice(dn)

#         # Find the indices:
#         indice.run()

#         # Are all the indices NaN?
#         if indice.all_nan():
#             status = "--- FAIL ---"
#             failed = True
#             have_all = False
#         else:
#             failed = False
#             status = "OK"

#         # Report:
#         if failed:
#             print("{}: {}".format(dn.strftime("%Y-%m-%d"), status))

#     # Report only if there were no issues:
#     if have_all:
#         print(
#             ">> We have all of the geophysical indices files between these "
#             "dates."
#         )

#     return
