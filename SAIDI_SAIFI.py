import pandas as pd
str_START_DATE_SS = '01.05.2015'
str_END_DATE_SS = '31.05.2015'
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
    START_DATE_SS = pd.to_datetime(row['START_DATE_SS'], format='%d.%m.%Y')
    END_DATE_SS = pd.to_datetime(row['END_DATE_SS'], format='%d.%m.%Y')        
else:
    print("CSV файл пустой, используем данные по умолчанию")
    START_DATE = pd.to_datetime(str_START_DATE, format='%d.%m.%Y')
    END_DATE = pd.to_datetime(str_END_DATE, format='%d.%m.%Y')        
    START_DATE_SS = pd.to_datetime(str_START_DATE_SS, format='%d.%m.%Y')
    END_DATE_SS = pd.to_datetime(str_END_DATE_SS, format='%d.%m.%Y')            
str_START_DATE = START_DATE.strftime('%Y-%m-%d')
str_END_DATE = END_DATE.strftime('%Y-%m-%d')
alpha_beta_T_MED_file = f'data/alpha_beta_T__MED_{str_START_DATE}_{str_END_DATE}.csv'
df_abT = pd.read_csv(alpha_beta_T_MED_file, sep=';', encoding='cp1251', decimal=',')
T_MED = df_abT['T_MED'].values[0]
print(f"T_MED: {T_MED:.6f}")
file_path = 'data/power_outages2.csv'
df = pd.read_csv(file_path, sep=';', encoding='cp1251', decimal=',')
df['Дата'] = df['Дата'].astype("datetime64[ns]")
df = df[(df['Дата'] >= START_DATE_SS) & (df['Дата'] <= END_DATE_SS)]
df = df[df['Продолжительность'] > 5]
df['SAIDI'] = df['Продолжительность']*df['Количество потребителей']
saidi_per_day = round(df.groupby('Дата')['SAIDI'].sum() / MAX_CONSUMERS, DECIMAL_PLACES)
saifi_per_day = round(df.groupby('Дата')['Количество потребителей'].sum() / MAX_CONSUMERS, DECIMAL_PLACES)
saidi_saifi_df = pd.DataFrame({'Дата': saidi_per_day.index.strftime('%Y-%m-%d'), 'SAIDI': saidi_per_day.values, 'SAIFI': saifi_per_day.values})
new_row = pd.DataFrame({'Дата': ['Сумма'], 'SAIDI': [round(saidi_per_day.sum(), DECIMAL_PLACES)], 'SAIFI': [round(saifi_per_day.sum(), DECIMAL_PLACES)]})
saidi_saifi_df = pd.concat([saidi_saifi_df, new_row], ignore_index=True)
str_START_DATE_SS = START_DATE_SS.strftime('%Y-%m-%d')
str_END_DATE_SS = END_DATE_SS.strftime('%Y-%m-%d')
saidi_saifi_file = f'data/saidi_saifi_{str_START_DATE_SS}_{str_END_DATE_SS}.csv'
saidi_saifi_df.to_csv(saidi_saifi_file, sep=';', encoding='cp1251', index=False, decimal=',')
saidi_filtered = saidi_per_day[saidi_per_day < T_MED]
saifi_filtered = saifi_per_day[saidi_per_day < T_MED]
saidi_saifi_filtered_df = pd.DataFrame({'Дата': saidi_filtered.index.strftime('%Y-%m-%d'), 'SAIDI': saidi_filtered.values, 'SAIFI': saifi_filtered.values})
new_row = pd.DataFrame({'Дата': ['Сумма'], 'SAIDI': [round(saidi_filtered.sum(), DECIMAL_PLACES)], 'SAIFI': [round(saifi_filtered.sum(), DECIMAL_PLACES)]})
saidi_saifi_filtered_df = pd.concat([saidi_saifi_filtered_df, new_row], ignore_index=True)
saidi_saifi_filtered_file = f'data/saidi_saifi_filtered_{str_START_DATE_SS}_{str_END_DATE_SS}.csv'
saidi_saifi_filtered_df.to_csv(saidi_saifi_filtered_file, sep=';', encoding='cp1251', index=False, decimal=',')
SAIDI = saidi_per_day.sum()
SAIDI_f = saidi_filtered.sum()
SAIFI = saifi_per_day.sum()
SAIFI_f = saifi_filtered.sum()
print("\nSAIDI и SAIFI за период:")
print(f"SAIDI: {SAIDI:.6f}")
print(f"SAIFI: {SAIFI:.6f}")
print("\nSAIDI и SAIFI за период без учета дней крупных событий:")
print(f"SAIDI: {SAIDI_f:.6f}")
print(f"SAIFI: {SAIFI_f:.6f}")
print('')
print(saidi_saifi_file)
print(saidi_saifi_filtered_file)
