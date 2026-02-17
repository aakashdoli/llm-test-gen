import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Path Setup
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chat_with_sql_main"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from app2 import get_gemini_response, read_sql_query

# --- TEST 1: get_gemini_response ---
@patch("app2.genai.GenerativeModel") 
def test_get_gemini_response_basic(mock_model_class):
    # Mock Google API
    mock_instance = mock_model_class.return_value
    mock_instance.generate_content.return_value.text = "SELECT * FROM STUDENTS"
    
    # REAL INPUTS (Strings/Lists, NOT Zeros)
    question = "How many students are there?"
    prompt = ["You are an SQL expert..."]
    
    result = get_gemini_response(question, prompt)
    assert result == "SELECT * FROM STUDENTS"

# --- TEST 2: read_sql_query ---
@patch("app2.sqlite3")
def test_read_sql_query_basic(mock_sqlite):
    # Mock Database
    mock_conn = mock_sqlite.connect.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = [("Student A",), ("Student B",)]
    
    # REAL INPUTS
    sql_query = "SELECT * FROM STUDENT"
    db_name = "student.db"
    
    result = read_sql_query(sql_query, db_name)
    assert len(result) == 2