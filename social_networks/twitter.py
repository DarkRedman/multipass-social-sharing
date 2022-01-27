from .base import SocialNetwork
import tweepy, os

class Twitter(SocialNetwork):
    def __init__(self, config, **kwargs):
        super().__init__(config=config, **kwargs)
        self.auth = None
        self.api = None
        self.logged_as = None

        try:
            auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
            auth.set_access_token(config['ACCESSTOKEN'], config['ACCESSTOKEN_SECRET'])
            api = tweepy.API(auth, wait_on_rate_limit=True, cache=None, retry_count=3, retry_delay=5, retry_errors=set([408, 500, 503, 504]))
            self.auth = auth
            self.api = api
            self.logged_as = api.verify_credentials().name
            self.upload_folder = config['UPLOAD_FOLDER']
        except KeyError:
            pass # Missing api credentials
        except tweepy.errors.Unauthorized as e:
            pass # Bad credentials

    def share(self, message, files=[]):
        if self.api:
            media_ids = []

            for filename in files:
                media = self.api.media_upload(filename)
                media_ids.append(media.media_id)

            self.api.update_status(message, media_ids=media_ids)

            return True
        return False


    @property
    def active(self):
        return bool(self.api)
    

if __name__ == '__main__':
    tw = Twitter()