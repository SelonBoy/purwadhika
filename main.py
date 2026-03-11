# library bawaan yang kita butuhkan
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime

# menghubungkan python dengan server mysql
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Shadowrx79@",
    database = "finance_tracker",
)

# function global
current_user = " "
current_user_id = None
current_user_nama = None

def input_tanggal():
    while True:
        tanggal = input("Tanggal (YYYY-MM-DD): ")
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            return tanggal
        except:
            print("❌ Format salah! Contoh: 2026-02-26\n")

def kategori_pengeluaran():
    while True:
        print("\n=== Pilih Kategori Pengeluaran ===")
        print("1. Makanan")
        print("2. Transportasi")
        print("3. Belanja/Hiburan")
        print("4. Tagihan/Cicilan")
        print("5. Tabungan/investasi")
        print("6. By. Lain-lain")

        pilih = input("Pilih: ")

        if pilih == "1":
            return "Makanan"
        elif pilih == "2":
            return "Transportasi"
        elif pilih == "3":
            return "Belanja/Hiburan"
        elif pilih == "4":
            return "Tagihan/Cicilan"
        elif pilih == "5":
            return "Tabungan/Investasi"
        elif pilih == "6":
            return "Lain-lain"
        else:
            print("Pilihan salah, coba lagi.")

# membuat worker ke database mydb
cursor = mydb.cursor()

# tambah user
def tambah_user():
    global current_user
    nama = input("Masukkan nama user: ")

    sql = "INSERT INTO users (nama) VALUES (%s)"
    val = (nama,)

    cursor.execute(sql, val)
    mydb.commit()

    print("User berhasil ditambah!\n")

# Membaca table expenses
def read_expenses():
    cursor.execute("SELECT tanggal, kategori, jumlah, catatan FROM expenses WHERE user_id=%s ORDER BY tanggal DESC", (current_user_id,))
    data = cursor.fetchall()

    if not data:
        print("Belum ada data\n")
        return

    df = pd.DataFrame(data, columns=cursor.column_names)
    print(df, "\n")

# Menambah data

def tambah_pemasukan():
    tanggal = input_tanggal()
    sumber = input("Sumber: ")
    
    while True:
        try:
            jumlah = int(input("Jumlah: "))
            break
        except:
            print("Masukkan angka!")

    sql = "INSERT INTO income (user_id, tanggal, sumber, jumlah) VALUES (%s,%s,%s,%s)"
    val = (current_user_id, tanggal, sumber, jumlah)

    cursor.execute(sql, val)
    mydb.commit()

    print("Pemasukan ditambah!\n")

    sql = "INSERT INTO income (user_id, tanggal, sumber, jumlah) VALUES (%s,%s,%s,%s)"
    val = (current_user_id, tanggal, sumber, jumlah)

    cursor.execute(sql, val)
    mydb.commit()
    print("Pemasukan ditambah!\n")


def tambah_pengeluaran():
    tanggal = input_tanggal()
    kategori = kategori_pengeluaran()
    while True:
        try:
            jumlah = int(input("Jumlah: "))
            break
        except:
            print("Masukkan angka!")
    catatan = input("Catatan (opsional): ")

    sql = """INSERT INTO expenses 
             (user_id, tanggal, kategori, jumlah, catatan)
             VALUES (%s,%s,%s,%s,%s)"""
    val = (current_user_id, tanggal, kategori, jumlah, catatan)

    cursor.execute(sql, val)
    mydb.commit()
    print("Pengeluaran ditambah!\n")

