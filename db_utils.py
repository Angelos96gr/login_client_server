import sqlite3
import pathlib
import os

PROJECT_PATH = pathlib.Path(__file__).parent.resolve()

class Database():
    def __init__(self, database_name, database_tables, database_cols) -> None:
        self.database_name = database_name
        self.database_tables = database_tables
        self.database_cols = database_cols

    def __str__(self) -> str:
        return f"Database object: {self.database_name} with the following tables {self.database_tables}"



db_doctors = Database("munich_docs.db", "docs", ["full_name", "address", "specialization"])
db_users = Database("users.db", "user", ["user_name", "pwd"])




def get_data_from_db(db_name, db_table):
    con = sqlite3.connect(f"{PROJECT_PATH}\\{db_name}")
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM {db_table}")
    return res


def register_new_user(user_name, pwd):
    
    try:
        con = sqlite3.connect(f"{PROJECT_PATH}\\{db_users.database_name}")
        cur = con.cursor()
        sql_command = f"INSERT INTO {db_users.database_tables} ({db_users.database_cols[0]},{db_users.database_cols[1]}) VALUES (?,?)"
        print(f"Adding new user: {user_name} to database") # allows duplicated rows because only primary key needs to be unique
        cur.execute(sql_command, (user_name, pwd))
        con.commit()
        con.close()
        return True
    except:
        print("Connection with database did not work")  
        return False



def convert_tuples_dict(res):

    dict_keys = [item[0] for item in res.description]
    list_tuples = res.fetchall()
    num_cols = list_tuples[0].__len__()

    list_dict = []
    for i, item in enumerate(list_tuples):
        # to do: make number of keys variable depending on the columns in the sql table
        temp_dict = {}
        for j in range(num_cols):
            temp_dict[dict_keys[j]] = item[j]
        
        list_dict.append(temp_dict)
    
    return(list_dict)

def login_user(user_name, pwd):
    pass #todo - check the user exists and the pwd, email are correct

def get_dbs() -> list:

    dbs_list = [db_file for db_file in os.listdir(PROJECT_PATH) if ".db" in db_file]
    return dbs_list


def get_users():

    return convert_tuples_dict(get_data_from_db(db_users.database_name, db_users.database_tables))


def get_doctors():
    return convert_tuples_dict(get_data_from_db(db_doctors.database_name, db_doctors.database_tables))



