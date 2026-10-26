import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- DATA LAYER (SQLite Database Operations) ---
DB_NAME = "nilai_siswa.db"

def run_query(sql, params=()):
    """Helper function untuk menjalankan query SQL secara aman."""
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:  # Otomatis melakukan commit atau rollback jika ada error
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()

def init_db():
    """Membuat tabel nilai_siswa jika belum ada."""
    run_query("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)