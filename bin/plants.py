import os,csv,shelve

class plantdb(object):
    '''a class wrapper around the shelve database containing the information about the plant image files'''
    #most methods operate under the assumption that the db connection is always closed.
    def __init__(self,csvpath,shelf):#since it is quick and easy, I am just going to always regenerate the db from the CSV each time the app is run.
        '''generates (or re-generates) the db "shelf" at specified path from specified CSV path.'''
        reader = csv.DictReader(open(csvpath,'rU'))
        self.records = 0
        self.dbpath = shelf
        try:
            self.db=shelve.open(self.dbpath)
            for row in reader:
                self.records += 1
                self.db[str(self.records)] = row
        except:
            print("Exception occurred at row %d"%self.records)
        finally:
            self.db.close()
        
    def dbopen(self):
        '''opens the underlying shelve database connection'''
        self.db = shelve.open(self.dbpath)
        
    def dbclose(self):
        '''closes the underlying shelve database'''
        self.db.close()

    def getinfo(self):
        '''extracts a list of unique family,genus,species tuples from the passed-in open shelve db object'''
        try:
            self.dbopen()
            d = self.db
            self.fgs = list(set([(d[i]['family'],d[i]['genus'],d[i]['species']) for i in d]))
            (self.fams,self.gens,self.specs) = [set(i) for i in zip(*self.fgs)] #unzip expression
        finally:
            self.dbclose()
            
    def getfamilies(self):
        '''returns a list of familes available'''
        return self.fams
    
    def getgenera(self,family):
        '''returns a list of genera falling under the specified family'''
        return sorted([i[1] for i in self.fgs if i[0] == family])

    def getspecies(self,genus):
        '''returns a list of species falling under the specified genus'''
        return sorted([i[2] for i in self.fgs if i[1] == genus])
            
    def getfiles(self,genus,species):
        '''returns a list of filename,filepath tuples corresponding to the specified species'''
        try:
            self.dbopen()
            d = self.db
            files = sorted([(d[i]['filename'],d[i]['filepath']) for i in d if d[i]['species'] == species and d[i]['genus'] == genus])
        finally:
            self.dbclose()
        return files
            

    #code these later
    #def __enter__():
    #def __exit__():

if __name__ == "__main__":
    print('plants.py being run in %s'%os.getcwd())
    p = plantdb('content_inventory.csv','plants.db')
    p.getinfo()
    print('There were %d unique families found'%len(p.fams))
    print('There were %d unique genera found'%len(p.gens))
    print('There were %d unique species found'%len(p.specs))
    p.dbclose()
    
    
