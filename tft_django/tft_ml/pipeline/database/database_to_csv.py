import psycopg2
from config import load_config
from query import tft_game_query
import pandas as pd

config = load_config()
queryCommand = tft_game_query()

try:
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(queryCommand)
            data = cur.fetchall()
            cur.execute(queryCommand + ' LIMIT 0')
            column_names = [desc[0] for desc in cur.description]

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

df = pd.DataFrame(data, columns=column_names)
file_name = ["../data/tft_games.csv", "../data/tft_games_pickled.csv"]

try:
    df.to_csv(file_name[0])
    df.to_pickle(file_name[1])
    print("File {} saved".format(file_name[0]))
except Exception as e:
    print("File {} could not be saved. Error {}".format(file_name, e))
