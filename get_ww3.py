# Baixa dados do NCEP/WW3 para o ponto mais proximo da
# boia de Recife para o ano de 2017

# Henrique Pereira - 25/01/2022

import os
import pandas as pd
import xarray as xr

# ds = xr.open_dataset('https://wwcei.noaa.gov/thredds-ocean/dodsC/ncep/nww3/2017/01/gribs/multi_1.glo_30m.wind.201701.grb2')

# 'https://polar.ncep.noaa.gov/waves/hindcasts/multi_1/201701/gribs/multi_1.glo_30m.wind.201701.grb2'

#pth_out = '/home/hp/Downloads/ww3ncep/'
pth_out = '/pessoal/henrique/database/WW3NCEP/'

# ponto da boia (lat, lon) (+360 p grade do ww3)
ponto_boia = [-3.2138, -38.4325+360.0] # fortaleza

anos = ['2017']
meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
variaveis = ['wind', 'hs', 'tp', 'dp']

out = pd.DataFrame()
for variavel in variaveis:
    print (variavel)
    dff = pd.DataFrame()
    for ano in anos:
        print (ano)
        for mes in meses:
            print (mes)

            filename = 'multi_1.glo_30m.{}.{}{}.grb2'.format(variavel, ano, mes)

            print (filename)
            url_grib = 'https://polar.ncep.noaa.gov/waves/hindcasts/multi_1/{}{}/gribs/{}'.format(
                        ano, mes, filename)
 
            # se nao exitir o arquivo na pasta
            if os.path.exists(pth_out + filename) == False:
                print ('baixando arquivo')
                os.system('cd {}; wget {}'.format(pth_out, url_grib))
            else:
                print ('arquivo ja existente')

            print ('lendo arquivo grib')
            ds = xr.open_dataset(pth_out + filename)

            print ('selecionando ponto da boia')
            ds1 = ds.sel(latitude=ponto_boia[0], longitude=ponto_boia[1], method='nearest')

            print ('convertendo em dataframe, selecionando variaveis e colocando indice de data')
            if variavel == 'wind':
                df = ds1[['u','v']].to_dataframe()
                df1 = df[['u','v','valid_time']].set_index('valid_time')
            elif variavel == 'hs':
                df = ds1[['swh']].to_dataframe()
                df1 = df[['swh','valid_time']].set_index('valid_time')
            elif variavel == 'tp':
                df = ds1[['perpw']].to_dataframe()
                df1 = df[['perpw','valid_time']].set_index('valid_time')
            elif variavel == 'dp':
                df = ds1[['dirpw']].to_dataframe()
                df1 = df[['dirpw','valid_time']].set_index('valid_time')

            print ('concatenando meses')
            dff = pd.concat((dff, df1), axis=0)

    print ('concatenando variaveis')
    out = pd.concat((out, dff), axis=1)

out.to_csv('output_ww3_pnboia_fortaleza.csv', float_format='%.2f', index=True)