import sqlite3 as sql
from datetime import datetime

class Database:
    def __init__(self, db_name='db.sqlite3'):
        self.con = sql.connect(db_name)
        print('connected to dbase')

    def close(self):
        self.con.close()
        print('database disconnected')
    def create_result_table(self):
        query = "CREATE TABLE results (Sno INTEGER PRIMARY KEY AUTOINCREMENT,userid INTEGER ,DATE_TIME TEXT ,email TEXT ,no_of_emails INTEGER , no_of_spams INTEGER, no_of_hams INTEGER , hit_ratio FLOAT )"
        try:
            self.con.execute(query)
            print('Table created')
        except Exception as e:
            print(f'error->{e}')

    def add_results(self,userid,email,no_of_mails,no_of_spams,no_of_hams):
        hit_ratio = (no_of_spams*100)/no_of_mails
        date= datetime.now()
        query = f"INSERT into results values( null,'{userid}','{date}' ,'{email}','{no_of_mails}','{no_of_spams}','{no_of_hams}','{hit_ratio}')"
        try:
            self.con.execute(query)
            self.con.commit()
            print('success')

        except Exception as e:
            print(query)
            print(f'error->{e}')

    def create_history_table(self):
        query = "CREATE TABLE history(Sno integer primary key AUTOINCREMENT,userid integer,Subject TEXT,email TEXT unique,Type_of_mail TEXT)"
        try:
            self.con.execute(query)
            print('Table created')
        except Exception as e:
            print(f'error->{e}')

    def add_history(self, userid, emails, subject_of_mails, type_of_mail):
        query = f"INSERT into history values( null,'{userid}', '{subject_of_mails}','{emails}','{type_of_mail}')"
        try:
            self.con.execute(query)
            self.con.commit()
            print('Success')
        except Exception as e:
            print(query)
            print(f'error->{e}')
    def get_results(self):
        query = "select * from results"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f'error->{e}')
            return None
    def get_history(self):
        query = "select * from history"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f'error->{e}')
            return None

    def create_user_table(self):
        query = "CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT,user TEXT,email TEXT unique ,password TEXT)"
        try:
            self.con.execute(query)
            print('Table created')
        except Exception as e:
            print(f'error->{e}')

    def add_user(self, username, email, password):
        query = f"INSERT into user values( null, '{username}','{email}','{password}')"
        try:
            self.con.execute(query)
            self.con.commit()
            print('success')

        except Exception as e:
            print(f'error->{e}')

    def get_user(self):
        query = "select * from user"
        try:
            result = self.con.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f'error->{e}')
            return None
