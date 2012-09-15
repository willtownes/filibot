'''uploads photos to flickr and records the photo_id in the database.'''
import os,flickr,sqlite3,logging,sys
from flickr_auth import getconfig

def makelogger(filename='log.txt'):
    '''returns a logger object that will write to specified file.
    Remember to call logging.shutdown() or log.removeHandler() to
    remove the lock on the log file at the end of logging.'''
    log = logging.getLogger('log')
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(filename)
    logfrmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(logfrmt)
    log.addHandler(fh)
    log.info("Starting the log...")
    return log

def postphotos(conn,path,flickrAPIobj):
    '''posts photos to flickr according to database records found via conn. Path is the parent directory of the images.
    flickrAPIobj is a pre-authenticated object for interfacing with the Flickr API (using someone else's library).'''
    f = flickrAPIobj #shortened name.
    c = conn.cursor()
    tags = ['Philippines','Botany','Asia','plants','specimens','filibot']
    log = makelogger()
    counter = 0
    try:
        data = c.execute('''select p.FILEPATH,f.FAMILY,p.GENUS,p.SPECIES,p.ALT_GENUS,p.ALT_SPECIES
                            from PLANTS p,REF_FAM f where f.F_ID = p.F_ID and p.FLICKR_ID is NULL''')
        for row in data:
            counter += 1
            print(counter)
            filepath = os.path.normpath(os.path.join(path,row[0].lstrip('/'))) #normalize filepath
            title = str(os.path.splitext(os.path.split(row[0])[-1])[0]) #separate the title from the filepath
            itags = str(' '.join(tags+list(filter(None,row[1:])))) #filters out None types
            fil = open(filepath, 'rb')
            photo_id = f.post(params={'title':title,'tags':itags}, files=fil) #this is actually a dictionary.
            if photo_id['stat'] != 'ok':
                log.error("Failed to post %s to flickr, because of flickr error %s"%(row[0],str(photo_id)))
            else:
                log.info("Posted %s to flickr. Photo ID is %s"%(row[0],photo_id['photoid'])) #debugging
                c.execute('''update PLANTS set FLICKR_ID = ? where FILEPATH = ?''',(photo_id['photoid'],row[0]))
    except Exception as e:
        log.exception(e)
    finally:
        conn.commit()
        log.info("Process ended")
        logging.shutdown()
        fil.close()
        
if __name__ == "__main__":
    cfg = getconfig()
    path = os.path.expanduser(r'~\My Documents\filibot\static')
    photofile = "test_photo.jpg"
    tokens = {'api_key':cfg['api_key'],
              'api_secret':cfg['secret'],
              'oauth_token': raw_input('Provide oauth token:\n>> '),
              'oauth_token_secret': raw_input('Provide oauth secret:\n>> ')
              }
    f = flickr.FlickrAPI(**tokens)
    #db stuff
    conn = sqlite3.connect("plants.sqlite")
    with conn:
        postphotos(conn,path,f)
