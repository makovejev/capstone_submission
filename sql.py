import sqlite3
from sqlite3 import Error
import pandas as pd


def create_connection(path):
    try:
        connection = sqlite3.connect(path)
        print('Connection to SQLite DB successful')
        return connection
    except Error as e:
        print(e)
        return None

connection = create_connection('/home/sergej/sandbox/ds/sql_files/file1.sql')
cursor = connection.cursor()

df = pd.read_csv('Spacex.csv')
df.to_sql('SPACEXTBL', connection, index=False, if_exists='replace', method="multi")

# 1
cursor.execute("SELECT distinct(Launch_Site) FROM SPACEXTBL")
for r in cursor.fetchall(): print(r)

# 2
cursor.execute('SELECT * FROM SPACEXTBL where Launch_Site like "CCA%" limit 5')
for r in cursor.fetchall(): print(r)

# 3
cursor.execute('SELECT sum(PAYLOAD_MASS__KG_) FROM SPACEXTBL where Customer = "NASA (CRS)"')
for r in cursor.fetchall(): print(r)

# 4
cursor.execute('SELECT avg(PAYLOAD_MASS__KG_) FROM SPACEXTBL where Booster_Version = "F9 v1.1"')
for r in cursor.fetchall(): print(r)

# 5
cursor.execute('SELECT min(Date) FROM SPACEXTBL where "Landing _Outcome" = "Success (ground pad)"')
for r in cursor.fetchall(): print(r)

# 6
cursor.execute('SELECT Booster_Version FROM SPACEXTBL '
               'where "Landing _Outcome" = "Success (drone ship)" and PAYLOAD_MASS__KG_ > 4000 and PAYLOAD_MASS__KG_ < 6000')
for r in cursor.fetchall(): print(r)

# 7
cursor.execute('SELECT count(*) FROM SPACEXTBL where "Landing _Outcome" like "Success%"')
for r in cursor.fetchall(): print(r)
cursor.execute('SELECT count(*) FROM SPACEXTBL where "Landing _Outcome" like "Failure%"')
for r in cursor.fetchall(): print(r)

# 8
cursor.execute('SELECT Booster_Version FROM SPACEXTBL '
               'where PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) from SPACEXTBL)')
for r in cursor.fetchall(): print(r)

# 9
cursor.execute('SELECT Date, "Landing _Outcome", Booster_Version, Launch_Site FROM SPACEXTBL '
               'where "Landing _Outcome" = "Failure (drone ship)" and Date like "%-2015"')
for r in cursor.fetchall(): print(r)


# 10
cursor.execute('ALTER TABLE SPACEXTBL ADD date2 date')
cursor.execute('update SPACEXTBL set date2=strftime("%Y/%m/%d",datetime(substr(Date, 7, 4) || "-" || substr(Date, 4, 2) || "-" || substr(Date, 1, 2)))')
cursor.execute('SELECT "Landing _Outcome", count("Landing _Outcome") as count FROM SPACEXTBL '
               'where date2 between "2010-04-06" and "2017-03-20" '
               'GROUP BY "Landing _Outcome" order by count DESC')
for r in cursor.fetchall(): print(r)