import tweepy
import keys_test

def api():
  # Authenticate to Twitter
  auth = tweepy.OAuthHandler(keys_test.API_KEY, keys_test.API_KEY_SECRET)
  auth.set_access_token(keys_test.ACCESS_TOKEN, keys_test.ACCESS_TOKEN_SECRET)

  return tweepy.API(auth)

def tweet(api: tweepy.API, message:str, image_path=None):
  if image_path:
    api.update_status_with_media(message, image_path)
  else:
    api.update_status(message)

  print('Tweeted Successfully!')


if __name__ == '__main__':
  api = api()
  tweet(api, 'This was tweeted using Python', 'dog.jpg')