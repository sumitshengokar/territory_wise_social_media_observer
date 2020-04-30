import sys
import datetime
from tweepy import API,Cursor
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
import pymysql


# Replace the "None"s by your own credentials
ACCESS_TOKEN ='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_TOKEN_SECRET ='YYYYYYYYYYYYYYY'
CONSUMER_KEY='ZZZZZZZZZZZZZZZZZZZZZZZ'
CONSUMER_SECRET='SSSSSSSSSSSSSSSSSSSSSSSSSSs'

#### TWITTER AUTHENTICATOR



auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)



def add_in_db(retweet_count, text, create, likes, location, source, reply, retweet):
    sql = "INSERT INTO Tweets (retweet_count,tweet,created_time,likes,location,source,reply,retweeted) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    val = [retweet_count, text, create, likes, location, source, reply, retweet]
    mycursor.execute(sql, val)
    conn.commit()


def run_code():
    # Replace the "None"s by your own credentials
    ACCESS_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    ACCESS_TOKEN_SECRET = 'YYYYYYYYYYYYYYYYYYYYY'
    CONSUMER_KEY = 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'
    CONSUMER_SECRET = 'SSSSSSSSSSSSSSSSSS'

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth, wait_on_rate_limit=True,
              wait_on_rate_limit_notify=True)

    conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
    mycursor = conn.cursor()

    class Listener(StreamListener):
        def __init__(self, output_file=sys.stdout):
            super(Listener, self).__init__()

        def add_in_db(retweet_count, text,create,likes,location,source,reply,retweet):
            sql = "INSERT INTO Tweets (retweet_count,tweet,created_time,likes,location,source,reply,retweeted) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            val = [retweet_count, text, create, likes, location, source, reply, retweet]
            mycursor.execute(sql, val)
            conn.commit()

        def on_status(self, status):
            text = status.text
            retweet_count = status.retweet_count
            create = status.created_at
            likes = status.favorite_count
            source = status.source
            location = status.user.location
            retweet = "False"
            try:
                if status.retweeted_status:
                    retweet = "True"
                    likes = status.retweeted_status.favorite_count
            except:
                retweet = "False"
            reply = "False"
            try:
                if status.in_reply_to_screen_name:
                    reply = "True"
            except:
                reply = "False"

            try:
                if not location:
                    location = "None"
            except:
                location = status.user.location

            print(text)
            add_in_db(retweet_count, text,create,likes,location,source,reply,retweet)


        def on_error(self, status_code):
            print("Encountered streaming error",status_code)
            return False


    listener = Listener()

    stream = Stream(auth=api.auth, listener=listener,tweet_mode='extended')
    tags = ['#kashmir','#Brexit',#india','#corona', '#modi', '#china', '#WHO', '#maharashtra', '#pune','#mumbai',
            '#PM','#actor', '#CM', '#pakistan','#trump']
    stream.filter(track=tags)
    try:
        print('Start streaming.')
        stream.sample(languages=['en'])
    except KeyboardInterrupt:
        print("Stopped.")
        conn.close()
    finally:
        print('Done.')
        conn.close()
        stream.disconnect()


if __name__=="__main__":
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
    mycursor = conn.cursor()
    run_code()
