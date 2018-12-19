#code based on code here: http://adilmoujahid.com/posts/2014/07/twitter-analytics/ and here https://www.dataquest.io/blog/streaming-data-python/

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_credentials import *
from textblob import TextBlob
import dataset

db = dataset.connect ('sqlite:///brexit_tweets.db')

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    

#filter out retweets
    def on_status (self, status):
        if status.retweeted or status.text.startswith('RT @'): 
            return
    
            
        loc = status.user.location
        date = status.created_at
        text = status.text
        retweet_count = status.retweet_count
        followers = status.user.followers_count
        blob = TextBlob(text)
        sent = blob.sentiment

            
        table = db['brexit_tweets']

        table.insert(dict(
            location = loc,
            date = date,
            text = text,
            retweet_count = retweet_count,
            followers = followers,
            polarity = sent.polarity,
            subjectivity = sent.subjectivity
                
             ))
    


    def on_error(self, status_code):
        if status_code == 420:
            return False



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode='extended')

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['brexit'],languages=['en'])



