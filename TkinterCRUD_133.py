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

def add_nilai(nama, biologi, fisika, inggris, prediksi):
    """Menyimpan data nilai siswa baru ke SQLite."""
    run_query("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))

def get_all_nilai():
    """Mengambil seluruh data nilai dari SQLite."""
    return run_query("""
        SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas 
        FROM nilai_siswa ORDER BY id DESC
    """)    

# --- LOGIC LAYER ---
def hitung_prediksi(biologi, fisika, inggris):
    """
    Logika penentuan prediksi fakultas:
    - Biologi paling tinggi -> Kedokteran
    - Fisika paling tinggi   -> Teknik
    - Inggris paling tinggi  -> Bahasa
    """
    if biologi >= fisika and biologi >= inggris:
        return "Kedokteran"
    elif fisika >= biologi and fisika >= inggris:
        return "Teknik"
    else:
        return "Bahasa"

# --- GUI LAYER (Tkinter Application) ---
class AppPrediksiFakultas:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Prediksi Fakultas - Tkinter & SQLite")
        self.root.geometry("650x500")
    

