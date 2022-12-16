import tweepy
from datetime import datetime, timedelta, timezone
import keys_test
import schedule

OUR_SEARCH_TERMS = ['python', 'javascript', 'data science', 'machine learning', 'artificial intelligence']

def str_to_time(x):
  return datetime.strptime(x, '%a %b %d %H:%M:%S %z %Y')

class PythonBot:
  
  def __init__(self):

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(keys_test.API_KEY, keys_test.API_KEY_SECRET)
    auth.set_access_token(keys_test.ACCESS_TOKEN, keys_test.ACCESS_TOKEN_SECRET)

    self.api = tweepy.API(auth)
    self.selection_function = lambda x: int(x['favorite_count']) + int(x['retweet_count']) + int(x['reply_count']) + (int(x['favorite_count']) + int(x['retweet_count'])) / int(x['user']['followers_count']) + int(x['user']['followers_count'])
    self.last_tweet_time = datetime.now(timezone.utc) - timedelta(minutes=10)

    # run it once now and then every 10 minutes after that
    self.run_bot()
    schedule.every(60).minutes.do(self.run_bot)

  def run_bot(self):
    try:
        found_tweets = []
        for term in OUR_SEARCH_TERMS:
            found_tweets += self.api.search_tweets(term, lang='en', result_type='recent', count=1000)
        # remove the unneeded things
        found_tweets = [t._json for t in found_tweets]
        # make sure not to old
        found_tweets = [t for t in found_tweets if self.str_to_time(t['created_at']) > self.last_tweet_time]
        print(found_tweets)
        # make sure they contain a link/image/video
        found_tweets = [t for t in found_tweets if 'http' in t['text']]
        # make sure no retweets
        found_tweets = [t for t in found_tweets if not ('retweeted_status' in t)]
        # select most popular one
        tweet = max(found_tweets, key=self.selection_function)
        # let's retweet this one
        self.api.retweet(tweet['id'])
        self.last_tweet_time = datetime.now(timezone.utc)
        print(f"BOT SUCCESSFUL RUN AT {self.last_tweet_time}")
    except Exception as e:
        print("Houston we had a problem...", e)

if __name__ == '__main__':
    bot = PythonBot()
    while True:
        schedule.run_pending()

# Consider using a more efficient data structure to store the tweets, such as a heap or a 
# priority queue, to make it easier to find the most popular tweet.

# Add more try/except blocks to handle different types of exceptions that may be thrown 
# when interacting with the Twitter API.

# Use a logging library to record important events and errors, instead of printing them to 
# the console.

# Use a more robust scheduling library, such as APScheduler, to schedule the bot to run 
# at regular intervals.