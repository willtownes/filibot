CREATE TABLE PLANTS
(
P_ID INTEGER PRIMARY KEY AUTOINCREMENT,
H_ID INT,
HSERIAL TEXT,
T_ID INT,
F_ID INT NOT NULL,
GENUS TEXT,
SPECIES	TEXT,	
IS_FRAGMENT TEXT,
IS_DRAWING TEXT,
INFO	TEXT,
SUBSPECIES	TEXT,
VARIETY	TEXT,
ALT_INFO	TEXT,
ALT_GENUS	TEXT,
ALT_SPECIES	TEXT,	
ALT_TYPE	TEXT,	
YR	INT,
FILEPATH TEXT NOT NULL UNIQUE,
FILETYPE TEXT NOT NULL,
FLICKR_ID TEXT,
NOTES	TEXT,
LAST_UPDATE	DATE DEFAULT CURRENT_DATE, URL text, LAT real, LON real,
FOREIGN KEY(H_ID) REFERENCES REF_HERB(H_ID),
FOREIGN KEY(T_ID) REFERENCES REF_TYPES(T_ID),
FOREIGN KEY(F_ID) REFERENCES REF_FAM(F_ID),
FOREIGN KEY(IS_FRAGMENT) REFERENCES REF_YN(YN_VAL),
FOREIGN KEY(IS_DRAWING) REFERENCES REF_YN(YN_VAL)
);
CREATE TABLE REF_FAM (
f_id integer primary key autoincrement,
family text not null,
notes text,
alt_family text,
subfamily text, flickr_id text);
CREATE TABLE REF_HERB
(
H_ID INTEGER PRIMARY KEY AUTOINCREMENT,
HCODE TEXT NOT NULL UNIQUE,
HNAME TEXT NOT NULL,
CITY TEXT,
COUNTRY TEXT,
URL TEXT
);
CREATE TABLE REF_TYPES
(
T_ID INTEGER PRIMARY KEY AUTOINCREMENT,
TCODE TEXT NOT NULL UNIQUE,
TNAME TEXT NOT NULL,
NOTES TEXT
);
CREATE TABLE REF_YN
(
YN_VAL TEXT NOT NULL UNIQUE
);
CREATE TABLE SCHEMA_CHANGES
(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
MAJOR_REL_NUM TEXT NOT NULL,
MINOR_REL_NUM TEXT NOT NULL,
POINT_REL_NUM TEXT NOT NULL,
SCRIPT_NAME TEXT NOT NULL,
UPDATE_DATE DATE DEFAULT CURRENT_TIMESTAMP
);