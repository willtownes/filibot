import web,os
import plants
##NEED TO MOVE THE LOGIC OF MAPPING FAMILIES>GENERA>SPECIES INTO PLANTS.PY AND STORE IN NESTED DICTIONARIES.
##sorting is not working properly because of the dictionary conversions
##Adding index pictures, better html layout, etc
##Tagalog version of the site??


urls = ('/(.*)/','redirect',
        '/','index',
        '/(.+)/(.+)/(.+)','species',
        '/(.+)/(.+)','genus',
        '/(.+)','family')

app = web.application(urls,globals())
render = web.template.render('templates/')

#this part brings in the data from the CSV file and inserts it into a shelve db for later reference.
p = plants.plantdb('bin/content_inventory.csv','bin/plants.db')
p.getinfo()

class redirect(object):
    def GET(self,path):
        if path != 'static': #exception to redirect rule is when searching for static image directory
            web.seeother('/'+path)

class index(object):
    def GET(self):
        fnames = p.getfamilies()
        return render.index(fnames)

class family(object):
    def GET(self,fname):
        genera = dict((g,p.getspecies(g)) for g in p.getgenera(fname)) #dictionary mapping genera to lists of species names
        return render.family(fname,genera)

class genus(object):
    def GET(self,fname,gname):
        #species is a dictionary whose keys are the species name, and the contents are the filename,filepath tuples
        species = dict((s,p.getfiles(gname,s)) for s in p.getspecies(gname))
        return render.genus(fname,gname,species)

class species(object):
    def GET(self,fname,gname,sname):
        files = p.getfiles(gname,sname)
        return render.species(fname,gname,sname,files)

if __name__ == "__main__":
    app.run()
