# processamento dos dados do waverys

import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
plt.close('all')

def imprime_variaveis(ds):
    """
    imprime nos das variaveis
    """
    for v in list(ds.data_vars):
        print (v + ' -- ' + ds[v].long_name)
    return

if __name__ == "__main__":

    # pathname
    pathname1 = '/home/hp/Dropbox/salinopolis/waverys/'
    pathname2 = '/media/hp/HIGGINS/projetos/salinopolis/dados/pnboia/'
    pathname3 = '/media/hp/HIGGINS/projetos/salinopolis/dados/era5/'

    p = {
    'sal':  [0.66517, -45.5839],
    'salc': [-0.6900, -46.7285],
    'for':  [-3.2138, -38.4325],
         }

    ds_wave = xr.open_dataset(pathname1 + 'global-reanalysis-wav-001-032_1610734452367.nc')
    ds_era5 = xr.open_dataset(pathname3 + 'ERA5_param_fortaleza.nc')
    boia = pd.read_csv(pathname2 + 'pnboia_fortaleza.csv', parse_dates=True, index_col='Datetime')

    # imprime_variaveis(ds)

    # seleciona dados para salinopolis e cria dataframe
    wave = ds_wave.sel(latitude=p['for'][0], longitude=p['for'][1], method='nearest').to_dataframe()
    era5 = ds_era5.sel(latitude=p['for'][0], longitude=p['for'][1], method='nearest').to_dataframe()

    boia = boia.rolling(window=3, center=True).mean()
    boia = boia.resample('3H').mean()

    # pega o mesmo periodo nos dados e no modelo
    boia = boia['2017-01-01 00:00:00':'2017-12-31 21:00:00']
    wave = wave['2017-01-01 00:00:00':'2017-12-31 21:00:00']

    boia.to_csv('boia.csv', float_format='%.2f')
    wave.to_csv('wave.csv', float_format='%.2f')

    print ('\n')
    print (list(wave.columns))
    print ('\n')
    print (list(era5.columns))

    # plotagem dos dados do pnboia e do era5 de fortaleza
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12,10), sharex=True)
    # ax1 = fig.add_subplot(311)
    axes[0].set_title('Fortaleza/CE')
    boia.Wvht.plot(ax=axes[0], ylim=(0,4), label='Boia')
    wave.VHM0.plot(ax=axes[0], label='WAVERYS')
    wave.VHM0_SW1.plot(ax=axes[0], label='WAVERYS_swell')
    wave.VHM0_WW.plot(ax=axes[0], label='WAVERYS_sea')
    # era.swh.plot(ax=axes[0], label='ERA5')
    axes[0].set_ylabel('Hs (m)')
    axes[0].legend(ncol=2)
    # axes[0].grid('on', which='major')
    # axes[0].grid('off', which='major', axis='xy' )
    axes[0].grid()
    # boia.Dpd.plot(ax=axes[1], ylim=(4,22), label='tp_boia')
    wave.VTPK.plot(ax=axes[1], label='total')
    # wav.VTM01_SW1.plot(ax=axes[1], label='swell')
    # wave.VSDX.plot(ax=axes[1], label='stokes_U')
    # wave.VSDY.plot(ax=axes[1], label='stokes_V')
    axes[1].set_ylabel('Tp (s)')
    axes[1].grid()
    axes[1].legend()
    # ax3 = fig.add_subplot(313)
    boia.Mwd.plot(ax=axes[2], ylim=(0, 150))
    wave.VMDR.plot(ax=axes[2])
    axes[2].set_ylabel('Dp º')
    axes[2].grid()
    axes[2].set_xlim(wave.index[0], wave.index[-1])

    plt.show()
