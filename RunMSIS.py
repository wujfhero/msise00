#!/usr/bin/env python
"""
Poker Flat Research Range altitude profile:   ./PlotMSIS.py 2018-01-01 -c 65 -148
"""
from pathlib import Path
from tempfile import gettempdir
from dateutil.parser import parse
import numpy as np
from matplotlib.pyplot import show
try:
    import seaborn as sns
    sns.set_style('ticks')
except ImportError:
    pass
#
import msise00
from msise00.plots import plotgtd
#
from gridaurora.worldgrid import latlonworldgrid


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='calls MSISE-00 from Python, a basic demo')
    p.add_argument('-t','--time',help='time of simulation (default over 24 hours from today', nargs='+')
    p.add_argument('-c','--latlon',help='geodetic latitude/longitude (deg)',metavar=('lat','lon'),type=float,nargs=2)
    p.add_argument('-a','--altkm',help='altitude (km) (start,stop,step)',metavar=('start','stop','step'),type=float,nargs=3)
    p.add_argument('-o','--odir',help='directory to write plots to',default=gettempdir())
    p.add_argument('-w',help='NetCDF4 .nc filename to write')
    p = p.parse_args()

    if p.time is not None:
        if len(p.time) == 2: # hour range
            time = np.arange(*p.time, dtype='datetime64[h]')
        elif len(p.time) == 1:
            time = parse(p.time[0])
    else:
        time =  np.arange('2017-08-21','2017-08-22',dtype='datetime64[h]')
#%% altitude 1-D mode
    if p.latlon is not None:
        print('entering single location mode')
        if p.altkm is None:
            p.altkm = (60., 1000, 5)
        altkm = np.arange(*p.altkm)
        glat,glon = p.latlon
#%% lat/lon grid mode at constant altitude
    else:# len(p.altkm)==1:
        print('lat/lon not specified, entering auto whole-world grid mode at first altitude')
        if p.altkm is None:
            altkm = 200.
        else:
            altkm = p.altkm[0]
        glat,glon = latlonworldgrid()

    altkm = np.atleast_1d(altkm)
    print(f'using altitudes from {altkm[0]:.1f} to {altkm[-1]:.1f} km')
# %% run
    atmos = msise00.run(time, altkm, glat, glon)
#%%
    if p.w:
        ncfn = Path(p.w).expanduser()
        print('saving',ncfn)
        atmos.to_netcdf(ncfn)

    plotgtd(atmos, p.odir)
    show()

