# ===================================================================
# TUDUH MENUDUH - Game Impostor Kata (Versi Python + Tampil window )
# cara jalan : python game_tuduh_menuduh.py
# ===================================================================

# #1 IMPORT Library
import tkinter as tk
from tkinter import ttk
import random

# #2 Warna & Tema
BG = "#0b0f19"          # latar window
CARD = "#151c2c"        # latar kartu / panel
INPUT_BG = "#1e293b"    # latar kolom input
ACCENT = "#6366f1"      # tombol utama
SECONDARY = "#4f46e5"   # tombol sekunder
DANGER = "#ff3366"      # merah (impostor / voting)
SUCCESS = "#00e676"     # hijau (warga menang)
INFO = "#3b82f6"        # biru muda (nama pemain)
TEXT = "#f8fafc"        
MUTED = "#f7fbff"

# tema warna kartu tiap pemain: (warna kartu, animal emoji)
CARD_THEMES = [
    ("#ff416c", "🕺"),
    ("#e94057", "💃"),
    ("#0083b0", "👨‍🚀"),
    ("#11998e", "🧘"),
    ("#fc4a1a", "🎸"),
    ("#8a2387", "🤹"),
]

# #3 BANK KATA (kategori -> pasangan kata yang mirip)
WORD_BANK = {
    "minuman": [
        {"civilian": "Kopi", "impostor": "Teh"},
        {"civilian": "Susu", "impostor": "Santan"},
        {"civilian": "Jus Jeruk", "impostor": "Lemonade"},
        {"civilian": "Boba", "impostor": "Cendol"},
        {"civilian": "Sirup", "impostor": "Madu"},
    ],
    "makanan": [
        {"civilian": "Nasi Goreng", "impostor": "Mie Goreng"},
        {"civilian": "Bakso", "impostor": "Siomay"},
        {"civilian": "Burger", "impostor": "Sandwich"},
        {"civilian": "Sate Ayam", "impostor": "Sate Kambing"},
        {"civilian": "Pizza", "impostor": "Martabak Telur"},
    ],
    "benda": [
        {"civilian": "Laptop", "impostor": "Komputer"},
        {"civilian": "Pensil", "impostor": "Pulpen"},
        {"civilian": "Sepatu", "impostor": "Sandal"},
        {"civilian": "Sendok", "impostor": "Garpu"},
        {"civilian": "Kasur", "impostor": "Sofa"},
    ],
    "profesi": [
        {"civilian": "Dokter", "impostor": "Perawat"},
        {"civilian": "Polisi", "impostor": "Tentara"},
        {"civilian": "Guru","impostor": "Dosen"},
        {"civilian": "Pilot", "impostor": "Masinis"},
        {"civilian": "Koki", "impostor": "Pelayan"},
    ],
}

KATEGORI_PILIHAN = ["🎲 Acak Semua Kategori", "☕ Minuman", "🍕 Makanan",
                    "📦 Benda", "👨‍🍳 Profesi"]
KATEGORI_KEY = [None, "minuman", "makanan", "benda", "profesi"]


