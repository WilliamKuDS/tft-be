import psycopg2
#from tft.models import Game
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

from config import load_config
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

import ast

class DataPreprocessing:
    def __init__(self):
        self.data = None
    def retrieveData(self):
        config = load_config()
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM tft_game")
                    data = cur.fetchall()
                    cur.execute("Select * FROM tft_game LIMIT 0")
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

    #def preprocessData(self):
        #temp = self.data.values_list()
        #data = np.core.records.fromrecords(temp, names=[f.name for f in Game._meta.fields])
        #return data

dp = DataPreprocessing()
colNames, df = dp.retrieveData()
df.columns = colNames
df.drop(df.iloc[:, 0:3], inplace=True, axis=1)

df = df[df.queue == 'Ranked']

df.drop(columns=['queue'], inplace=True)

df['length_decimal'] = df['length'].apply(convert_to_decimal)
df.drop(columns=['length'], inplace=True)

df['stages'] = df['round'].apply(convert_to_stage)
df.drop(columns=['round'], inplace=True)

df = pd.get_dummies(df, columns=['headliner'])

augCol = []
for x in df['augments']:
    augCol.append(ast.literal_eval(x))

mlb = MultiLabelBinarizer(sparse_output=True)

df = df.join(
            pd.DataFrame.sparse.from_spmatrix(
                mlb.fit_transform(augCol),
                index=df.index,
                columns=mlb.classes_))
df = df.drop(['augments'], axis=1)

for i in df.index:
    x = df['traits'][i].replace("[", "").replace("]", "").strip()
    if x == "":
        continue
    new_x = ast.literal_eval(x)
    df.at[i, 'traits'] = new_x


df2 = pd.json_normalize(df['traits'])

#print(df2)
df.reset_index(drop=True, inplace=True)
df2.reset_index(drop=True, inplace=True)

new_df = pd.concat([df.drop(['traits'], axis=1), df2], axis=1)

unitList = []
for x in df['units']:
    #print(ast.literal_eval(x))
    unitList.append([ast.literal_eval(x)])

teamDF = pd.DataFrame(unitList, columns=['team'])

# Convert each team's list of dictionaries into a single dictionary
teams_dicts = []
for team in teamDF['team']:
    team_dict = {}
    for unit in team:
        unit_name = unit['Name']
        team_dict[f'{unit_name}_Tier'] = unit['Tier']  # Include the tier information
        for item in unit['Items']:
            team_dict[f'{unit_name}_{item}'] = 1  # Assuming presence of an item is marked with 1
    teams_dicts.append(team_dict)

# Use DictVectorizer to one-hot encode the dictionaries
vec = DictVectorizer(sparse=True)
X_encoded = vec.fit_transform(teams_dicts)

# Optionally, you can convert the sparse matrix to a DataFrame if needed
encoded_df = pd.DataFrame(X_encoded.toarray(), columns=vec.get_feature_names_out())

final_df = pd.concat([new_df.drop(['units'], axis=1), encoded_df], axis=1)

y = final_df['placement']
x = final_df.drop(columns=['placement'])

y = y - 1

scaler = MinMaxScaler()

# Normalize the numerical data between 0 and 1
X = scaler.fit_transform(x)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LGBMClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: %.2f%%" % (100 * accuracy))





