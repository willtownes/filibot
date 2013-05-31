'''
This is the data model part of the app.
'''
import os,web

class PlantDB(object):
    '''a class wrapper around the database'''
    def __init__(self,dbname='data/plants.sqlite',dbtype='sqlite'):
        self.db = web.database(dbn=dbtype,db=dbname)
        self.families = None
    def getFamilies(self):
        '''return list of family names'''
        if not self.families: #caching
            sql = "select distinct family from ref_fam order by family"
            self.families = [i.family for i in self.db.query(sql)]
        return self.families

if __name__ == "__main__": #self-testing stuff for when module is run alone
    print('plants.py being run in %s'%os.getcwd())
    p = PlantDB()
    families = p.getFamilies()
    print('There were %d unique families found'%len(p.families))
    print('here are the first ten families:')
    for f in families[:10]:
        print(f)