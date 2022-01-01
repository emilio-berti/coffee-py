import psycopg2 as psy

with open('password') as pwd:
	pwd = pwd.readlines()[0].replace('\n', '')

conn = psy.connect(dbname = 'coffee', user = 'coffeepi', password = pwd)
print('Connection to database "coffee" established')
curs = conn.cursor()

curs.execute("SELECT relname FROM pg_class WHERE relkind = 'r' and relname !~ '^(pg_|sql_)';")
tables = curs.fetchall()
tables = list(map(lambda x: x[0], tables))

if len(tables) == 0 or 'log' not in tables:
    curs.execute('''
        CREATE TABLE log (no SERIAL PRIMARY KEY,
                                            event TIMESTAMP,
                                            username TEXT);
    ''')
conn.commit()
print('Table "log" created')
# example of loggin event:
# INSERT INTO log (event, username) VALUES (now(), 'eb97ziwi');

if len(tables) == 0 or 'balance' not in tables:
    curs.execute('''
        CREATE TABLE balance (no SERIAL PRIMARY KEY,
                              username TEXT,
                              balance FLOAT);
    ''')
conn.commit()
print('Table "balance" created')