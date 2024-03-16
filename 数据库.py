import csv
import sqlite3


conn = sqlite3.connect('model.db')


cs = conn.cursor()
cs.execute('''create table books(
            name text not null ,
            image text,
            class text,
            produce_date text,
            visitors text,
            fix_price text,
            ratio text,
            score text,
            reference_price text,
            current_price text
            
            
            
)''')

mybooklist = []

with open('模型_top300-2.csv',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        #print(row.encode('gbk', errors='ignore'))

        cs.execute(f'insert into books values("{row[0]}","{row[1]}","{row[2]}","{row[3]}","{row[4]}","{row[5]}","{row[6]}","{row[7]}","{row[8]}","{row[9]}")')
    conn.commit()
conn.close()

