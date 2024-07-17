import pandas as pd
import numpy as np
str_START_DATE = '01.01.2010'
str_END_DATE = '31.12.2014'
MAX_CONSUMERS = 2000
DECIMAL_PLACES = 6
dfid = pd.read_csv('data/Initial_data.csv', sep=';', encoding='cp1251', decimal=',')
if not dfid.empty:
    row = dfid.iloc[0]
    MAX_CONSUMERS = row['MAX_CONSUMERS']
    START_DATE = pd.to_datetime(row['START_DATE'], format='%d.%m.%Y')
    END_DATE = pd.to_datetime(row['END_DATE'], format='%d.%m.%Y')        
else:
    print("CSV файл пустой, используем данные по умолчанию")
    START_DATE = pd.to_datetime(str_START_DATE, format='%d.%m.%Y')
    END_DATE = pd.to_datetime(str_END_DATE, format='%d.%m.%Y')        
print(MAX_CONSUMERS)
print(START_DATE)
print(END_DATE)
file_path = 'data/power_outages2.csv'
df = pd.read_csv(file_path, sep=';', encoding='cp1251', decimal=',')
df['Дата'] = df['Дата'].astype("datetime64[ns]")
df = df[(df['Дата'] >= START_DATE) & (df['Дата'] <= END_DATE)]
df = df[df['Продолжительность'] > 5]
print(df)
df['SAIDI'] = df['Продолжительность']*df['Количество потребителей']
saidi_per_day = df.groupby('Дата')['SAIDI'].sum() / MAX_CONSUMERS
saidi_non_zero = saidi_per_day[saidi_per_day > 0]
alpha = round(np.log(saidi_non_zero).sum() / len(saidi_non_zero), DECIMAL_PLACES)
beta = round(np.sqrt(((np.log(saidi_non_zero) - alpha)**2).sum() / len(saidi_non_zero)), DECIMAL_PLACES)
T_MED = round(np.exp(alpha + 2.5 * beta), DECIMAL_PLACES)
data = []
data.append([alpha, beta, T_MED])
dfo = pd.DataFrame(data, columns=["alpha", "beta", "T_MED"])
str_START_DATE = START_DATE.strftime('%Y-%m-%d')
str_END_DATE = END_DATE.strftime('%Y-%m-%d')
alpha_beta_T_MED_file = f'data/alpha_beta_T__MED_{str_START_DATE}_{str_END_DATE}.csv'
dfo.to_csv(alpha_beta_T_MED_file, sep=';', encoding='cp1251', index=False, decimal=',')
print(alpha, beta, T_MED)
