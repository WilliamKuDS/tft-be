import argparse
import json
from datetime import timedelta, datetime
import re


def getPlayerNameFromURL(url):
    return url[34:]

def getDuplicates(checkValue, path):
    pass



def addData(gameStats, path):
    with open(path, "a+", encoding='utf-8') as outfile:
        temp = json.dumps(gameStats)
        outfile.write(temp + '\n')

def updateData(self, gameStats, path):
    pass

def readData(self, gameStats, path):
    pass

def deleteData(self, path, item):
    pass

def getNameLoop(self, item):
    pass


def parseQuery():
    parser = argparse.ArgumentParser(description='Enter Query Type')
    subparsers = parser.add_subparsers(dest='query', help='sub-command help')
    # parser.add_argument('-m', '--mode', action='store', help='Specify mode 1 (Query Player) or 2 (Query Subplayers)')

    parserMode_1 = subparsers.add_parser('1', help='Query Specific Player')
    parserMode_1.add_argument('-n', '--name', type=str, required=True, help='Player Name')
    parserMode_1.add_argument('-t', '--tag', type=str, required=True, help='Player Tag')
    parserMode_1.add_argument('-r', '--region', type=str, required=True, help='Player Region')
    parserMode_1.add_argument('-l', '--length', type=int, help='Amount of Matches to Query')

    parserMode_2 = subparsers.add_parser('2', help='Query Subplayers')
    parserMode_2.add_argument('-a', '--player_amount', type=int, required=True, help='Amount of Players to Query')
    parserMode_2.add_argument('-l', '--length', type=int, required=True, help='Amount to Matches to Query')

    parserMode_3 = subparsers.add_parser('3', help='Update Players')

    return parser.parse_args()

def getURL(name, region, tag):
    return 'https://www.metatft.com/player/' + region + '/' + name + '-' + tag


def calculate_date(time_string):
    current_time = datetime.now()

    if "hour" in time_string:
        hours = int(time_string.split()[0])
        return current_time - timedelta(hours=hours)

    elif "day" in time_string:
        if time_string.startswith("a"):  # Check if it's "a day ago"
            return current_time - timedelta(days=1)
        else:
            days = int(time_string.split()[0])
            return current_time - timedelta(days=days)

    elif "weeks" in time_string:
        weeks = int(time_string.split()[0])
        return current_time - timedelta(weeks=weeks)

    else:
        raise ValueError("Invalid time string")