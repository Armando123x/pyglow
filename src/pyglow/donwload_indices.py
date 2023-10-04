import os
import pytz
import shutil
import urllib
import contextlib
import collections

from keys import *
from datetime import datetime



class downloader(object):
      
    def __init__(self,**kwargs):

        self.verbose = kwargs.get("verbose",False)


        self.__download_kp(2020)

        self.__download_ae(2020)
        
        #change this line when dst and kp data from peru stations is ready
        self.__download_dst(2020)

        

    def __download_kp(self,year0,year1=None):


        if year1 is None:
            year1 = datetime.now(pytz.utc).year

        for year in range(year0,year1+1):

            src="ftp://ftp.gfz-potsdam.de/pub/home/obs/Kp_ap_Ap_SN_F107/"\
                    + "Kp_ap_Ap_SN_F107_%4i.txt" %(year)

            
            name_file = "%4i" % (year)

            

            path_des = os.path.join(PYGLOW_FILES,'kp',name_file)

            if not os.path.isdir(os.path.dirname(path_des)):

                os.makedirs(os.path.dirname(path_des))

            listname = os.listdir(os.path.join(PYGLOW_FILES,'kp'))

            if (not(name_file in listname)) or (year1==datetime.now(pytz.utc).year):
                    try:
                        with contextlib.closing(urllib.request.urlopen(src)) as r:
                            with open(path_des, 'wb') as f:
                                shutil.copyfileobj(r, f)


                    except IOError as e:
        
                                print("Failed downloading data for year {}."
                                    "File does not exist ({})".format(
                                        year,
                                        str(e),
                                    ),
                                )

    def __download_ae(self,year0,year1=None):
        
        pyglow_dir = os.path.join(PYGLOW_FILES,'ae')

        if not os.path.isdir(pyglow_dir):
             os.makedirs(pyglow_dir)


        if year1 is None:
            year1 = datetime.now(pytz.utc).year

        for year in range(year0,year1+1):
            for month in range(1,13):
                filename = '{:4d}{:02d}'.format(year,month)

                des = os.path.join(pyglow_dir, filename)

                self.__process_ae(year,month,des)
 

    def __process_ae(self,year, month, des):
        '''
        Helper function to earch for the appropriate location
        and download the AE index file from WDC Kyoto for the
        given month and year. Save it to the specified file "des".
        Return True if successful, False if not.
        '''
        # There are three possible sources of data. Search for
        # them in the following order:
        # 1) Final
        # 2) Provisional
        # 3) Realtime
        year_month = '%i%02i' % (year, month)
        wgdc_fn = 'ae%s%02i.for.request' % (str(year)[2:], month)
        src_provisional = \
            'http://wdc.kugi.kyoto-u.ac.jp/ae_provisional/%s/%s' % \
            (year_month, wgdc_fn)
        src_realtime = 'http://wdc.kugi.kyoto-u.ac.jp/ae_realtime/%s/%s' % \
            (year_month, wgdc_fn)

        success = False

        for src in [src_provisional, src_realtime]:
            try:
                with contextlib.closing(urllib.request.urlopen(src)) as r:
                    contents = r.readlines()
                    # If that succeeded, then the file exists
                    if self.verbose:
                        print(
                            "\nDownloading\n{src}\nto\n{des}".format(
                                src=src,
                                des=des,
                            )
                        )

                    with open(des, 'w') as f:
                        # this shrinks the filesize to hourly
                        for c in contents:
                            c = c.decode('utf8')
                            f.write(
                                "%s%s%s\n" % (c[12:18], c[19:21], c[394:400])
                            )
                    success = True
                    break
            except urllib.error.HTTPError:
                pass
        return success
    
    def __download_dst(self,year0,year1=None):
        """
        Update the Dst index files used in pyglow.
        The files will be downloaded from WDC Kyoto
        to your pyglow installation directory.

        _update_dst(years=None)

        :param years: (optional) a list of years to download.
                If this input is not provided, the full
                range of years starting from 2005 to the
                current year will be downloaded. Pre-2005
                files are shipped with pyglow.
        """

        pyglow_dir = os.path.join(PYGLOW_FILES,'dst')

        if year1 is None:
            year1 = datetime.now(pytz.utc).year

        if not os.path.isdir(pyglow_dir):
            os.makedirs(pyglow_dir)

        for year in range(year0,year1+1):

            for month in range(1,13):
                filename = '{:4d}{:02d}'.format(year,month)

                des = os.path.join(pyglow_dir, filename)

 
        # Loop through each month:
        for month in range(1, 13):
            des = '%s%i%02i' % (pyglow_dir, year, month)
            self.__process_dst(year, month, des)

        return

    def __process_dst(year, month, des):


        """
        Helper function to earch for the appropriate location
        and download the DST index file from WDC Kyoto for the
        given month and year. Save it to the specified file "des".
        Return True if successful, False if not.
        """
        # There are three possible sources of data. Search for
        # them in the following order:
        # 1) Final
        # 2) Provisional
        # 3) Realtime

        success = False
 

 
        year_month = '%i%02i' % (year, month)
        wgdc_fn = 'dst%s%02i.for.request' % (str(year)[2:], month)
        src_final = 'http://wdc.kugi.kyoto-u.ac.jp/dst_final/%s/%s' % \
            (year_month, wgdc_fn)
        src_provisional = \
            'http://wdc.kugi.kyoto-u.ac.jp/dst_provisional/%s/%s' % \
            (year_month, wgdc_fn)
        src_realtime = 'http://wdc.kugi.kyoto-u.ac.jp/dst_realtime/%s/%s' % \
            (year_month, wgdc_fn)

        
        for src in [src_final, src_provisional, src_realtime]:
            try:
                with contextlib.closing(urllib.request.urlopen(src)) as r:
                    contents = r.read().decode('utf8')
                    # If that succeeded, then the file exists
                    print(
                        "\nDownloading\n{src}\nto\n{des}".format(
                            src=src,
                            des=des
                        )
                    )
                    with open(des, 'w') as f:
                        f.write(contents)
                    success = True
                    break
            except urllib.error.HTTPError:
                pass
    
        return success

            