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

def init_db():
    """Membuat tabel nilai_siswa dengan atribut yang diminta."""
    run_query("""CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
    )""")
