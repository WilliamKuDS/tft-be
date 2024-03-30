import psycopg2
# from tft.models import Game
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

from config import load_config
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler, LabelEncoder, StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

import ast


class DataPreprocessing:
    def __init__(self):
        self.data = None

    def retrieveData(self):
        config = load_config()
        queryCommand = '''SELECT 
    tft_game_info.queue,
    tft_game_info.lobby_rank,
    tft_game.player_game_id,
    tft_game.placement,
    tft_game.level,
    tft_game.length,
    tft_game.round,
    array_agg(DISTINCT tft_game_trait.game_trait_id) AS game_traits,
    array_agg(DISTINCT tft_game_unit.game_unit_id) AS game_units,
    array_agg(DISTINCT tft_augment.augment_id) AS augments
FROM 
    tft_game_info
JOIN 
    tft_game ON tft_game_info.game_id = tft_game.game_id_id
LEFT JOIN 
    tft_game_game_trait_id ON tft_game.player_game_id = tft_game_game_trait_id.game_id
LEFT JOIN 
    tft_game_trait ON tft_game_game_trait_id.game_trait_id = tft_game_trait.game_trait_id
LEFT JOIN 
    tft_game_game_unit_id ON tft_game.player_game_id = tft_game_game_unit_id.game_id
LEFT JOIN 
    tft_game_unit ON tft_game_game_unit_id.game_unit_id = tft_game_unit.game_unit_id
LEFT JOIN 
    tft_game_augment_id ON tft_game.player_game_id = tft_game_augment_id.game_id
LEFT JOIN 
    tft_augment ON tft_game_augment_id.augment_id = tft_augment.augment_id
GROUP BY 
    tft_game_info.queue,
    tft_game_info.lobby_rank,
    tft_game.player_game_id,
    tft_game.placement,
    tft_game.level,
    tft_game.length,
    tft_game.round'''

        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(queryCommand)
                    data = cur.fetchall()
                    cur.execute(queryCommand + ' LIMIT 0')
                    colNames = [desc[0] for desc in cur.description]
                    return colNames, pd.DataFrame(data)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


def listOHE(df, colName):
    mlb = MultiLabelBinarizer(sparse_output=True)
    df = df.join(
        pd.DataFrame.sparse.from_spmatrix(
            mlb.fit(df[colName]),
            index=df.index,
            columns=mlb.classes_))

    return df


