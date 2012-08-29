'''
Generates the SQLITE3 database from the following CSV files:
fams.csv
herbarium_codes.csv
primary.csv
typecodes.csv
'''
import sqlite3 as sq
import csv,os,time

def str2null(string):
    '''returns None if the string is empty, otherwise the string itself'''
    if string == "": return None
    else: return string

def dbconnect(dbname="plants.sqlite"):
    '''returns database connection object to specified name'''
    return sq.connect(dbname)

def dbmaker(conn,schemafile="dbschema.sql"):
    '''makes a sqlite database called <<dbname>> given schemafile, returns connection object'''
    #alternative approach
    #os.system("sqlite3 {0} < {1}".format(dbname,schemafile))
    with conn:
        c = conn.cursor()
        c.executescript(open(schemafile).read())
        print("database schema created successfully")
        return conn

def make_ref_tbl(conn,csvfile,rtable):
    '''adds data from csv file into reference table'''
    reader = csv.reader(open(csvfile))
    fieldnames = next(reader) #assuming column headers in first row
    sql_cols = ",".join(fieldnames) #autogenerate column names from CSV field names
    sql_vars = ",".join(["?"]*len(fieldnames))
    query = "insert into {0} ({1}) values ({2})".format(rtable,sql_cols,sql_vars)
    with conn:
        c = conn.cursor()
        for row in reader:
            row = map(str2null,row) #switch all empty strings with NULLs
            #execute insert statement
            try: c.execute(query,row)
            except Exception as e:
                print(query)
                print(row) #for debugging
                raise e
        conn.commit()
        return conn

def make_primary_tbl(conn,csvfile,table):
    '''adds data from csv file into primary table'''
    reader = csv.DictReader(open(csvfile))
    with conn:
        c = conn.cursor()
        for irow in reader:
            row = dict((i,str2null(irow[i])) for i in irow) #convert all empty strings to NULL
            #replacing codes with IDs to reference tables (to utilize foreign keys)
            row['F_ID'] = c.execute("select F_ID from REF_FAM where FAMILY = ?",(row['FAMILY'],)).fetchone()[0]
            del(row['FAMILY']) #family code is never null

            if row['HCODE']: #herbarium code could be null
                row['H_ID'] = c.execute("select H_ID from REF_HERB where HCODE = ?",(row['HCODE'],)).fetchone()[0]
            else: row['H_ID'] = None
            del(row['HCODE'])

            if row['TCODE']: #type code could be null
                row['T_ID'] = c.execute("select T_ID from REF_TYPES where TCODE = ?",(row['TCODE'],)).fetchone()[0]
            else: row['T_ID'] = None
            del(row['TCODE'])
            
            sql_cols = ",".join(row.keys()) #autogenerate column names from modified list of CSV field names
            sql_vars = ",".join([":"+i for i in row.keys()])
            query = "insert into {0} ({1}) values ({2})".format(table,sql_cols,sql_vars)
            try: c.execute(query,row)
            except Exception as e:
                print(query)
                print(row) #for debugging
                raise e
        conn.commit()
        return conn

def backup(conn,ofile=None):
    '''backs up the database connected by conn to the specified ofile path.
    If no ofile path is provided, the default is to use the system time
    with suffix ".bak"'''
    if not ofile: ofile = str(int(time.time()))+'.bak'
    with conn:
        with open(ofile,'w') as f:
            for line in conn.iterdump():
                f.write('%s\n' % line)
            print("backup to %s completed successfully!"%ofile)
                
if __name__ == "__main__":
    #self test code
    if os.path.exists("plants.sqlite"): os.remove("plants.sqlite")
    conn = dbconnect()
    conn = dbmaker(conn)
    csvs = ["fams.csv","herbarium_codes.csv","typecodes.csv"]
    tbls = ["REF_FAM","REF_HERB","REF_TYPES"]
    for i in zip(csvs,tbls):
        conn = make_ref_tbl(conn,*i)
    conn = make_primary_tbl(conn,"primary.csv","PLANTS")
    c = conn.cursor()
    count = c.execute("select count(*) from plants").fetchone()
    print("Detected %d records in the PLANTS table"%count)
    backup(conn) #generates backup with timestamp as filename
    conn.close()
    raw_input() #comment out later, just hangs to display results to user.
    