# #4 KELAS UTAMA APLIKASI
class TuduhMenuduhApp:
    
    # #4a KONSTRUKTOR: membuat window dan state game 
    def __init__(self, root):
        self.root = root 
        root.title("Tuduh Menuduh - Game Impostor Kata")
        root.geometry("460x720")
        root.minsize(420, 680)
        root.configure(bg=BG)

        # state game 
        self.players = []
        self.current = 0
        self.pair = {}
        self.category_name = ""
        self.timer_left = 120
        self.timer_running = False
        self.timer_job = None
        self.card_open = False
        self.vote_var = tk.IntVar(value=-1)
        self.name_entries = []
        
        # Container utama (semua layar ditaruh di sini)
        self.container = tk.Frame(root, bg=CARD, padx=24, pady=20)
        self.container.pack(fill="both", expand=True, padx=12, pady=12)
        
        self.screen = None
        self.build_setup()
        self.show(self.f_setup)
        
    # #4b FUNGSI BANTUAN: tombol, label, ganti layar
    def button(self, parent, text, command, color=ACCENT):
        return tk.Button(parent, text=text, command=command, bg=color, fg="white",
                         activebackground=color, activeforeground="white",
                         font=("Segoe UI", 12, "bold"), relief="flat", bd=0,
                         cursor="hand2", pady=12)

    def label(self, parent, text, size=11, bold=False, color=TEXT, **kw):
        return tk.Label(parent, text=text, bg=kw.pop("bg", CARD), fg=color,
                        font=("Segoe UI", size, "bold" if bold else "normal"), **kw)

    def show(self, frame):
        """Sembunyikan layar lama, tampilkan layar baru."""
        if self.screen is not None:
            self.screen.pack_forget()
        self.screen = frame
        frame.pack(fill="both", expand=True)

    def popup(self, title, msg):
        """Jendela pemberitahuan kecil."""
        win = tk.Toplevel(self.root, bg=CARD, padx=24, pady=20)
        win.title(title)
        win.transient(self.root)
        win.grab_set()
        self.label(win, title, 14, True, INFO).pack(pady=(0, 8))
        self.label(win, msg, 10, color=MUTED, wraplength=280).pack(pady=(0, 14))
        self.button(win, "Selesai", win.destroy).pack(fill="x")


    # =====================================================================
    # #5 LAYAR 1: SETUP
    # =====================================================================
    def build_setup(self):
        f = tk.Frame(self.container, bg=CARD)
        self.f_setup = f

        self.label(f, "TUDUH MENUDUH", 24, True, "#a5b4fc").pack()
        self.label(f, "Satu laptop, semua ikut main!", 10, color=MUTED).pack(pady=(0, 14))

        # #5a Jumlah pemain (3 - 10)
        self.label(f, "Jumlah Pemain (3-10):", 10, True, MUTED).pack(anchor="w")
        self.count_var = tk.StringVar(value="4")
        spin = tk.Spinbox(f, from_=3, to=10, textvariable=self.count_var,
                          command=self.update_player_inputs, font=("Segoe UI", 12),
                          bg=INPUT_BG, fg=TEXT, buttonbackground=SECONDARY,
                          insertbackground=TEXT, relief="flat")
        spin.pack(fill="x", pady=(2, 10), ipady=6)
        spin.bind("<KeyRelease>", lambda e: self.update_player_inputs())

        # #5b Jumlah impostor
        self.label(f, "Jumlah Impostor:", 10, True, MUTED).pack(anchor="w")
        self.imp_var = tk.StringVar(value="1 Impostor")
        self.imp_combo = ttk.Combobox(f, textvariable=self.imp_var, state="readonly",
                                      values=["1 Impostor"], font=("Segoe UI", 11))
        self.imp_combo.pack(fill="x", pady=(2, 10), ipady=4)

        # #5c Kategori kata
        self.label(f, "Kategori Kata:", 10, True, MUTED).pack(anchor="w")
        self.cat_var = tk.StringVar(value=KATEGORI_PILIHAN[0])
        ttk.Combobox(f, textvariable=self.cat_var, state="readonly",
                     values=KATEGORI_PILIHAN, font=("Segoe UI", 11)
                     ).pack(fill="x", pady=(2, 10), ipady=4)

        # #5d Nama-nama pemain (dibuat dinamis sesuai jumlah pemain)
        self.label(f, "Nama-nama Pemain:", 10, True, MUTED).pack(anchor="w")
        self.names_frame = tk.Frame(f, bg=CARD)
        self.names_frame.pack(fill="both", expand=True, pady=(2, 6))
        self.update_player_inputs()

        # #5e Tombol mulai
        self.button(f, "Mulai Game", self.start_game).pack(fill="x", side="bottom")

    def update_player_inputs(self):
        """Buat ulang kolom nama sesuai jumlah pemain (nilai lama dipertahankan)."""
        try:
            count = int(self.count_var.get())
        except ValueError:
            count = 3
        count = max(3, min(10, count))

        # simpan nama yang sudah diketik
        lama = [e.get() for e in self.name_entries]
        for w in self.names_frame.winfo_children():
            w.destroy()
        self.name_entries = []

        # grid 2 kolom supaya muat di window
        for i in range(count):
            e = tk.Entry(self.names_frame, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Segoe UI", 10))
            e.insert(0, lama[i] if i < len(lama) else f"Pemain {i + 1}")
            e.grid(row=i // 2, column=i % 2, padx=3, pady=3, sticky="ew", ipady=5)
            self.name_entries.append(e)
            self.names_frame.columnconfigure((0, 1), weight=1)

        # Impostor maksimal 2 (hanya jika pemain >= 4)
        opsi = ["1 Impostor"] + (["2 Impostor"] if count >= 4 else [])
        self.imp_combo["values"] = opsi
        if self.imp_var.get() not in opsi:
            self.imp_var.set(opsi[0])


    # =====================================================================
    # #6 MEMBAGI PERAN & KATA
    # =====================================================================
    def start_game(self):
        # #6a Ambil nama pemain (kosong -> "Pemain N")
        names = [e.get().strip() or f"Pemain {i + 1}"
                 for i, e in enumerate(self.name_entries)]
        jumlah_imp = int(self.imp_var.get().split()[0])

        # #6b Pilih kategori & pasang kata secara acak
        idx = KATEGORI_PILIHAN.index(self.cat_var.get())
        kategori = KATEGORI_KEY[idx] or random.choice(list(WORD_BANK))
        self.category_name = kategori.upper()
        self.pair = random.choice(WORD_BANK[kategori])

        # #6c Pilih impostor (tanpa duplikat)
        idx_imp = random.sample(range(len(names)), jumlah_imp)

        # #6d Susun data pemain
        self.players = []
        for i, nama in enumerate(names):
            is_imp = i in idx_imp
            self.players.append({
                "nama": nama,
                "is_impostor": is_imp,
                "kata": self.pair["impostor"] if is_imp else self.pair["civilian"],
                "tema": CARD_THEMES[i % len(CARD_THEMES)],
            })

        self.current = 0
        self.build_pass()
        self.show(self.f_pass)
        
    # =======================================================
    # #7 LAYAR 2: OPER LAPTOP (PASS DEVICE)
    # =======================================================
    def build_pass(self):
        nama = self.players[self.current]["nama"]
        f = tk.Frame(self.container, bg=CARD)
        self.f_pass = f
     
        mid = tk.Frame(f, bg=CARD)
        mid.pack(expand=True)
        self.label(mid, "Giliran Pemain", 11, color=MUTED).pack()
        self.label(mid, nama, 30, True, INFO).pack(pady=14)
        self.label(mid, f"Berikan laptop ini ke {nama}.", 11).pack()
        self.label(mid, "Pastikan pemain lain tidak mengintip layar!", 9,
                   color=MUTED).pack(pady=10)
     
        self.button(f, f"Saya Adalah {nama}", self.show_card).pack(fill="x", side="bottom")
        
    # ===========================================================
    # #8 LAYAR 3: KARTU RAHASIA (klik untuk intip / tutup)
    # ===========================================================
    def show_card(self):
        p = self.players[self.current]
        warna, avatar = p["tema"]
        self.card_open = False
 
        f = tk.Frame(self.container, bg=CARD)
        self.f_card = f
 
        self.label(f, "Klik kartu untuk mengintip!", 10, color=MUTED).pack(pady=(0, 8))
 
        # #8a Bagian kartu berwarna + avatar
        kartu = tk.Frame(f, bg=warna, cursor="hand2")
        kartu.pack(fill="both", expand=True)
        self.label(kartu, p["nama"], 22, True, "white", bg=warna).pack(pady=(24, 4))
        self.label(kartu, avatar, 60, bg=warna).pack(pady=6)
 
        # #8b Panel penutup: awalnya tertutup, klik untuk membuka
        self.cover = tk.Frame(kartu, bg="#1a1030", cursor="hand2")
        self.cover.pack(fill="both", expand=True, padx=14, pady=(10, 14))
        self.cover_icon = self.label(self.cover, "🔒", 34, bg="#1a1030")
        self.cover_icon.pack(pady=(18, 2))
        self.cover_cat = self.label(self.cover, "▲ KETUK UNTUK MENGINTIP", 10, True,
                                    "white", bg="#1a1030")
        self.cover_cat.pack()
        self.cover_word = self.label(self.cover, "", 24, True, "white", bg="#1a1030")
        self.cover_word.pack(pady=6)
        
        # Semua bagian panel bisa diklik
        for w in (self.cover, self.cover_icon, self.cover_cat, self.cover_word):
            w.bind("<Button-1>", lambda e: self.toggle_card())
 
        self.button(f, "Selesai & Lanjut", self.next_player, SECONDARY
                    ).pack(fill="x", side="bottom", pady=(10, 0))
        self.show(f)
 
    def toggle_card(self):
        """Buka / tutup kartu."""
        p = self.players[self.current]
        self.card_open = not self.card_open
        if self.card_open:
            self.cover_icon.config(text="🕵️" if p["is_impostor"] else "👥")
            self.cover_cat.config(text=f"KATEGORI: {self.category_name}")
            self.cover_word.config(text=p["kata"].upper(),
                                   fg=DANGER if p["is_impostor"] else "white")
        else:
            self.cover_icon.config(text="🔒")
            self.cover_cat.config(text="▲ KETUK UNTUK MENGINTIP")
            self.cover_word.config(text="")
 
    def next_player(self):
        """Lanjut ke pemain berikutnya, atau mulai diskusi jika semua sudah."""
        self.current += 1
        if self.current < len(self.players):
            self.build_pass()
            self.show(self.f_pass)
        else:
            self.build_discussion()
            self.show(self.f_disc)
            
    # ==================================================================
    # #9 LAYAR 4: DISKUSI (urutan bicara + timer)
    # ==================================================================
    def build_discussion(self):
        f = tk.Frame(self.container, bg=CARD)
        self.f_disc = f
 
        self.label(f, "Babak Diskusi", 20, True).pack()
        self.label(f, "Berikan 1 kata petunjuk secara bergantian!", 10,
                   color=MUTED).pack(pady=(0, 14))
 
        # #9a Urutan bicara diacak
        urutan = [p["nama"] for p in self.players]
        random.shuffle(urutan)
        box = tk.Frame(f, bg=BG, padx=12, pady=12)
        box.pack(fill="x")
        self.label(box, "Urutan Bicara:", 9, True, MUTED, bg=BG).pack()
        self.label(box, "  ➔  ".join(urutan), 11, True, INFO, bg=BG,
                   wraplength=360).pack(pady=4)
 
        # #9b Tampilan timer
        self.timer_left = 120
        self.timer_running = False
        self.timer_label = self.label(f, "02:00", 46, True, DANGER)
        self.timer_label.pack(pady=26)
 
        # #9c Tombol timer & voting
        self.timer_btn = self.button(f, "Mulai Timer", self.toggle_timer, SECONDARY)
        self.timer_btn.pack(fill="x", side="bottom")
        self.button(f, "Mulai Voting", self.start_voting, DANGER
                    ).pack(fill="x", side="bottom", pady=(0, 10))
 
    def update_timer_label(self):
        m, s = divmod(self.timer_left, 60)
        self.timer_label.config(text=f"{m:02d}:{s:02d}")
 
    def toggle_timer(self):
        if self.timer_running:
            # Pause
            self.timer_running = False
            self.root.after_cancel(self.timer_job)
            self.timer_btn.config(text="Lanjutkan Timer")
        else:
            # Mulai / lanjut
            self.timer_running = True
            self.timer_btn.config(text="Pause Timer")
            self.tick()
 
    def tick(self):
        """Dipanggil tiap 1 detik oleh root.after()."""
        if self.timer_left > 0:
            self.timer_left -= 1
            self.update_timer_label()
            self.timer_job = self.root.after(1000, self.tick)
        else:
            self.timer_running = False
            self.root.bell()
            self.start_voting()
            self.popup("⏰ Waktu Diskusi Habis!", "Saatnya menuduh siapa Impostor-nya!")            
            
    # ==================================================================
    # #10 LAYAR 5: VOTING
    # ==================================================================
    def start_voting(self):
        # Hentikan timer kalau masih jalan
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False
 
        f = tk.Frame(self.container, bg=CARD)
        self.f_vote = f
        self.vote_var.set(-1)
 
        self.label(f, "Tuduh Impostor!", 20, True).pack()
        self.label(f, "Siapa yang dicurigai sebagai Impostor?", 10,
                   color=MUTED).pack(pady=(0, 12))
 
        # #10a Daftar pemain berbentuk tombol pilihan
        for i, p in enumerate(self.players):
            tk.Radiobutton(f, text=p["nama"], variable=self.vote_var, value=i,
                           indicatoron=False, bg=INPUT_BG, fg=TEXT,
                           selectcolor=ACCENT, activebackground=ACCENT,
                           activeforeground="white", font=("Segoe UI", 11, "bold"),
                           relief="flat", bd=0, pady=9, cursor="hand2"
                           ).pack(fill="x", pady=3)
 
        self.button(f, "Tentukan Hasil", self.process_vote, DANGER
                    ).pack(fill="x", side="bottom")
        self.show(f)
 
    # ==================================================================
    # #11 LAYAR 6: HASIL AKHIR
    # ==================================================================
    def process_vote(self):
        idx = self.vote_var.get()
        if idx < 0:
            self.popup("Peringatan", "Pilih salah satu pemain yang dicurigai terlebih dahulu!")
            return
        dituduh = self.players[idx]
 
        f = tk.Frame(self.container, bg=CARD)
        self.f_result = f
 
        # #11a Tentukan pemenang
        if dituduh["is_impostor"]:
            judul, warna = "WARGA MENANG! 🎉", SUCCESS
            sub = f"{dituduh['nama']} adalah Impostor dan berhasil tertangkap!"
        else:
            judul, warna = "IMPOSTOR MENANG! 😈", DANGER
            sub = f"{dituduh['nama']} adalah Warga! Impostor berhasil mengelabui kalian."
            self.root.bell()
 
        self.label(f, judul, 20, True, warna).pack()
        self.label(f, sub, 10, color=MUTED, wraplength=360).pack(pady=(2, 12))
 
        # #11b Kotak kata & peran semua pemain
        box = tk.Frame(f, bg=BG, padx=14, pady=12)
        box.pack(fill="x")
        self.label(box, f"Kata Warga: {self.pair['civilian']}", 11, True, INFO,
                   bg=BG).pack(anchor="w")
        self.label(box, f"Kata Impostor: {self.pair['impostor']}", 11, True, DANGER,
                   bg=BG).pack(anchor="w", pady=(2, 8))
        self.label(box, "Peran Pemain:", 10, True, MUTED, bg=BG).pack(anchor="w")
 
        for p in self.players:
            row = tk.Frame(box, bg=BG)
            row.pack(fill="x", pady=2)
            self.label(row, p["nama"], 10, bg=BG).pack(side="left")
            peran = "IMPOSTOR" if p["is_impostor"] else "WARGA"
            self.label(row, f"{peran} ({p['kata']})", 10, True,
                       DANGER if p["is_impostor"] else SUCCESS, bg=BG).pack(side="right")
 
        # #11c Main lagi -> kembali ke layar setup
        self.button(f, "Main Lagi", self.reset_game).pack(fill="x", side="bottom")
        self.show(f)
 
    def reset_game(self):
        self.show(self.f_setup)


# #12 TITIK MASUK PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    TuduhMenuduhApp(root)
    root.mainloop()