def convert_to_decimal(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes + seconds / 60.0


def convert_to_stage(time_str):
    round, stages = map(int, time_str.split('-'))
    return round * 7 + stages

    # def preprocessData(self):
    # temp = self.data.values_list()
    # data = np.core.records.fromrecords(temp, names=[f.name for f in Game._meta.fields])
    # return data


def data_preprocessing():
    dp = DataPreprocessing()
    colNames, df = dp.retrieveData()
    df.columns = colNames

    df = df[df.queue == 'ranked']

    df.drop(columns=["player_game_id", 'queue', 'lobby_rank'], inplace=True)

    df['length_decimal'] = df['length'].apply(convert_to_decimal)
    df.drop(columns=['length'], inplace=True)
    #
    df['stages'] = df['round'].apply(convert_to_stage)
    df.drop(columns=['round'], inplace=True)
    #

    df['game_traits'] = df['game_traits'].apply(lambda x: ','.join(map(str, x)))
    df['game_units'] = df['game_units'].apply(lambda x: ','.join(map(str, x)))
    df['augments'] = df['augments'].apply(lambda x: ','.join(map(str, x)))

    categorical_columns = ['game_traits', 'game_units', 'augments']
    # df.drop(columns=['game_traits', 'game_units', 'augments'], inplace=True)

    labelencoder = LabelEncoder()
    for col in categorical_columns:
        df[col] = labelencoder.fit_transform(df[col])

    for col in categorical_columns:
        df[col] = df[col].astype('int')

    print(df.columns)
    print(df.to_string())

    y = df['placement']
    X = df.drop(columns=['placement'])

    scaler = StandardScaler()
    scaler.fit(X)
    #X_scaled = scaler.transform(X)
    #scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    labels = [2,3,4]

    #print(X_scaled)

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
    X_validation, X_test, y_validation, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)


    train_data = lgb.Dataset(X_train, label=y_train, categorical_feature=labels, free_raw_data=False)
    validation_data = lgb.Dataset(X_validation, label=y_validation, categorical_feature=labels, free_raw_data=False)

    param = {'num_leaves': 31, 'objective': 'multiclass', 'num_class': 9}
    param['metric'] = ['multi_error', 'multi_logloss']

    num_round = 20
    bst = lgb.train(param, train_data, num_round, valid_sets=[validation_data], callbacks=[lgb.early_stopping(stopping_rounds=5)])
    bst.save_model('model.txt', num_iteration=bst.best_iteration)
    bst.save_model('model.txt')


    y_pred = bst.predict(X_test)
    y_pred = np.argmax(y_pred, axis=1)

    print(y_pred)
    print(y_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

    # df = pd.get_dummies(df, columns=['headliner'])
    #
    # augCol = []
    # for x in df['augments']:
    #     augCol.append(ast.literal_eval(x))
    #
    # mlb = MultiLabelBinarizer(sparse_output=True)
    #
    # df = df.join(
    #             pd.DataFrame.sparse.from_spmatrix(
    #                 mlb.fit_transform(augCol),
    #                 index=df.index,
    #                 columns=mlb.classes_))
    # df = df.drop(['augments'], axis=1)
    #
    # for i in df.index:
    #     x = df['traits'][i].replace("[", "").replace("]", "").strip()
    #     if x == "":
    #         continue
    #     new_x = ast.literal_eval(x)
    #     df.at[i, 'traits'] = new_x
    #
    #
    # df2 = pd.json_normalize(df['traits'])
    #
    # #print(df2)
    # df.reset_index(drop=True, inplace=True)
    # df2.reset_index(drop=True, inplace=True)
    #
    # new_df = pd.concat([df.drop(['traits'], axis=1), df2], axis=1)
    #
    # unitList = []
    # for x in df['units']:
    #     #print(ast.literal_eval(x))
    #     unitList.append([ast.literal_eval(x)])
    #
    # teamDF = pd.DataFrame(unitList, columns=['team'])
    #
    # # Convert each team's list of dictionaries into a single dictionary
    # teams_dicts = []
    # for team in teamDF['team']:
    #     team_dict = {}
    #     for unit in team:
    #         unit_name = unit['Name']
    #         team_dict[f'{unit_name}_Tier'] = unit['Tier']  # Include the tier information
    #         for item in unit['Items']:
    #             team_dict[f'{unit_name}_{item}'] = 1  # Assuming presence of an item is marked with 1
    #     teams_dicts.append(team_dict)
    #
    # # Use DictVectorizer to one-hot encode the dictionaries
    # vec = DictVectorizer(sparse=True)
    # X_encoded = vec.fit_transform(teams_dicts)
    #
    # # Optionally, you can convert the sparse matrix to a DataFrame if needed
    # encoded_df = pd.DataFrame(X_encoded.toarray(), columns=vec.get_feature_names_out())
    #
    # final_df = pd.concat([new_df.drop(['units'], axis=1), encoded_df], axis=1)
    #
    # y = final_df['placement']
    # x = final_df.drop(columns=['placement'])
    #
    # y = y - 1
    #
    # scaler = MinMaxScaler()
    #
    # # Normalize the numerical data between 0 and 1
    # X = scaler.fit_transform(x)

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #
    # model = LGBMClassifier(random_state=42)
    # model.fit(X_train, y_train)
    # y_pred = model.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy: %.2f%%" % (100 * accuracy))
