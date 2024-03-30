import psycopg2
from config import load_config
from query import tft_game_query
import pandas as pd

def retrieveData():
    config = load_config()
    queryCommand = tft_game_query()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(queryCommand)
                data = cur.fetchall()
                cur.execute(queryCommand + ' LIMIT 0')
                column_names = [desc[0] for desc in cur.description]
                return column_names, data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def dataToCSV(data, file_name):
    try:
        data.to_csv(file_name, encoding='utf-8', index=False)
        print("File {} saved".format(file_name))
    except Exception as e:
        print("File {} could not be saved. Error {}".format(file_name, e))

def queryTableToCSV():
    column_names, data = retrieveData()
    df = pd.DataFrame(data, columns=column_names)
    dataToCSV(df, "tft_games.csv")
    print("TFT Games saved to csv")

def data_preprocessing():
    df = pd.read_csv('tft_games.csv')
    print(df.head().to_string())
    print(df.shape)
    if df.isnull().values.any():
        print("There are {} null values in the df".format(df.isnull().sum().sum()))
        nan_rows = df[df.isnull().T.any()].to_string()
        print("There are the null rows: {}".format(nan_rows))
        # From this, we see that the null values are mostly from lobby_rank, as all players in the
        # game are unranked
    else:
        print("There are no null values in the dataframe.")


data_preprocessing()

