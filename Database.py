import sqlite3

DB_NAME = "database_siswa.db"

def run_query(sql, params=()):
    """Fungsi helper untuk menjalankan query SQL secara aman."""
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            return conn.execute(sql, params).fetchall()
    finally:
        conn.close()