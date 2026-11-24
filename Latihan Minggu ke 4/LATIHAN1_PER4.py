print(" Daftar Belanja ")
print("**********************")

harga_sabun = 2500
harga_sosis = 8000
harga_kopi  = 7000

jumlah_sabun = int(input("Masukan Jumlah Sabun Mandi : "))
jumlah_sosis = int(input("Masukan Jumlah Sosis       : "))
jumlah_kopi  = int(input("Masukan Jumlah Kopi        : "))

jumlah_sabun = harga_sabun * jumlah_sabun
jumlah_sosis = harga_sosis * jumlah_sosis
jumlah_kopi = harga_kopi * jumlah_kopi

#Ketentuan Diskon
if jumlah_sabun > 4:
    total_sabun = 0.75

if jumlah_sosis > 2:
    total_sosis = 0.90

if jumlah_kopi > 10:
    total_kopi = 0.85

total_harga = total_sabun + total_sosis + total_kopi

print("=" * 30)

print("Sabun Mandi : Rp", int(total_sabun))
print("Sosis       : Rp", int(total_sosis))
print("Kopi        : Rp", int(total_kopi))
print("--------------------------------------------------")
print("Total Harga : Rp", int(total_harga))