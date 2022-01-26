# Comparacao dos dados de reanalise do WW3 com os dados
# da boia de Fortaleza
# Henrique Pereira - 26/01/2022

import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import importlib
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ocean-wave'))
import waveplot, waveaux
importlib.reload(waveplot)
importlib.reload(waveaux)
plt.close('all')

pth_ww3 = '/home/hp/gdrive/salinopolis/ww3ncep/'
pth_boia = '/media/hp/HIGGINS/database/PNBOIA/fortaleza/'

fln_ww3 = 'output_ww3_pnboia_fortaleza.csv'
fln_boia = 'fortaleza.csv'

ww3 = pd.read_csv(pth_ww3 + fln_ww3, parse_dates=True, index_col='valid_time')

boia = pd.read_csv(pth_boia + fln_boia, parse_dates=True, index_col='Datetime')

#interpola o ww3 para 1h
ww3 = ww3.resample('1H').mean().interpolate()

# reamostra dados da boia para 1h e seleciona o periodo do ww3

# qualificacao nos dados
boia['Dpd'].loc[boia.Dpd < 0] = np.nan

boia = boia.resample('1H').mean().interpolate()
boia = boia.loc[ww3.index[0]:ww3.index[-1]]

# calcula intensidade e direcao do vento
ww3['ws'], ww3['wd'] = waveaux.uv2id(ndr_ucomp=ww3.u, ndr_vcomp=ww3.v, str_conv='meteo')

# waveplot.plot_serie_wind_hs_tp_dp(date=ww3.index,
# 								  ws=ww3.ws,
# 								  wd=ww3.wd,
# 								  hs=ww3.swh,
# 								  tp=ww3.perpw,
# 								  dp=ww3.dirpw,
# 								  title='WW3')

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(boia.Wspd, label='boia')
ax1.plot(ww3.ws, label='ww3')
ax1.legend()
ax1.set_ylabel('vel vento')
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.plot(boia.Wdir)
ax2.plot(ww3.wd)
ax2.set_ylabel('dir vento')

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(boia.Wvht, label='boia')
ax1.plot(ww3.swh, label='ww3')
ax1.legend()
ax1.set_ylabel('altura')
ax2 = fig.add_subplot(312, sharex=ax1)
ax2.plot(boia.Dpd)
ax2.plot(ww3.perpw)
ax2.set_ylabel('periodo')
ax3 = fig.add_subplot(313, sharex=ax1)
ax3.plot(boia.Mwd)
ax3.plot(ww3.dirpw)
ax3.set_ylabel('direcao')

plt.show()