'''Create photosets for each family and assign all images to a set. The Flickr API client is from:
https://github.com/michaelhelmick/python-flickr'''
import flickr,sqlite3,csv
from flickr_auth import getconfig
# given a single photo ID, create a photoset with specified name and print out the ID of the photoset

#photo ID: 8101132900
#set title: Actinidiaceae

def make_photosets(conn,flickrAPIobj,csvlocation):
    '''Create a photoset for each family and write out the flickr ID for the photoset to CSV file'''
    f = flickrAPIobj #shortened name.
    c = conn.cursor()
    ofile = open(csvlocation,'wb')
    resfile = csv.writer(ofile)
    resfile.writerow(("F_ID","P_ID","PHOTOSET_ID"))
    try:
        for row in c.execute('''SELECT f.f_id,f.family,f.subfamily, min(p.p_id),p.flickr_id from plants p, ref_fam f where p.f_id = f.f_id group by p.f_id'''):
            #print(row)
            if row[2] is None:
                name = row[1]
            else:
                name = row[1]+'-'+row[2]
            #print(name)
            params = {'title':name.encode('utf-8'),'primary_photo_id':row[4].encode('utf-8')}
            #print(params)
            set_id = f.post('flickr.photosets.create',params=params)
            if set_id['stat'] != 'ok':
                print("Failure to post for family: (%d,%s)"%(row[0],row[1]))
                break
            else:
                print(set_id)
                resfile.writerow((row[0],row[3],set_id['photoset']['id']))
    finally:
        ofile.close() #csvfile with results.

def insertids(conn,csvlocation):
    '''takes a CSV containing photoset IDs and family IDs and inserts the former ID into the database'''
    c = conn.cursor()
    reader = csv.reader(open(csvlocation,'rb'))
    next(reader) #skip header row.
    for row in reader:
        c.execute('''update REF_FAM set FLICKR_ID = ? where F_ID = ?''',(row[2],row[0]))
    conn.commit()

def photosIntoSets(conn,flickrAPIobj):
	'''once the photosets have all been created, inserts all the remaining plant photos into their family's set'''
	f = flickrAPIobj #shortened name.
	c = conn.cursor()
	counter = 0
	for row in c.execute('''SELECT p.flickr_id,f.flickr_id from plants p, ref_fam f where p.f_id=f.f_id order by f.family'''):
		params = {'photoset_id':row[1],'photo_id':row[0]}            	
        #print(params)
		try:
			set_id = f.post('flickr.photosets.addPhoto',params=params)
		except flickr.FlickrAuthError, e:
			pass
		counter += 1
		if counter % 10 == 0: print(counter)

if __name__ == "__main__":
    cfg = getconfig()
    tokens = {'api_key':cfg['api_key'],
              'api_secret':cfg['secret'],
              'oauth_token': cfg['oauth_token'],
              'oauth_token_secret': cfg['oauth_secret']
              }
    f = flickr.FlickrAPI(**tokens)
    #db stuff
    csvlocation = 'photoset_results.csv'
    conn = sqlite3.connect("plants.sqlite")
    with conn:
        #make_photosets(conn,f,csvlocation)
        #insertids(conn,csvlocation)
		photosIntoSets(conn,f)