# Sub menu
def statistik_menu():
    while True:
        print("\n=== HITUNG RATA RATA ===")
        print("1. Mingguan")
        print("2. Bulanan")
        print("3. Tahunan")
        print("4. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            cursor.execute("""
            SELECT AVG(total_mingguan)
            FROM (
                SELECT SUM(jumlah) as total_mingguan
                FROM expenses
                WHERE user_id=%s
                GROUP BY YEARWEEK(tanggal)
            ) as data
            """, (current_user_id,))

            avg = cursor.fetchone()[0] or 0
            print(f"Rata-rata pengeluaran mingguan: Rp {avg:,.0f}")

        elif pilih == "2":
            cursor.execute("""
            SELECT AVG(total_bulanan)
            FROM (
                SELECT SUM(jumlah) as total_bulanan
                FROM expenses
                WHERE user_id=%s
                GROUP BY YEAR(tanggal), MONTH(tanggal)
            ) as data
            """,(current_user_id,))

            avg = cursor.fetchone()[0] or 0
            print(f"Rata-rata pengeluaran 30 hari terakhir: Rp {avg:,.0f}")

        elif pilih == "3":
            cursor.execute("""
            SELECT AVG(total_tahunan)
            FROM (
                SELECT SUM(jumlah) as total_tahunan
                FROM expenses
                WHERE user_id=%s
                GROUP BY YEAR(tanggal)
            ) as data
            """,(current_user_id,))

            avg = cursor.fetchone()[0] or 0
            print(f"Rata-rata pengeluaran 1 tahun terakhir: Rp {avg:,.0f}")

        elif pilih == "4":
            break

# visualisasi
def visualisasi_menu():
    while True:
        print("\n=== VISUALISASI ===")
        print("1. Pengeluaran per Kategori")
        print("2. Income vs Expense")
        print("3. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            cursor.execute("""
                SELECT kategori, SUM(jumlah)
                FROM expenses
                WHERE user_id=%s
                GROUP BY kategori
                ORDER BY SUM(jumlah) DESC
            """, (current_user_id,))
            data = cursor.fetchall()

            if not data:
                print("Belum ada data.\n")
                continue

            kategori = [x[0] for x in data]
            jumlah = [x[1] for x in data]

            plt.figure()
            bars = plt.bar(kategori, jumlah)

            plt.title("Total Pengeluaran per Kategori")
            plt.ylabel("Jumlah (Rp)")
            plt.xticks(rotation=30)

            # format rupiah
            ax = plt.gca()
            ax.yaxis.set_major_formatter(
                mticker.FuncFormatter(lambda x, _: f'Rp {x:,.0f}')
            )

            # angka di atas bar
            for bar in bars:
                y = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, y,
                         f"Rp {y:,.0f}", ha='center', va='bottom')

            plt.show()

        elif pilih == "2":
            cursor.execute("SELECT SUM(jumlah) FROM income WHERE user_id=%s", (current_user_id,))
            inc = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(jumlah) FROM expenses WHERE user_id=%s", (current_user_id,))
            exp = cursor.fetchone()[0] or 0

            plt.figure()
            bars = plt.bar(["Income", "Expense"], [inc, exp])

            plt.title("Income vs Expense")
            plt.ylabel("Jumlah (Rp)")

            ax = plt.gca()
            ax.yaxis.set_major_formatter(
                mticker.FuncFormatter(lambda x, _: f'Rp {x:,.0f}')
            )

            for bar in bars:
                y = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, y,
                         f"Rp {y:,.0f}", ha='center', va='bottom')

            plt.show()

        elif pilih == "3":
            break
# lihat user
def lihat_users():
    while True:
        print("\n=== TABLE USER ===")
        print("1. Lihat User")
        print("2. Tambah User")
        print("3. Hapus User")
        print("4. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            cursor.execute("SELECT id, nama FROM users")
            users = cursor.fetchall()

            if not users:
                print("Belum ada user.\n")
                continue

            for u in users:
                print(f"ID: {u[0]} | Nama: {u[1]}")

        elif pilih == "2":
            tambah_user()

        elif pilih == "3":
            user_id = input("Masukkan ID user yang mau dihapus: ")

            cursor.execute("DELETE FROM income WHERE user_id=%s",(user_id,))
            cursor.execute("DELETE FROM expenses WHERE user_id=%s",(user_id,))
            cursor.execute("DELETE FROM users WHERE id=%s",(user_id,))
            mydb.commit()

            print("User berhasil dihapus\n")

        elif pilih == "4":
            break
# VISUALISASI AWAL
def next_menu():
    while True:
        print(f"\n=== HAI {current_user_nama} PERSONAL FINANCE TRACKER ===")
        print("1. Tambah Pemasukan")
        print("2. Tambah Pengeluaran")
        print("3. Hitung Rata-rata")
        print("4. Visualisasi")
        print("5. Lihat Expense")
        print("0. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_pemasukan()
        elif pilih == "2":
            tambah_pengeluaran()
        elif pilih == "3":
            statistik_menu()
        elif pilih == "4":
            visualisasi_menu()
        elif pilih == "5":
            read_expenses()
        elif pilih == "0":
            if current_user:
                print(f"Bye {current_user_nama}")
            else:
                print("Bye")
            break
        else:
            print("Pilihan salah!")

def pilih_users():
    global current_user_id, current_user_nama

    cursor.execute("SELECT id, nama FROM users")
    users = cursor.fetchall()

    if not users:
        print("Belum ada user. Tambah user dulu.\n")
        return

    print("\n=== LIST USER ===")
    for u in users:
        print(f"ID: {u[0]} | Nama: {u[1]}")

    try:
        user_id = int(input("Pilih ID user: "))
    except:
        print("ID tidak valid\n")
        return

    cursor.execute("SELECT id, nama FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if user:
        current_user_id = user[0]
        current_user_nama = user[1]
        print(f"Login sebagai {current_user_nama}\n")
    else:
        print("User tidak ditemukan\n")

def main_menu():
    while True:
        print("\n=== WELCOME TO PERSONAL FINANCE TRACKER ===")
        print("0. Lihat User")
        print("1. Pilih User")

        pilih = input("Pilih menu: ")

        if pilih == "0":
            lihat_users()
        elif pilih == "1":
            pilih_users()
            if current_user_id is not None:
                next_menu()
        else:
            print("Pilihan salah!")
            continue

#run program
main_menu()