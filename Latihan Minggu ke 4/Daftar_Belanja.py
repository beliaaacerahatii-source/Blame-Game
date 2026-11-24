Sabun_mandi = 2500
Sosis = 8000
Kopi = 7000
print("Hitung Belanja")
jumlah_sabun = int(input("Masukkan jumlah beli sabun: "))
jumlah_sosis = int(input("Masukkan jumlah beli sosis: "))
jumlah_kopi = int(input("Masukkan jumlah beli kopi: "))
total_sabun = jumlah_sabun * Sabun_mandi
total_sosis = jumlah_sosis * Sosis
total_kopi = jumlah_kopi * Kopi
if jumlah_sabun >= 4: total_sabun *= 0.75
if jumlah_sosis >= 2: total_sosis *= 0.90
if jumlah_kopi >= 10: total_kopi *= 0.85
total = total_sabun + total_sosis + total_kopi
print("Total belanja: Rp", total)