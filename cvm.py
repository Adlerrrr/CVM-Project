import pandas as pd
import zipfile
import pandas as pd

column_types = {
    14: str,
    17: str,
    18: str,
    20: str,
    22: str,
    24: str,
    27: str,
    37: str,
    38: str
}

pd.set_option("display.max_colwidth",150)
""" https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_202112.zip """

def get_infos_cvm(year,month):
    url ='https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{:02d}{:02d}.zip'.format(year,month)
    return pd.read_csv(url,compression='zip',encoding='latin1',sep=';')

def get_key_infos_cvm():
    url = 'https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'
    return pd.read_csv(url,encoding='latin1',sep=';',dtype=column_types)

df_infos = get_infos_cvm(2022,3)
""" print(df_infos.head(80)) """

df_key_infos = get_key_infos_cvm()
""" print(df_key_infos.head(10))
 """
min_investor = 100000000

funds = df_infos[df_infos['VL_PATRIM_LIQ'] >= min_investor].pivot(index='DT_COMPTC',columns='CNPJ_FUNDO',values=['VL_TOTAL','VL_QUOTA','VL_PATRIM_LIQ','CAPTC_DIA','RESG_DIA'])
""" print(funds) """

nav = funds['VL_QUOTA']
nav_base1 = nav/funds['VL_QUOTA'].iloc[0]
""" print(nav)
print(nav_base1) """

pfee_rank = pd.DataFrame()
pfee_rank['retorno(%)'] = (nav_base1.iloc[-1].sort_values(ascending=False)[:10]-1) *100


for cnpj in pfee_rank.index:
    fund_name = df_key_infos[df_key_infos['CNPJ_FUNDO']==cnpj]
    pfee_rank.at[cnpj,'Fundo de investimento'] = fund_name['DENOM_SOCIAL'].values[0]
    pfee_rank.at[cnpj,'Classe'] = fund_name['CLASSE'].values[0]
    pfee_rank.at[cnpj,'PL'] = fund_name['VL_PATRIM_LIQ'].values[0]


print(pfee_rank)