# Processamento dos dados de Salinopolis

import conda
import os
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
from mpl_toolkits.basemap import Basemap as bm
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
import geopy.distance
plt.close('all')

def uv2id(u, v):
    """
    Conversao de u e v para intensidade e direcao
    """
    i = np.sqrt(u ** 2 + v ** 2)
    d = (np.rad2deg(np.arctan2(u, v))) % 360.
    return i, d

def read_era5_param(pathfile, datei, datef, ponto):
    """
    Leitura dos parâmetros do ERA5
    - pathname - path do arquivo netcdf
    - filename - arquivo netcdf
    - ponto mais proximo para pegar no era5
    - datei - data inicial
    - dataf - data final
    """
    ds = xr.open_dataset(pathfile)
    
    # seleciona ponto mais proximo
    ds1 = ds.sel(longitude=ponto[1], latitude=ponto[0], method='nearest')
    ds2 = ds1.sel(time=slice(datei, datef))
    df = ds2.to_dataframe()
    df['ws'], df['wd'] = uv2id(df.u10, df.v10)
    
    df.index.name = 'date'
    return ds, df

def plot_bmop_loc(etopo1, df_sal, df_for, boia, df_sal_costa):
    """
    """
    # lat lon ERA5
    lat_sal = df_sal.latitude[0]
    lon_sal = df_sal.longitude[0]
    lat_for = df_for.latitude[0]
    lon_for = df_for.longitude[0]
    lat_boia = boia.Lat[0]
    lon_boia = boia.Lon[0]
    # radius_era5_km = 0.3
    # radius_era5 = 1.0 * radius_era5_km / 111.0 #km to degrees
    # cria matriz com lat lon
    lons, lats = np.meshgrid(etopo1.lon.data, etopo1.lat.data)
    # m = bm(projection='cyl',llcrnrlat=lat_fso-.03,urcrnrlat=lat_fso+.03,
    #          llcrnrlon=lon_fso-.04,urcrnrlon=lon_fso+.04, lat_ts=0,resolution='l')
    m = bm(projection='cyl',llcrnrlat=-10,urcrnrlat=5, 
           llcrnrlon=-52,urcrnrlon=-32, lat_ts=0,resolution='h')
    fig = plt.figure(figsize=(8,8))
    # lvls = np.arange(-4000,0,1)
    # lvls = [-4000, -2000, -1000, -500, -200, -25]
    lvls = [-200]
    CS1 = m.contour(lons, lats, etopo1.z, colors='black',
                    # cmap=plt.cm.jet,
                    levels=lvls, alpha=0.3)
    plt.clabel(CS1, inline=1, inline_spacing=3, fontsize=10, fmt='%i')#, manual=manual_locations)
    plt.xticks(rotation=15)
    m.drawcoastlines()
    m.drawstates()
    m.fillcontinents()
    m.drawmeridians(np.arange(-52, -32, 2), labels=[0,0,0,1], linewidth=0.3)
    m.drawparallels(np.arange(-10, 5, 2), labels=[1,0,0,0], linewidth=0.3)
    # plota grade do era5
    # xx, yy = np.meshgrid(ds_sal.longitude.values, ds_sal.latitude.values)
    # plt.plot(xx, yy, 'ko', markersize=5)
    xx, yy = np.meshgrid(ds_for.longitude.values, ds_for.latitude.values)
    plt.plot(xx, yy, 'ko', markersize=5)
    # plota posicoes e nomes
    m.plot(lon_sal, lat_sal, 'k.', markersize=7)
    plt.text(lon_sal+0.02, lat_sal+0.01, 'ERA5_Sal', color='r', fontweight='bold', fontsize=14)
    m.plot(lon_for, lat_for, 'k.', markersize=7)
    plt.text(lon_for+0.02, lat_for+0.01, 'ERA5_For', color='r', fontweight='bold', fontsize=14)
    m.plot(lon_boia, lat_boia, 'g.', markersize=7)
    plt.text(lon_boia+0.02, lat_boia-0.05, 'Boia', color='r', fontweight='bold', fontsize=14)
    m.plot(df_sal.longitude.values[0], df_sal.latitude.values[0], 'g.', markersize=7)
    plt.text(df_sal.longitude.values[0]+0.02, df_sal.latitude.values[0]-0.05, 'S', color='r', fontweight='bold', fontsize=14)
    m.plot(df_sal_costa.longitude.values[0], df_sal_costa.latitude.values[0], 'g.', markersize=7)
    plt.text(df_sal_costa.longitude.values[0]+0.02, df_sal_costa.latitude.values[0]-0.05, 'costa', color='r', fontweight='bold', fontsize=14)
    # m.tissot(lon_era5, lat_era5, radius_era5, 30, color='k', alpha=0.2)
    # m.plot(lon_buoy, lat_buoy, 'k.', markersize=7)
    # m.tissot(lon_buoy, lat_buoy, radius_buoy, 30, color='k', alpha=0.2)
    # plt.text(lon_buoy+0.02, lat_buoy+0.01, 'BMOP', color='r', fontweight='bold', fontsize=14)
    plt.xticks(rotation=15)
    return fig


