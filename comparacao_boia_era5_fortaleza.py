# comparacao dos dados de fortaleza
# era5, pnboia, e pos-processado do pnboia

import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
plt.close('all')

ppath = os.environ['HOME']

era5 = pd.read_csv(ppath + '/gdrive/salinopolis/output_era5_fortaleza.csv',
    parse_dates=True, index_col='date')

pnboia = pd.read_csv(ppath + '/gdrive/salinopolis/dados/pnboia/pnboia_fortaleza.csv',
    parse_dates=True, index_col='Datetime')

pp = pd.read_csv(ppath + '/gdrive/salinopolis/parametros_onda_fortaleza.csv',
    parse_dates=True, index_col='date')

# subtrair serie do periodo medio do era5 e do pnboia
era5 = era5['2016-12']
pp = pp['2016-12']

pp['mean_spec_period'] = gaussian_filter(pp.mean_spec_period, sigma=1)

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title('Periodos de onda calculado pelos dados espectrais da boia de fortaleza')
# pp[['tz','tp','mean_spec_period','mean_zup_period']].plot(ax=ax1)

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title('Comparacao da boia com o ERA5')
# # pp[['tz','tp','mean_spec_period','mean_zup_period']].plot(ax=ax1)
# pp[['hm0']].plot(ax=ax1)
# era5[['swh']].plot(ax=ax1)

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title('Comparacao da boia com o ERA5')
# pp[['tz','tp','mean_spec_period','mean_zup_period']].plot(ax=ax1)
# # pp[['tp']].plot(ax=ax1)
# era5[['mwp']].plot(ax=ax1)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_title('Comparacao da boia com o ERA5')
ax1.plot(pp.mean_spec_period, label='Posproc')
# pp[['tp']].plot(ax=ax1)
ax1.plot(era5.mwp, label='ERA5')
ax1.plot(pp.mean_spec_period + (era5.mwp/pp.mean_spec_period), '-', label='Posproc + (ERA5 / Posproc)')
# ax1.plot(era5.mwp - pp.mean_zup_period)
# ax1.set_xlim(pp.index[0], pp.index[-1])
ax1.set_ylabel('Mean Wave Period (segundos)')
ax1.legend()


plt.show()