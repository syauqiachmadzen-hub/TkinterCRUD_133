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

        # Inisialisasi database
        init_db()

        # Frame Form Input
        form_frame = tk.LabelFrame(root, text=" Form Input Nilai Siswa ", padx=10, pady=10)
        form_frame.pack(fill="x", padx=15, pady=10)

        # Labels & Entries
        tk.Label(form_frame, text="Nama Siswa:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nama = tk.Entry(form_frame, width=30)
        self.entry_nama.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Nilai Biologi:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_biologi = tk.Entry(form_frame, width=30)
        self.entry_biologi.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Nilai Fisika:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_fisika = tk.Entry(form_frame, width=30)
        self.entry_fisika.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Nilai Inggris:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_inggris = tk.Entry(form_frame, width=30)
        self.entry_inggris.grid(row=3, column=1, pady=5)

        # Submit Button
        btn_submit = tk.Button(
            form_frame, 
            text="Submit Nilai", 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            command=self.on_submit
        )
        btn_submit.grid(row=4, column=0, columnspan=2, pady=10)

        # Frame Tabel Data (Treeview)
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")

        # Config Header Tabel
        self.tree.heading("id", text="ID")
        self.tree.heading("nama_siswa", text="Nama Siswa")
        self.tree.heading("biologi", text="Biologi")
        self.tree.heading("fisika", text="Fisika")
        self.tree.heading("inggris", text="Inggris")
        self.tree.heading("prediksi_fakultas", text="Prediksi Fakultas")

        # Config Lebar Kolom
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nama_siswa", width=140)
        self.tree.column("biologi", width=60, anchor="center")
        self.tree.column("fisika", width=60, anchor="center")
        self.tree.column("inggris", width=60, anchor="center")
        self.tree.column("prediksi_fakultas", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Refresh isi tabel saat pertama dijalankan
        self.refresh_table()

    def on_submit(self):
        """Handler saat tombol Submit Nilai diklik."""
        nama = self.entry_nama.get().strip()
        bio_str = self.entry_biologi.get().strip()
        fis_str = self.entry_fisika.get().strip()
        ing_str = self.entry_inggris.get().strip()

        # Validasi Input
        if not nama or not bio_str or not fis_str or not ing_str:
            messagebox.showwarning("Peringatan", "Semua kolom input wajib diisi!")
            return

        try:
            biologi = int(bio_str)
            fisika = int(fis_str)
            inggris = int(ing_str)
        except ValueError:
            messagebox.showerror("Error Validation", "Nilai Biologi, Fisika, dan Inggris harus berupa angka!")
            return

        # Hitung Hasil Prediksi
        prediksi = hitung_prediksi(biologi, fisika, inggris)

        # Simpan ke SQLite Database
        add_nilai(nama, biologi, fisika, inggris, prediksi)

        # Tampilkan Pesan Berhasil & Reset Input Form
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        self.clear_entries()
        self.refresh_table()

    def clear_entries(self):
        """Mereset isi kolom input entry."""
        self.entry_nama.delete(0, tk.END)
        self.entry_biologi.delete(0, tk.END)
        self.entry_fisika.delete(0, tk.END)
        self.entry_inggris.delete(0, tk.END)

    def refresh_table(self):
        """Menampilkan kembali baris data terbaru dari database ke tabel."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in get_all_nilai():
            self.tree.insert("", tk.END, values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppPrediksiFakultas(root)
    root.mainloop()