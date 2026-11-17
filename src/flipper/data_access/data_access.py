import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parents[3] / "data" / "testbank.db"


class DataAccessService:
    """Reads and writes rows in the questions table."""

    def __init__(self, database: Path = DATABASE):
        self.database = database

    def insert(
        self,
        course: str,
        question: str,
        answer: str,
        f1: str | None = None,
        f2: str | None = None,
        f3: str | None = None,
    ) -> int:
        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute(
                """
                INSERT INTO questions (
                    course, question, answer, f1, f2, f3, correct, attempts
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (course, question, answer, f1, f2, f3, 0, 0),
            )
            row_id = cursor.lastrowid
        if row_id is None:
            raise RuntimeError("Insert did not return an id.")
        return row_id
    
    def insert_cell(self, id: int, col: str, value: str | int):
        allowlist = ['f1', 'f2', 'f3', 'correct', 'attempt']
        if col not in allowlist:
            raise ValueError(f"DAS: provided column value, {col}, is not valid")

        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute(
                f"""
                UPDATE questions
                SET {col} = ?
                WHERE id = ?
                """,
                (value, id),
            )

    def get(self, row_id: int) -> tuple | None:
        with sqlite3.connect(self.database) as conn:
            return conn.execute(
                """
                SELECT id, course, question, answer, f1, f2, f3, correct, attempts
                FROM questions
                WHERE id = ?
                """,
                (row_id,),
            ).fetchone()

    def invalid_count(self, course) -> int:
        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute(
                """
                SELECT COUNT(*)
                FROM questions
                WHERE course = ?
                AND (
                    f1 IS NULL OR f1 = ''
                    OR f2 IS NULL OR f2 = ''
                    OR f3 IS NULL OR f3 = ''
                )
                """,
                (course,),
            ).fetchone()
        return cursor[0]

    def total_count(self, course) -> int:
        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute(
                """
                SELECT COUNT(*)
                FROM questions
                WHERE course = ?
                """,
                (course,),
            ).fetchone()
        return cursor[0]

    # returns list of ids belonging to invalid entries and COURSE
    def invalid_list(self, course) -> list[int]:
        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute(
                """
                SELECT id
                FROM questions
                WHERE course = ?
                AND (
                    f1 IS NULL OR f1 = ''
                    OR f2 IS NULL OR f2 = ''
                    OR f3 IS NULL OR f3 = ''
                )
                """,
                (course,),
            ).fetchall()

        return [row[0] for row in cursor]

    # returns list of valid ids
    def valid_list(self, course: str) -> list[int]:
        with sqlite3.connect(self.database) as conn:
            cursor = conn.execute(
                """
                SELECT id 
                FROM questions
                WHERE course = ?
                AND f1 IS NOT NULL AND f1 <> ''
                AND f2 IS NOT NULL AND f2 <> ''
                AND f3 IS NOT NULL AND f3 <> ''
                """,
                (course,),
            ).fetchall()
        return [row[0] for row in cursor]
    

    # Returns a bool depending on value in column
    def check_col(self, row_id: int, column: str) -> bool:
        allowed = {"course", "question", "answer", "f1", "f2", "f3"}

        if column not in allowed:
            raise ValueError(f"Unknown column: {column}")

        with sqlite3.connect(self.database) as conn:
            row = conn.execute(
                f"""
                SELECT {column} IS NOT NULL AND {column} <> ''
                FROM questions
                WHERE id = ?
                """,
                (row_id,),
            ).fetchone()
        if row is None:
            return False
        return bool(row[0])

    def get_question_answer(self, id: int) -> tuple[str,str] | None:
        with sqlite3.connect(self.database) as conn:
            row = conn.execute(
                """
                SELECT question, answer
                FROM questions
                WHERE id = ?
                """,
                (id,),
            ).fetchone()
        if row is None:
            return None
        
        return row[0], row[1]
    

    

