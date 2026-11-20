import sqlite3
from pathlib import Path
from typing import Mapping
from platformdirs import user_config_dir

from flipper.consts import APP_AUTHOR, APP_NAME, DEF_TESTBANK, DEF_COURSES, DEF_AICHAT_CONFIG

CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
DATA_DIR = CONFIG_DIR / "data"

# if the data directory does not exist create it
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

VALID_DB_AND_TABLES: dict[str,list[str]] = {
    "education": ["testbank", "courses"],
    "configurations": ["ai_chat_config"],
} 

TABLE_DEFINITIONS: list[dict[str,str]] = [
    {"testbank": DEF_TESTBANK},
    {"courses": DEF_COURSES},
    {"ai_chat_config": DEF_AICHAT_CONFIG},
]



# TODO - Create database_item_Vx db versioning system to allow for future changes to db schema.
    # - DAS needs a create_db function which is passed a db_schema (e.g. testbank_schema_v1).
    # - ??? hold path to database in its own "type"???

class DataAccessService:
    """Provides database access services object 
    
    Args:
        database: filename of the database as string (e.g. "my_database.db")
        table_name: The name of the table contained within database (e.g. "testbank")
    
    Returns:
        None
    """

    def __init__(self, database: str, table_name: str):
        print(f"DAS: Initializing DAS for [{database}] and table [{table_name}]")
        # Ensure database is an approved database name
        if not VALID_DB_AND_TABLES.__contains__(database[:-3]):
            raise ValueError(f"Error: Provided database [{database}] is not a valid database")

        # Ensure database and table are a valid pair
        if table_name not in VALID_DB_AND_TABLES[database[:-3]]:
            raise ValueError(f"Error: [{table_name}] is not a valid table in [{database}]")


        # check to see if databse exists, if not create it
        self.database_path = DATA_DIR / database
        if not self.database_path.exists():
            print(f"DAS: Database [{self.database_path}] does not exist.. creating database")
            self.create_db(database)

        self.database = self.database_path

        # check to see if the database has the table
        if not self.hasTable(table_name):
            print(f"DAS: Table [{table_name}] does not exist.. creating table")
            self.create_table(table_name)

        #All checks complete, reassign database variable
        
        self.table_name = table_name

    def create_db(self, filename: str):
        # check file name extension, if not ending in '.db' raise exception
        if filename[-3:] != '.db':
            raise ValueError(f"DAS:Error: filename = {filename} must have the extension '.db'")
        
        # check if database already exists
        self.database_path = DATA_DIR / filename
        if self.database_path.exists():
            raise FileExistsError(f"DAS:Error: The database: {filename}, already exists")

        # create database
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("PRAGMA journal_mode = WAL")
        
        print(f"DAS: Database succesfully created at [{self.database_path}]")

    def create_table(self, table):
        print(f"DAS: Creating table [{table}]")
        table_definition = None

        for table_name in TABLE_DEFINITIONS:
            if table_name.__contains__(table):
                table_definition = table_name[table]

        if table_definition == None:
            raise ValueError(f"DAS:Error: Could not find definition for [{table}] table")

        # build table
        with sqlite3.connect(self.database_path) as conn:
            conn.execute(table_definition)

        print(f"DAS: table [{table}] succesfully created at [{self.database_path}] ")

    def hasTable(self, table_name) -> bool:
        print(f"DAS: Checking that table [{table_name}] exists in [{self.database}]")
        with sqlite3.connect(self.database_path) as conn:
            result = conn.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name = ?
                """, (table_name,)
            ).fetchone()
        return result is not None

    def get_all(self) -> list[sqlite3.Row]:
        with sqlite3.connect(self.database) as conn:
            conn.row_factory = sqlite3.Row
            result = conn.execute(f"SELECT * FROM {self.table_name}")
            return result.fetchall()

    def insert(self, data: dict):
        # build SQL strings
        columns = list(data.keys())
        values  = list(data.values())

        values_str = ", ".join("?" * len(values))
        columns_str= ", ".join(columns)
        sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({values_str})"

        
        with sqlite3.connect(self.database) as conn:
            conn.execute(sql, values)
            conn.commit()

    def get_row(self, identifier: tuple) -> tuple | None:
        if len(identifier) != 2:
            raise ValueError(f"DAS:Error: get_row() was called with an invalid condition [{identifier}]")
        
        row_identifier = identifier[0]
        identifier_val = identifier[1]
        with sqlite3.connect(self.database) as conn:
            return conn.execute(
                f"""
                SELECT *
                FROM {self.table_name}
                WHERE {row_identifier} = ?
                """,
                (identifier_val,),
            ).fetchone()

    def update_row(self, identifier: tuple[str, object], data: Mapping[str, object]) -> None:
        identifying_col, identifier_val = identifier
        cols = list(data.keys())
        vals = list(data.values())

        # Build SQL query
        set_clause = ", ".join(f"{col} = ?" for col in cols)
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {identifying_col} = ?"

        #send SQL query
        with sqlite3.connect(self.database) as conn:
            conn.execute(sql, vals + [identifier_val])
            conn.commit()

    """
    Count the number of rows where the conditions hold. 
    The conditions should be checked as valid by the service holding the DAS object

    Args:
        conditions: A dictionary where the key is the column name and the value is the checked for truth (exists)
    
    Returns:
        An integer representing the number of rows which have Column Name and Value defined in conditions as true.
    """
    def count_rows(self, identifier: tuple, conditions: Mapping | None = None) -> int:
        # set identifier variables
        identifying_col = str(identifier[0])
        identifier_val  = str(identifier[1])
        # Build SQL query
        if conditions == None:
            with sqlite3.connect(self.database) as conn:
                result = conn.execute(
                    f"SELECT COUNT(*) FROM {self.table_name} WHERE {identifying_col} = ?"
                    , (identifier_val,)).fetchone()
                return result[0]
            
        query_data = self.build_query_variables(conditions)
        condition_clause = " AND ".join(
            f"{col} = ?" for col in query_data["col_list"]
        )
        sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE {identifying_col} = ?"

        if condition_clause:
            sql += f" AND {condition_clause}"

        with sqlite3.connect(self.database) as conn:
            result = conn.execute(
                sql, [identifier_val, *query_data["val_list"]]
            ).fetchone()

        return result[0]


    def get_list(self, identifier: tuple, conditions: dict) -> list[int]:
        identifying_col, identifier_val = identifier
        query_data = self.build_query_variables(conditions)
        condition_clause = " AND ".join(
            f"{col} = ?" for col in query_data["col_list"]
        )

        sql = f"SELECT id FROM {self.table_name} WHERE {identifying_col} = ?"
        if condition_clause:
            sql += f" AND {condition_clause}"

        with sqlite3.connect(self.database) as conn:
            rows = conn.execute(
                sql, [identifier_val, *query_data["val_list"]]
            ).fetchall()

        return [row[0] for row in rows]

    def check_row(self, identifier: tuple, conditions: dict) -> bool:
        query_data = self.build_query_variables(conditions)
        condition_clause = " AND ".join(
            f"{col} = ?" for col in query_data["col_list"]
        )

        identifying_col, identifier_val = identifier

        sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE {identifying_col} = ?"
        if condition_clause:
            sql += f" AND {condition_clause}"

        with sqlite3.connect(self.database) as conn:
            result = conn.execute(
                sql, [identifier_val, *query_data["val_list"]]
            ).fetchone()

        return result is not None and result[0] > 0

    def check_col(self, row_id: int, column: str) -> bool:
        allowed = {
            "id", "is_valid", "course", "question", "answer",
            "f1", "f2", "f3", "correct", "attempts",
        }
        if column not in allowed:
            raise ValueError(f"Unknown column: {column}")

        with sqlite3.connect(self.database) as conn:
            result = conn.execute(
                f"""
                SELECT {column} IS NOT NULL AND {column} <> ''
                FROM {self.table_name}
                WHERE id = ?
                """,
                (row_id,),
            ).fetchone()

        return result is not None and bool(result[0])

    def build_query_variables(self, data: Mapping) -> dict[str, list]:
        result = {}

        #get col and val list
        result['col_list'] = list(data.keys())
        result['val_list'] = list(data.values())
        
        #Build sql query strings
        result['col_str']  = ", ".join(result['col_list'])
        result['val_str']  = ", ".join("?" * (len(result['val_list'])))

        return result 



# Old functions below

    # def invalid_count(self, course) -> int:
    #     with sqlite3.connect(self.database) as conn:
    #         cursor = conn.execute(
    #             """
    #             SELECT COUNT(*)
    #             FROM questions
    #             WHERE course = ?
    #             AND (
    #                 f1 IS NULL OR f1 = ''
    #                 OR f2 IS NULL OR f2 = ''
    #                 OR f3 IS NULL OR f3 = ''
    #             )
    #             """,
    #             (course,),
    #         ).fetchone()
    #     return cursor[0]

    # def total_count(self, course) -> int:
    #     with sqlite3.connect(self.database) as conn:
    #         cursor = conn.execute(
    #             """
    #             SELECT COUNT(*)
    #             FROM questions
    #             WHERE course = ?
    #             """,
    #             (course,),
    #         ).fetchone()
    #     return cursor[0]

    # # returns list of ids belonging to invalid entries and COURSE
    # def invalid_list(self, course) -> list[int]:
    #     with sqlite3.connect(self.database) as conn:
    #         cursor = conn.execute(
    #             """
    #             SELECT id
    #             FROM questions
    #             WHERE course = ?
    #             AND (
    #                 f1 IS NULL OR f1 = ''
    #                 OR f2 IS NULL OR f2 = ''
    #                 OR f3 IS NULL OR f3 = ''
    #             )
    #             """,
    #             (course,),
    #         ).fetchall()

    #     return [row[0] for row in cursor]

    # # returns list of valid ids
    # def valid_list(self, course: str) -> list[int]:
    #     with sqlite3.connect(self.database) as conn:
    #         cursor = conn.execute(
    #             """
    #             SELECT id 
    #             FROM questions
    #             WHERE course = ?
    #             AND f1 IS NOT NULL AND f1 <> ''
    #             AND f2 IS NOT NULL AND f2 <> ''
    #             AND f3 IS NOT NULL AND f3 <> ''
    #             """,
    #             (course,),
    #         ).fetchall()
    #     return [row[0] for row in cursor]
    

    # # Returns a bool depending on value in column
    # def check_col(self, row_id: int, column: str) -> bool:
    #     allowed = {"course", "question", "answer", "f1", "f2", "f3"}

    #     if column not in allowed:
    #         raise ValueError(f"Unknown column: {column}")

    #     with sqlite3.connect(self.database) as conn:
    #         row = conn.execute(
    #             f"""
    #             SELECT {column} IS NOT NULL AND {column} <> ''
    #             FROM questions
    #             WHERE id = ?
    #             """,
    #             (row_id,),
    #         ).fetchone()
    #     if row is None:
    #         return False
    #     return bool(row[0])

    # def get_question_answer(self, id: int) -> tuple[str,str] | None:
    #     with sqlite3.connect(self.database) as conn:
    #         row = conn.execute(
    #             """
    #             SELECT question, answer
    #             FROM questions
    #             WHERE id = ?
    #             """,
    #             (id,),
    #         ).fetchone()
    #     if row is None:
    #         return None
        
    #     return row[0], row[1]
    

    

