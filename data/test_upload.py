##import httplib2,time
##import oauth2 as oauth
from flickr_auth import getconfig
##url = 'http://api.flickr.com/services/upload'
###url = 'http://api.flickr.com/services/rest'
cfg = getconfig()
##consumer = oauth.Consumer(key=cfg['api_key'],secret=cfg['secret'])
##params = {'oauth_consumer_key': consumer.key,
##          'oauth_nonce': oauth.generate_nonce(),
##          'oauth_signature_method':'HMAC-SHA1',
##          'oauth_timestamp': int(time.time()),
##          'oauth_token': '72157631406445432-f1d5db15852b53fc',
##          'oauth_version': "1.0",
##          'username': 'filibot.web',
##          #'api_key': consumer.key,
##          #'method':'upload',
##          'oauth_token_secret': '907be36bc82e0c36'
##          }
##req = oauth.Request(method='POST',url=url,parameters=params)
##signature = oauth.SignatureMethod_HMAC_SHA1().sign(req,consumer,None)
##req['oauth_signature'] = signature
##req['photo'] = 'test_photo.jpg' #this is a file in the immediate directory
##print(req.to_url()) #debugging
##resp, content = httplib2.Http().request(req.to_url(),"POST")
##print(content)
##########################################
##access_token = {}
##access_token['user_nsid'] = '85725978@N07'
##access_token['oauth_token_secret'] = '907be36bc82e0c36'
import os
##import flickr_api as f
path = os.path.expanduser(r'~\My Documents\filibot\data')
photofile = "test_photo.jpg"
##f.set_auth_handler('tokens.cfg') #file containing api keys and auth tokens.
##user = f.test.login()
###f.upload(photo_file=os.path.join(path,photofile), title="Test Automated Upload")
############################################
##This works as an alternative...
import flickr
tokens = {'api_key':cfg['api_key'],
          'api_secret':cfg['secret'],
          'oauth_token':raw_input('Provide oauth token:\n>> '),
          'oauth_token_secret':raw_input('Provide oauth secret:\n>> ')
          }
f = flickr.FlickrAPI(**tokens)
files = open(os.path.join(path,photofile), 'rb')
add_photo = f.post(params={'title':'Test Title!'}, files=files)
print(add_photo)  # Returns the photo id of the newly added photo
