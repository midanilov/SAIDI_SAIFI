import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta
START_YEAR = 2010
END_YEAR = 2022
MAX_CONSUMERS = 2000
MIN_DURATION = 1
MAX_DURATION = 4320 * 60
CONSUMERS_STEP = 50
DECIMAL_PLACES = 6
def generate_power_outages(start_year, end_year):
    data = []
    for year in range(start_year, end_year + 1):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        for _ in range(random.randint(30, 100)):
            random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
            unix_time = int(time.mktime(random_date.timetuple()))
            date_str = random_date.strftime("%Y-%m-%d")
            time_str = random_date.strftime("%H:%M:%S")
            duration_seconds = np.random.lognormal(mean=5, sigma=2)
            duration = round(max(MIN_DURATION, min(duration_seconds, MAX_DURATION)) / 60, DECIMAL_PLACES)
            consumers = random.randint(1, MAX_CONSUMERS // CONSUMERS_STEP) * CONSUMERS_STEP
            interruption_type = "устойчивый" if duration > 5 else "мгновенный"
            data.append([unix_time, date_str, time_str, duration, consumers, interruption_type, year])
    df = pd.DataFrame(data, columns=["Время UNIX", "Дата", "Время", "Продолжительность", "Количество потребителей", "Тип прерывания", "Год"])
    df.sort_values(by="Время UNIX", inplace=True)
    i = 0
    while i < len(df) - 1:
        current_end_time = df.iloc[i]['Время UNIX'] + pd.Timedelta(minutes=float(df.iloc[i]['Продолжительность'])).total_seconds()
        next_start_time = df.iloc[i + 1]['Время UNIX']
        if current_end_time >= next_start_time:
            combined_end_time = df.iloc[i + 1]['Время UNIX'] + pd.Timedelta(minutes=float(df.iloc[i + 1]['Продолжительность'])).total_seconds()
            new_duration = (combined_end_time - df.iloc[i]['Время UNIX']) / 60
            new_duration = round(new_duration, DECIMAL_PLACES)
            df.at[i, 'Продолжительность'] = new_duration
            df.at[i, 'Количество потребителей'] += df.iloc[i + 1]['Количество потребителей']
            df.drop(df.index[i + 1], inplace=True)
            df.reset_index(drop=True, inplace=True)
        else:
            i += 1
    return df
dfid = pd.read_csv('data/Initial_data.csv', sep=';', encoding='cp1251', decimal=',')
if not dfid.empty:
    row = dfid.iloc[0]
    START_YEAR = row['START_YEAR']
    END_YEAR = row['END_YEAR']
    MAX_CONSUMERS = row['MAX_CONSUMERS']
    CONSUMERS_STEP = row['CONSUMERS_STEP']
    MIN_DURATION = row['MIN_DURATION']
    MAX_DURATION = row['MAX_DURATION']
else:
    print("CSV файл пустой, используем данные по умолчанию")
power_outages_df = generate_power_outages(START_YEAR, END_YEAR)
power_outages_df.to_csv('data/power_outages2.csv', sep=';', encoding='cp1251', index=False, decimal=',')
years_stat = []
for year in range(START_YEAR, END_YEAR + 1):
    year_data = power_outages_df[power_outages_df['Год'] == year]
    stable_count = year_data[year_data['Тип прерывания'] == 'устойчивый'].shape[0]
    instant_count = year_data[year_data['Тип прерывания'] == 'мгновенный'].shape[0]
    min_duration = year_data['Продолжительность'].min()
    max_duration = year_data['Продолжительность'].max()
    years_stat.append([year, stable_count, instant_count, min_duration, max_duration])
total_stable_count = power_outages_df[power_outages_df['Тип прерывания'] == 'устойчивый'].shape[0]
total_instant_count = power_outages_df[power_outages_df['Тип прерывания'] == 'мгновенный'].shape[0]
total_min_duration = power_outages_df['Продолжительность'].min()
total_max_duration = power_outages_df['Продолжительность'].max()
total_stat = ["Весь период", total_stable_count, total_instant_count, total_min_duration, total_max_duration]
stat_df = pd.DataFrame(years_stat + [total_stat], columns=["Период", "Устойчивые", "Мгновенные", "Мин. время", "Макс. время"])
print(stat_df)
stat_df.to_csv('data/power_outages_stats.csv', sep=';', encoding='cp1251', index=False, decimal=',')
