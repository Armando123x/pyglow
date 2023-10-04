
import numpy as np


class LocationTime(object):

    def __init__(self, dn=None, lat=None, lon=None, alt=None):

        self._dn = dn
        self.lat = lat
        self._lon = lon
        self.alt = alt
        
        if self._dn is not None:
            # Year:
        
            self.year = dn.year

            # Day of year:
            self.doy = dn.timetuple().tm_yday

            # UTC seconds:
            self.utc_sec = dn.hour*3600. + dn.minute*60.

            # UTC Hour:
            self.utc_hour = dn.hour

            # Solar local time hour:
            if self._lon is not None:
                self.slt_hour = np.mod(self.utc_sec/3600. + self._lon/15., 24)

            # Integer year and doy, e.g. 2018039
            self.iyd = np.mod(dn.year, 100)*1000 + self.doy

    @property
    def dn(self):
        return self._dn
    
    
    @dn.setter
    def dn (self,valor):
        self._dn = valor
        #operaciones 
        self.year = self._dn.year
        self.doy  = self._dn.timetuple().tm_day
        self.utc_sec = self._dn.hour*3600. + self._dn.minute*60
        self.utc_hour = self._dn.hour
        
        if self._lon is not None:
                self.slt_hour = np.mod(self.utc_sec/3600. + self._lon/15., 24)
        
        
        self.iyd = np.mod(self._dn.year,100)*1000 + self.doy
        
    
    @property
    def lon(self):
        return self._lon
    
    @lon.setter
    def lon(self,valor):
        self._lon=valor
        #operaciones 
        self.year = self._dn.year
        self.doy  = self._dn.timetuple().tm_day
        self.utc_sec = self._dn.hour*3600. + self._dn.minute*60
        self.utc_hour = self._dn.hour
        
        
        #operaciones 
        if self._lon is not None:
            self.slt_hour = np.mod(self.utc_sec/3600. + self._lon/15., 24)


    
        
            
        
        
    