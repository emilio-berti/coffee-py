import pandas as pd
import psycopg2 as psy

with open('password') as pwd:
    pwd = pwd.readlines()[0].replace('\n', '')

conn = psy.connect(dbname = 'coffee', user = 'coffeepi', password = pwd)
curs = conn.cursor()
curs.execute('''
    SELECT *, balance - due AS total FROM (
        SELECT username, count(*)*.4 AS due, balance FROM log 
            LEFT JOIN balance USING (username)
        GROUP BY log.username, balance
    ) AS foo;
''')

total = curs.fetchall()
balance = pd.DataFrame({
    'name': [total[i][0] for i in range(len(total))],
    'balance': [-total[i][1] if total[i][3] is None else total[i][3] for i in range(len(total))]
})

# get names missing in _balance_ and that will be added.
curs.execute('SELECT DISTINCT username FROM balance;')
all_names = curs.fetchall()
all_names = [all_names[i][0] for i in range(len(all_names))]
to_add = list({x for x in balance['name'].tolist()}.difference({x for x in all_names}))
# add missing names
for x in to_add:
    curs.execute('''
             INSERT INTO balance 
             (username, balance) 
             VALUES ('{}', {});
         '''.format(x, 0))

conn.commit()

# add the rest
for i in balance.index.tolist():
    # add the rest
    curs.execute('''
     UPDATE balance
     SET balance = {}
     WHERE username = '{}';
                 '''
     .format(balance.iloc[i]['balance'],
             balance.iloc[i]['name']))

conn.commit()

# reset logs to null
curs.execute('DELETE FROM log WHERE no > 0')
conn.commit()

conn.close()

print('Balance updated to:\n', balance)