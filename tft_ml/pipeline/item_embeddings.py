import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def parse_stats(stats_str):
    stats_list = stats_str.strip("[]").replace("'", "").split(", ")
    stats_dict = {}
    for stat in stats_list:
        if stat:
            key, value = stat.split(" +")
            stats_dict[key.strip()] = float(value.strip('%'))
    return stats_dict


data = pd.read_csv('data/tft_items/tft_items_webscrape.csv')
data['Stats'] = data['Stats'].apply(parse_stats)
stats_df = data['Stats'].apply(pd.Series)
stats_df.fillna(0, inplace=True)

stat_columns = stats_df.columns

scaler = MinMaxScaler()
normalized_stats = scaler.fit_transform(stats_df)
normalized_stats_df = pd.DataFrame(normalized_stats, columns=stat_columns)

data['Power Level'] = normalized_stats_df.sum(axis=1)

final_df = pd.concat([data['Name'].str.replace('[^a-zA-Z0-9]', '', regex=True).str.lower(), data['Power Level']], axis=1)
final_df.to_csv('data/tft_items/tft_items_power.csv', index=False)
