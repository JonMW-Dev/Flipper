import sqlite3

from flipper.data_access import data_access
from flipper.data_access.data_access import DataAccessService
from flipper.modules.edu.testbank_service import TestBankService as BankService


def test_check_col_reports_whether_column_is_populated(tmp_path, monkeypatch):
    monkeypatch.setattr(data_access, "DATA_DIR", tmp_path)
    database_path = tmp_path / "education.db"
    with sqlite3.connect(database_path) as conn:
        conn.execute(
            """
            CREATE TABLE testbank (
                id INTEGER PRIMARY KEY,
                f1 TEXT
            )
            """
        )
        conn.executemany(
            "INSERT INTO testbank (id, f1) VALUES (?, ?)",
            [(1, None), (2, ""), (3, "answer")],
        )

    service = BankService.__new__(BankService)
    service.data_service = DataAccessService("education.db", "testbank")

    assert service.check_col(1, "f1") is False
    assert service.check_col(2, "f1") is False
    assert service.check_col(3, "f1") is True
    assert service.check_col(4, "f1") is False
