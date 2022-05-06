from authenticate.auth import TwitterAuth

# Create twitter auth object
twitter_auth = TwitterAuth()
# Get the api object
api = twitter_auth.get_api()
# Update status
api.update_status("Hi")
