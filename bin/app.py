import web,os,plants

urls = ('/(.*)/','redirect',
        '/','index',
        '/tagalog(?:.htm)*.*','tagalog')

app = web.application(urls,globals())
try:
    p = plants.PlantDB()
    families = p.getFamilies()
except:
    print("database not found! proceeding with sample data")
    families = ['Acanthaceae','Aceraceae','Actinidiaceae']
render = web.template.render('templates/')

class redirect(object):
    def GET(self,path):
        web.seeother('/'+path)

class index(object):
    def GET(self):
        return render.index(families)

class tagalog(object):
    def GET(self):
        return render.tagalog(families)
        
if __name__ == "__main__":
    app.run()
