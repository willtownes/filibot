'''
This is a script to authenticate to flickr and get an auth token.
Much of the authentication code borrows heavily from:
https://github.com/simplegeo/python-oauth2#readme
http://mkelsey.com/2011/07/03/Flickr-oAuth-Python-Example.html
'''
import webbrowser,ConfigParser,os,urlparse,time,httplib2
import oauth2 as oauth

#global variables
configdefault = "flickr.cfg"
callback_url = "https://github.com/willtownes" #fake callback URL until actual website available
request_token_url = "http://www.flickr.com/services/oauth/request_token"
authorize_url = 'http://www.flickr.com/services/oauth/authorize'
access_token_url = 'http://www.flickr.com/services/oauth/access_token'
params = {'oauth_nonce': oauth.generate_nonce(),
          'oauth_timestamp': int(time.time()),
          'oauth_signature_method':'HMAC-SHA1',
          'oauth_version': "1.0",
          'oauth_callback':callback_url         
          }

def makeconfig1(key,secret,configfile=configdefault):
    '''inserts the provided API key and secret into a configuration file
    for later use'''
    cfg = ConfigParser.ConfigParser()
    cfg.add_section('Flickr_API')
    cfg.set('Flickr_API','api_key',key)
    cfg.set('Flickr_API','secret',secret)
    with open(configfile,'wb') as ofile:
        cfg.write(ofile)

def getconfig(configfile=configdefault):
    '''gets the API key and secret from the config file'''
    config = ConfigParser.ConfigParser()
    config.read(configfile)
    params = {}
    params['api_key'] = config.get('Flickr_API','api_key')
    params['secret'] = config.get('Flickr_API','secret')
    return params

def getreqtoken(consumer,url=request_token_url,params=params):
    '''gets the request token and secret from Flickr. This is a temporary token that is used for 
    having the user authorize an access token and to sign the request to obtain said access token.'''
    params['oauth_consumer_key'] = consumer.key #add to parameters dictionary
    req = oauth.Request(method='GET',url=request_token_url,parameters=params)
    signature = oauth.SignatureMethod_HMAC_SHA1().sign(req,consumer,None)
    req['oauth_signature'] = signature
    #print(req.to_url()) #debugging
    resp, content = httplib2.Http().request(req.to_url(),"GET")
    if resp['status'] != '200': raise Exception("Invalid response %s." % resp['status'])
    else: return dict(urlparse.parse_qsl(content))

def redirectuser(token,url=authorize_url):
    '''Redirect the user to the flickr website to authorize this app'''
    webbrowser.open(urlparse.urljoin(url,"?oauth_token=%s"%token['oauth_token']))

def getaccesstoken(consumer,oauth_token,oauth_secret,oauth_verifier,url=access_token_url):
    '''Once the consumer has redirected the user back to the oauth_callback
     URL you can request the access token the user has approved. You use the 
     request token to sign this request. After this is done you throw away the
     request token and use the access token returned. You should store this 
     access token somewhere safe, like a database, for future use.'''
    token = oauth.Token(oauth_token,oauth_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer,token)
    resp, content = client.request(access_token_url, "POST")
    if resp['status'] != '200': raise Exception("Invalid response %s." % resp['status'])
    else: return dict(urlparse.parse_qsl(content))

def authflow():
    '''top-level function to run through the authentication flow if the user doesn't already have an access token.
    Depends on a bunch of global variables!'''
    if not os.path.exists(configdefault):
        key = raw_input("Provide the API key: \n> ")
        secret = raw_input("Provide the secret: \n> ")
        makeconfig1(key,secret)
    cfg = getconfig() #this is a dictionary
    consumer = oauth.Consumer(key=cfg['api_key'],secret=cfg['secret'])
    request_token = getreqtoken(consumer) #this is a dictionary
    print("Request Token:")
    print("    - oauth_token        = %s" % request_token['oauth_token'])
    print("    - oauth_token_secret = %s\n\n" % request_token['oauth_token_secret'])
    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    redirectuser(request_token)
    while accepted.lower() == 'n': accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')
    access_token = getaccesstoken(consumer,request_token['oauth_token'],request_token['oauth_token_secret'],oauth_verifier)
    print("Access Token:")
    print("    - oauth_token        = %s" % access_token['oauth_token'])
    print("    - oauth_token_secret = %s" % access_token['oauth_token_secret'])
    print("\nYou may now access protected resources using the access tokens above. Please store them someplace safe!\n" )
    return access_token
    
if __name__ == "__main__":
    #authentication stuff
    q = raw_input("If you know the access token, type 'Y', otherwise just hit enter:\n> ")
    if q.lower() == 'y':
        access_token = {}
        access_token['username'] = raw_input("Provide the username: ")
        access_token['oauth_token'] = raw_input("Provide the oauth token: ")
        access_token['user_nsid'] = raw_input("Provide the user_nsid: ")
        access_token['oauth_token_secret'] = raw_input("Provide the oauth token secret: ")
    else: access_token = authflow()
    