if __name__ == "__main__":

    ppath = os.environ['HOME']
    path_etopo = ppath + '/gdrive/etopo/ETOPO-REMO.nc'
    path_era5_salinopolis = ppath + '/gdrive/salinopolis/dados/era5/ERA5_param_salinopolis.nc'
    path_era5_fortaleza = ppath + '/gdrive/salinopolis/dados/era5/ERA5_param_fortaleza.nc'
    path_pnboia_fortaleza = ppath + '/gdrive/salinopolis/dados/pnboia/pnboia_fortaleza.csv'
    path_out_era5_fortaleza = ppath + '/gdrive/salinopolis/output_era5_fortaleza.csv'

    datei = '2016-12-01 00:00:00'
    datef = '2017-11-30 23:00:00'

    # dicionario com posicoes
    dicpos = {
              'sal': [0.8, -45.8], # salinopolis offshore
              'salc': [-0.690058, -46.7285], # salinopolis costeiro
              'for': [-3.2138, -38.4325], # fortaleza, ponto da boia
             }

    # lon_min, lon_max, lat_min, lat_max
    grade_etopo = [-52, -32, -10, 5]

    boia = pd.read_csv(path_pnboia_fortaleza, parse_dates=True, index_col='Datetime')

    etopo = xr.open_dataset(path_etopo)

    etopo1 = etopo.sel(lon=slice(grade_etopo[0],grade_etopo[1]), lat=slice(grade_etopo[2],grade_etopo[3]))

    # ERA5 salinopolis
    ds_sal, df_sal = read_era5_param(path_era5_salinopolis, datei=datei, datef=datef,
        ponto=[dicpos['sal'][0], dicpos['sal'][1]])

    # ERA5 salinipolis costeiro
    ds_sal_costa, df_sal_costa = read_era5_param(path_era5_salinopolis, datei=datei, datef=datef,
        ponto=[dicpos['salc'][0], dicpos['salc'][1]])

    # ERA5 fortaleza
    ds_for, df_for = read_era5_param(path_era5_fortaleza, datei=datei, datef=datef,
        ponto=[dicpos['for'][0], dicpos['for'][1]])

    # serie de dados continua na boia
    boia = boia[datei:datef]

    ###########################################################
    # calcula distancia entre 2 coordenadas
    print ('Distância entre Boia e ERA5_For: {:.1f} km'.format(
           geopy.distance.geodesic((boia.Lon[0], boia.Lat[0]), (df_for.longitude[0], df_for.latitude[0])).km))

    print ('Distância entre Boia e ERA5_Sal: {:.1f} km'.format(
           geopy.distance.geodesic((boia.Lon[0], boia.Lat[0]), (df_sal.longitude[0], df_sal.latitude[0])).km))

    print ('Distância entre ERA5_Sal e ERA5_For: {:.1f} km'.format(
           geopy.distance.geodesic((df_sal.longitude[0], df_sal.latitude[0]), (df_for.longitude[0], df_for.latitude[0])).km))

    print ('Distância entre pontos de grade do ERA5: {:.2f} km'.format(
           geopy.distance.geodesic((ds_sal.longitude[0], ds_sal.latitude[0]), (ds_sal.longitude[1], ds_sal.latitude[1])).km))

    ###########################################################
    plt.figure(figsize=(12,6))
    a = boia.Wdir
    a.plot(label='Boia')
    b = df_for.wd -180
    b[b < 0] = b[b < 0] + 360
    b.plot(label='ERA5')
    plt.title('Direção do vento em Fortaleza')
    plt.ylabel('graus')
    plt.ylim(0, 200)
    plt.xlim(a.index[0], a.index[-1])
    plt.xlim('2017-08', '2017-09')
    plt.legend()

    ###########################################################
    # plota localizacao do ERA5 e Boia
    fig = plot_bmop_loc(etopo1, df_sal, df_for, boia, df_sal_costa)
    # plt.savefig(path + 'localizacao_era5_salinopolis.png', bbox_inches="tight")

    ###########################################################
    # plotagem dos dados do pnboia e do era5 de fortaleza
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12,10), sharex=True)
    # ax1 = fig.add_subplot(311)
    axes[0].set_title('Fortaleza/CE')
    boia.Wvht.plot(ax=axes[0], ylim=(0,4), label='Boia')
    df_for.swh.plot(ax=axes[0], label='ERA5')
    axes[0].set_ylabel('Hs (m)')
    axes[0].legend(ncol=2)
    # axes[0].grid('on', which='major')
    # axes[0].grid('off', which='major', axis='xy' )
    axes[0].grid()
    boia.Dpd.plot(ax=axes[1], ylim=(4,22))
    df_for.mwp.plot(ax=axes[1])
    axes[1].set_ylabel('Tp (s)')
    axes[1].grid()
    # ax3 = fig.add_subplot(313)
    boia.Mwd.plot(ax=axes[2], ylim=(0, 150))
    df_for.mwd.plot(ax=axes[2])
    axes[2].set_ylabel('Dp º (Boia) / MWP º (ERA5) ')
    axes[2].grid()
    axes[2].set_xlim(boia.index[0], boia.index[-1])

    ###########################################################
    # plotagem dos da boia de fortaleza e era5 de salinopolis
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12,10), sharex=True)
    # ax1 = fig.add_subplot(311)
    axes[0].set_title('ERA5 Salinópolis X Boia Fortaleza')
    boia.Wvht.plot(ax=axes[0], ylim=(0,4), label='Boia_For')
    df_sal.swh.plot(ax=axes[0], label='ERA5_Sal')
    axes[0].set_ylabel('Hs (m)')
    axes[0].legend(ncol=2)
    # axes[0].grid('on', which='major')
    # axes[0].grid('off', which='major', axis='xy' )
    axes[0].grid()
    boia.Dpd.plot(ax=axes[1], ylim=(4,22))
    df_sal.mwp.plot(ax=axes[1])
    axes[1].set_ylabel('Tp (s)')
    axes[1].grid()
    # ax3 = fig.add_subplot(313)
    boia.Mwd.plot(ax=axes[2], ylim=(0, 360))
    df_sal.mwd.plot(ax=axes[2])
    axes[2].set_ylabel('Dp º (Boia) / MWP º (ERA5) ')
    axes[2].grid()
    axes[2].set_xlim(boia.index[0], boia.index[-1])

    ###########################################################
    # plotagem dos dados do pnboia
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12,8), sharex=True)
    # ax1 = fig.add_subplot(311)
    axes[0].set_title('PNBOIA Fortaleza')
    boia.Wvht.plot(ax=axes[0], ylim=(0,4))
    axes[0].set_ylabel('Hs (m)')
    # axes[0].grid('on', which='major')
    # axes[0].grid('off', which='major', axis='xy' )
    axes[0].grid()
    boia.Dpd.plot(ax=axes[1], ylim=(4,20))
    axes[1].set_ylabel('Tp (s)')
    axes[1].grid()
    # ax3 = fig.add_subplot(313)
    boia.Mwd.plot(ax=axes[2], ylim=(0, 360))
    axes[2].set_ylabel('Dp (º)')
    axes[2].grid()

    ###########################################################
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8,5), sharex=True)
    color = 'tab:blue'
    # ax1.set_xlabel('time (s)')
    ax1.set_title('PNBOIA Fortaleza')
    ax1.set_ylabel('Hs (m)', color=color)
    ax1.plot(boia.Wvht, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Int. Vento (m/s)', color=color)  # we already handled the x-label with ax1
    ax2.plot(boia.Wspd, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()


    ###########################################################
    # salva dados do ERA5
    # df_sal.to_csv(path_era5 + 'era5_param_salinopolis.csv')
    # df_sal_costa.to_csv(path_era5 + 'era5_param_salinopolis_costa.csv')
    df_for.to_csv(path_out_era5_fortaleza, float_format='%.2f')

    plt.show()
