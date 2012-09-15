'''uploads photos to flickr and records the photo_id in the database.'''
import os,flickr,sqlite3
from flickr_auth import getconfig

def postphotos(conn,path,flickrAPIobj):
    '''posts photos to flickr according to database records found via conn. Path is the parent directory of the images.
    flickrAPIobj is a pre-authenticated object for interfacing with the Flickr API (using someone else's library).'''
    f = flickrAPIobj #shortened name.
    c = conn.cursor()
    counter = 0
    tags = ['Philippines','Botany','Asia','plants','specimens','filibot']
    with conn:
        data = c.execute('''select p.FILEPATH,f.FAMILY,p.GENUS,p.SPECIES,p.ALT_GENUS,p.ALT_SPECIES
                            from PLANTS p,REF_FAM f where f.F_ID = p.F_ID''').fetchmany(10)
        for row in data:
            counter += 1
            filepath = os.path.normpath(os.path.join(path,row[0].lstrip('/'))) #normalize filepath
            title = os.path.splitext(os.path.split(row[0])[-1])[0] #separate the title from the filepath
            try: 
                extratags = [str(i) for i in row[1:]]
                itags = ' '.join(tags.extend(extratags)) #coerce unicode
            except Exception as e:
                return extratags,e
            print(filepath) #debugging
            print(title)
            fil = open(filepath, 'rb')
            photo_id = f.post(params={'title':title,'tags':itags}, files=fil)
            print("Posted %s to flickr. Photo ID is %s"%(filepath,photo_id)) #debugging
            c.execute('''update PLANTS set FLICKR_ID = ? where FILEPATH = ?''',(photo_id,row[0]))
            if counter == 2:
                conn.commit()
                counter == 0
            else: pass

if __name__ == "__main__":
    cfg = getconfig()
    path = os.path.expanduser(r'~\My Documents\filibot\static')
    photofile = "test_photo.jpg"
    tokens = {'api_key':cfg['api_key'],
              'api_secret':cfg['secret'],
              'oauth_token':raw_input('Provide oauth token:\n>> '),
              'oauth_token_secret':raw_input('Provide oauth secret:\n>> ')
              }
    f = flickr.FlickrAPI(**tokens)
    #db stuff
    conn = sqlite3.connect("plants.sqlite")
    extratags,e = postphotos(conn,path,f)
    




####===============Attempt 1 (failed)=========================
##import httplib2,time
##import oauth2 as oauth
##from flickr_auth import getconfig
##url = 'http://api.flickr.com/services/upload'
###url = 'http://api.flickr.com/services/rest'
##cfg = getconfig()
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

####===============Attempt 2 (failed)=========================
##access_token = {}
##access_token['user_nsid'] = '85725978@N07'
##access_token['oauth_token_secret'] = '907be36bc82e0c36'
##import os
##import flickr_api as f
##path = os.path.expanduser(r'~\My Documents\filibot\data')
##photofile = "test_photo.jpg"
##f.set_auth_handler('tokens.cfg') #file containing api keys and auth tokens.
##user = f.test.login()
###f.upload(photo_file=os.path.join(path,photofile), title="Test Automated Upload")
