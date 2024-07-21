import sqlite3
import pathlib
import os

PROJECT_PATH = pathlib.Path(__file__).parent.resolve()


class Database:
    def __init__(self, database_name, database_tables, database_cols) -> None:
        self.database_name = database_name
        self.database_tables = database_tables
        self.database_cols = database_cols

    def __str__(self) -> str:
        return f"Database object: {self.database_name} with the following tables {self.database_tables}"


#Update database instances to have two one for db_users and one for db_doctors
db_users = Database("users.db", ["user", "docs"], ["user_name", "pwd"])


def create_new_table(db_name, db_table):
    con = sqlite3.connect(f"{PROJECT_PATH}\\{db_name}")
    cur = con.cursor()
    res = cur.execute(
        f"""CREATE TABLE {db_table} (
                    doc_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    full_name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    user_id INTEGER UNIQUE NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user(user_id)
                    );
                    """
    )


def get_data_from_db(db_name, db_table):
    con = sqlite3.connect(f"{PROJECT_PATH}\\{db_name}")
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM {db_table}")
    return res


def register_new_user(username, pwd):

    try:
        con = sqlite3.connect(f"{PROJECT_PATH}\\{db_users.database_name}")
        cur = con.cursor()
        sql_command = f"INSERT INTO {db_users.database_tables[0]} ({db_users.database_cols[0]},{db_users.database_cols[1]}) VALUES (?,?)"
        print(
            f"Adding new user: {username} to database"
        )  # allows duplicated rows because only primary key needs to be unique
        cur.execute(sql_command, (username, pwd))
        con.commit()
        con.close()
        return True
    except:
        print("Connection with database did not work")
        return False


def delete_user(username, pwd):
    try:
        con = sqlite3.connect(f"{PROJECT_PATH}\\{db_users.database_name}")
        cur = con.cursor()
        sql_command = f"DELETE FROM {db_users.database_tables[0]} WHERE {db_users.database_cols[0]} = ? AND {db_users.database_cols[1]} = ?"
        print(f"Deleting user: {username} from database")
        cur.execute(sql_command, (username, pwd))
        con.commit()
        con.close()
        return True
    except:
        print("Connection with database did not work")
        return False


def register_new_doctor(doc_name, doc_address, doc_specialization, user_id):
    try:
        con = sqlite3.connect(f"{PROJECT_PATH}\\{db_users.database_name}")
        cur = con.cursor()

        #ToDO user_id comes from username i.e. email but should be the primary key instead
        sql_command = f"""INSERT INTO TABLE {db_users.database_tables[1]} 
            (full_name, address, specialization, user_id) VALUES(?,?,?,?);"""
        cur.execute(sql_command, (doc_name, doc_address, doc_specialization, user_id))
        print(f"Adding new doctor: {doc_name} from database with user_id")
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

    return list_dict


def check_user_exists(username, pwd):

    db_entries = convert_tuples_dict(get_data_from_db("users.db", "user"))
    for db_entry in db_entries:
        if (db_entry["user_name"] == username) and (db_entry["pwd"] == pwd):
            print(f"User {username} already exists")
            return True
    print(f"User {username} does not exist in the database")
    return False


def get_dbs() -> list:

    dbs_list = [db_file for db_file in os.listdir(PROJECT_PATH) if ".db" in db_file]
    return dbs_list


def get_users():

    return convert_tuples_dict(
        get_data_from_db(db_users.database_name, db_users.database_tables[0])
    )


def get_doctors():
    return convert_tuples_dict(
        get_data_from_db(db_users.database_name, db_users.database_tables[1])
    )
