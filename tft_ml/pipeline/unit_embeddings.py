import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('data/tft_units/tft_units_webscrape.csv')

unit_statistics_columns = ['Tierlist', 'Placement', 'Win Rate', 'Frequency']
unit_info_columns = ['Type', 'Traits']
unit_ability_columns = ['Ability Name', 'Ability Description']
unit_stat_columns = ['Health', 'Attack Damage', 'Ability Power', 'Mana Start', 'Mana Cost', 'Armor',
                        'Magic Resist', 'Attack Speed', 'Crit Chance', 'Crit Damage', 'Range']

df['Crit Chance'] = df['Crit Chance'].str.rstrip('%').astype(float)
df['Crit Damage'] = df['Crit Damage'].str.rstrip('%').astype(float)

scaler = MinMaxScaler()
df_normalized = df.copy()
df_normalized[unit_stat_columns] = scaler.fit_transform(df[unit_stat_columns])

df['Power Level'] = df_normalized[unit_stat_columns].sum(axis=1)
final_df = df[['Name', 'Tier', 'Power Level']]
final_df['Name'] = final_df['Name'].str.replace('[^a-zA-Z0-9]', '', regex=True).str.lower()
final_df.to_csv('data/tft_units/tft_units_power.csv', index=False)
