import os
import sys
from logging import DEBUG
from pathlib import Path

from dotenv import load_dotenv

project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

from yfpy import Data
from yfpy.logger import get_logger
from yfpy.query import YahooFantasySportsQuery

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ENVIRONMENT SETUP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# load .env file in order to read local environment variables
load_dotenv(dotenv_path=project_dir / "auth" / ".env")

# set directory location of private.json for authentication
auth_dir = project_dir / "auth"

# set target directory for data output
data_dir = Path(__file__).parent / "output"

# create YFPY Data instance for saving/loading data
data = Data(data_dir)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VARIABLE SETUP  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# set desired season year
def get_season():
    # season = 2012
    # season = 2013
    # season = 2014
    # season = 2015
    # season = 2016
    # season = 2017
    # season = 2018
    # season = 2019
    # season = 2020
    # season = 2021
    # season = 2022
    season = 2023
    return season

season = get_season()

# set desired league ID (see README.md for finding value)
def get_league_id():
    # FOOTBALL
    league_id = "579463"  # NFL - 2023


    return league_id


league_id = get_league_id()

def get_game_code():
    # FOOTBALL
    game_code = "nfl"  # NFL

    return game_code

game_code = get_game_code()

def get_game_id():
    # FOOTBALL
    game_id = 423  # NFL - 2023

    return game_id


game_id = get_game_id()


# configure the Yahoo Fantasy Sports query (change all_output_as_json_str=True if you want to output JSON strings)
yahoo_query = YahooFantasySportsQuery(
    auth_dir,
    league_id,
    game_code,
    game_id=game_id,
    offline=False,
    all_output_as_json_str=False,
    consumer_key=os.environ["YFPY_CONSUMER_KEY"],
    consumer_secret=os.environ["YFPY_CONSUMER_SECRET"]
)

# Manually override league key for example code to work
yahoo_query.league_key = f"{game_id}.l.{league_id}"

print(yahoo_query)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# RUN QUERIES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


#print(repr(yahoo_query.get_league_draft_results()))
print(yahoo_query.get_league_standings())
logger = get_logger("yfpy.models", DEBUG)