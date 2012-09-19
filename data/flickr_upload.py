'''uploads photos to flickr and records the photo_id in the database.'''
import os,flickr,sqlite3,logging,sys,csv,httplib
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

def postphotos(conn,path,flickrAPIobj,csvlocation):
    '''posts photos to flickr according to database records found via conn. Path is the parent directory of the images.
    flickrAPIobj is a pre-authenticated object for interfacing with the Flickr API (using someone else's library).'''
    f = flickrAPIobj #shortened name.
    c = conn.cursor()
    tags = ['Philippines','Botany','Asia','plants','specimens','filibot']
    log = makelogger(filename='flickr_log.txt')
    counter = 0
    ofile = open(csvlocation,'wb')
    resfile = csv.writer(ofile)
    resfile.writerow(("Filepath","Flickr ID"))
    try:
        for row in c.execute('''select p.FILEPATH,f.FAMILY,p.GENUS,p.SPECIES,p.ALT_GENUS,p.ALT_SPECIES
                            from PLANTS p,REF_FAM f where f.F_ID = p.F_ID and p.FILETYPE != 'BMP'
                            and p.FLICKR_ID is NULL'''): #excluding BMP files temporarily since they are really large.
            counter += 1
            print(counter)
            filepath = os.path.normpath(os.path.join(path,row[0].lstrip('/'))) #normalize filepath
            title = str(os.path.splitext(os.path.split(row[0])[-1])[0]) #separate the title from the filepath
            itags = str(' '.join(tags+list(filter(None,row[1:])))) #filters out None types
            if not os.path.exists(filepath):
                photo_id = {'stat':'file not found'}
            else:
                with open(filepath, 'rb') as fil:
                    #the photo_id response is actually a dictionary.
                    try: photo_id = f.post(params={'title':title,'tags':itags}, files=fil)
                    #this kind of exception usually means the file is too large.
                    except httplib.BadStatusLine: photo_id = {'stat' : "BadStatusLine exception"}
            if photo_id['stat'] != 'ok':
                log.error("Failed to post %s to flickr, because of error %s"%(row[0],str(photo_id)))
            else:
                log.info("Posted %s to flickr. Photo ID is %s"%(row[0],photo_id['photoid'])) #debugging
                resfile.writerow((row[0],photo_id['photoid']))
    except Exception as e: #unanticipated exceptions, break out of the loop and record details.
        log.exception(e)
        log.info("Filepath: %s"%filepath)
        log.info("Title: %s"%title)
        log.info("itags: %s"%itags)
    finally:
        ofile.close() #csvfile with results.
        log.info("Ended posting photos to flickr")
        logging.shutdown()

def insertids(conn,csvlocation):
    '''takes a CSV containing filepaths and flickr IDs and inserts records into the database'''
    log = makelogger(filename='database_log.txt')
    log.info("Starting process of extracting IDs from temporary CSV and inserting into database")
    c = conn.cursor()
    try:
        reader = csv.reader(open(csvlocation,'rb'))
        next(reader) #skip header row.
        for row in reader:
            c.execute('''update PLANTS set FLICKR_ID = ? where FILEPATH = ?''',(row[1],row[0]))
    except FlickrAPIError as e:
        log.exception(e.code)
        log.exception(e.msg)
    except Exception as e:
        log.exception(e)
    finally:
        conn.commit()
        log.info("Process ended")
        logging.shutdown()
        
if __name__ == "__main__":
    cfg = getconfig()
    if os.name.lower() == 'nt': #windows
        path = os.path.expanduser(r'~\My Documents\filibot\static')
    else: #mac
        path = os.path.expanduser(r'~/Documents/filibot/static')
    tokens = {'api_key':cfg['api_key'],
              'api_secret':cfg['secret'],
              'oauth_token': cfg['oauth_token'],
              'oauth_token_secret': cfg['oauth_secret']
              }
    f = flickr.FlickrAPI(**tokens)
    #db stuff
    csvlocation = 'results.csv'
    conn = sqlite3.connect("plants.sqlite")
    with conn:
        postphotos(conn,path,f,csvlocation)
        insertids(conn,csvlocation)
