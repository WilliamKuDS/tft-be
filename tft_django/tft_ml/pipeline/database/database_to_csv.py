import psycopg2
from config import load_config
import tft_query
import pandas as pd

def query_database(query):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
                cur.execute(query + ' LIMIT 0')
                column_names = [desc[0] for desc in cur.description]
                return data, column_names

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_games():
    data, column_names = query_database(tft_query.tft_game_query())
    df = pd.DataFrame(data, columns=column_names)
    file_name = ["../data/tft_games/tft_games.csv", "../data/tft_games/tft_games_pickled.csv"]

    try:
        df.to_csv(file_name[0])
        df.to_pickle(file_name[1])
        print("File {}, {} saved".format(file_name[0], file_name[1]))
    except Exception as e:
        print("File {} could not be saved. Error {}".format(file_name, e))

def get_units():
    data, column_names = query_database(tft_query.tft_unit_query())
    df = pd.DataFrame(data, columns=column_names)
    file_name = ["../data/tft_units/tft_units.csv", "../data/tft_units/tft_units_pickled.csv"]

    try:
        df.to_csv(file_name[0])
        df.to_pickle(file_name[1])
        print("File {}, {} saved".format(file_name[0], file_name[1]))
    except Exception as e:
        print("File {} could not be saved. Error {}".format(file_name, e))

def get_items():
    data, column_names = query_database(tft_query.tft_item_query())
    df = pd.DataFrame(data, columns=column_names)
    file_name = ["../data/tft_items/tft_items.csv", "../data/tft_items/tft_items_pickled.csv"]

    try:
        df.to_csv(file_name[0])
        df.to_pickle(file_name[1])
        print("File {}, {} saved".format(file_name[0], file_name[1]))
    except Exception as e:
        print("File {} could not be saved. Error {}".format(file_name, e))

get_games()
get_units()
get_items()
