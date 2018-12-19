from sqlalchemy import create_engine, Table, MetaData, select
import sqlalchemy
#import pandas as pd

#querying and connecting to the database

engine = create_engine ('sqlite:///brexit_tweets.db')
connection = engine.connect()

metadata = MetaData()

brexit_table = Table('brexit_tweets', metadata, autoload=True, autoload_with=engine)

#print(brexit_table.columns.keys())

#filtering tweets and text from users in London

london_tweets = select([brexit_table]).where(brexit_table.columns.location.startswith('london'))


for result in connection.execute(london_tweets):
    print(result.text)