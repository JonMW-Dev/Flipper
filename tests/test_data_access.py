# tests the Data Access Layer
from pathlib import Path
from flipper.data_access.data_access import DataAccessService

def test_data_insert_get_insertCell():
    print("Running test_data_insert_get_insertCell")
    # Create the test database in the project's data directory.
    test_db_path = Path(__file__).resolve().parent.parent / "data" / "test_db.db"

    das = DataAccessService(test_db_path)

    # insert a new row
    row_id = das.insert(
        course="Test Course",
        question="What is the capital of France?",
        answer="Paris",
        f1="London",
        f2="Berlin",
        f3="Madrid",
    )

    # retrieve the row and check its contents
    row = das.get(row_id)
    assert row is not None
    assert row[1] == "Test Course"
    assert row[2] == "What is the capital of France?"
    assert row[3] == "Paris"
    assert row[4] == "London"
    assert row[5] == "Berlin"
    assert row[6] == "Madrid"
    assert row[7] == 0  # correct
    assert row[8] == 0  # attempts

    # update a cell and check its contents
    das.insert_cell(row_id, "correct", 1)
    updated_row = das.get(row_id)
    assert updated_row is not None
    assert updated_row[7] == 1  # correct