import csv,sqlite3
with open('badfamilies.csv') as fams:
    reader = csv.DictReader(fams)
    rows = [row for row in reader]
conn = sqlite3.connect('plants.sqlite')
with conn:
    c = conn.cursor()
    for row in rows:
        id = int(row['F_ID'])
        c.execute('''update ref_fam set family=? where f_id=?''',(row['new name'],id))
        if row['alt family']: c.execute('''update ref_fam set alt_family=? where f_id=?''',(row['alt family'],id))
        if row['subfamily']: c.execute('''update ref_fam set subfamily=? where f_id=?''',(row['subfamily'],id))
    conn.commit()