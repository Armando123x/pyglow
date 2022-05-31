import numpy as np
from pathlib import Path
import os 
import datetime as dt

from .get_kpap import get_kpap
from .get_apmsis import get_apmsis
from .constants import nan
from . import generate_kpap
from .indice_maintenance import update_indices


class Indice(object):

    def __init__(self, dn):
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
        
        self.GEOPHYSICAL_INDICES=generate_kpap.fetch()
        self.check_day()
        
        
    def check_day(self,): 
  
        '''
        Revisamos si los indices se encuentran actualizados
        '''
        path_IRI=Path(self.DIR_FILE+'/IRI_files')
        path_IRI.mkdir(parents=True,exist_ok=True)
        name_indicator=Path(self.DIR_FILE+'/IRI_files/last_day.txt')
        name_indicator.touch(exist_ok=True)
        #print("Verificando indices ...")
        impr=Path(self.DIR_FILE+"/IRI_files/impr.txt")
        
        impr.touch(exist_ok=True)
        now =dt.datetime.now(dt.timezone.utc)
        year=now.year
        escribir_text=False
        
        #Actualizamos la tabla
        #pgw.actualizar_tablas()  
        last_kp=generate_kpap.get_last_value()
        
        
        #last_kp=pgw.get_last_value() 
        
        with open (impr,'r+') as f:
            count=f.readline()
        try:
            count=int(count)
        except ValueError as e:
            count=0
        with open(name_indicator,'r') as f:
            linea=f.readline()
            fecha_hoy=now.strftime("%Y-%m-%d")
            if(linea==fecha_hoy):
                if (count!=1):
                    print("Los indices se encuentran actualizados a la fecha {}".format(fecha_hoy))
                    print("Ultimo valor Kp, Ap, 10.7 es de la fecha {}".format(last_kp))
                    with open (impr,'r+') as fr:
                        fr.write("1")
                else:
                    pass
            else:
                print("Los indices se actualizarán a la fecha de hoy {}. \nEsto puede tomar un momento...".format(fecha_hoy))
                update_indices(year)
                print("Actualización terminada")
                escribir_text=True
                #f.write(fecha_hoy)
                with open (impr,'r+') as fr:
                        fr.write("0")
                     
                
                
            if escribir_text:
                with open(name_indicator,'w') as f:
                    f.write(fecha_hoy)
                    self.GEOPHYSICAL_INDICES=generate_kpap.fetch(True) 
                    last_kp=generate_kpap.get_last_value()
                    print("Ultimo valor Kp, Ap, 10.7 es de la fecha {}".format(last_kp))
     
        
        
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
        all_nan &= np.isnan(self.kp)
        all_nan &= np.isnan(self.ap)
        all_nan &= np.isnan(self.f107)
        all_nan &= np.isnan(self.f107a)
        all_nan &= np.isnan(self.f107p)
        all_nan &= np.isnan(self.kp_daily)
        all_nan &= np.isnan(self.ap_daily)
        all_nan &= np.isnan(self.dst)
        all_nan &= np.isnan(self.ae)
        all_nan &= all(np.isnan(_) for _ in self.apmsis)

        return all_nan


import dateutil.parser

from datetime import timedelta
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
