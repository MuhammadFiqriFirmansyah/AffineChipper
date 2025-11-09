#!/usr/bin/env python3
"""
Affine Cipher GUI
Author: [Muhammad Fiqri Firmansyah]
For: UTS Kriptografi - Universitas Pelita Bangsa
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import pyperclip

# -----------------------------
# 🔐 Affine Cipher Core Logic
# -----------------------------
ALPHABET_SIZE = 26

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encrypt(plaintext, a, b):
    result = []
    for ch in plaintext:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            x = ord(ch) - ord(base)
            y = (a * x + b) % ALPHABET_SIZE
            result.append(chr(y + ord(base)))
        else:
            result.append(ch)
    return ''.join(result)

def affine_decrypt(ciphertext, a, b):
    a_inv = mod_inverse(a, ALPHABET_SIZE)
    if a_inv is None:
        raise ValueError("Nilai 'a' tidak memiliki invers modulo 26 (tidak coprime).")
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            y = ord(ch) - ord(base)
            x = (a_inv * (y - b)) % ALPHABET_SIZE
            result.append(chr(x + ord(base)))
        else:
            result.append(ch)
    return ''.join(result)

# -----------------------------
# 🎨 GUI with ttkbootstrap
# -----------------------------
class AffineCipherApp(tb.Window):
    def __init__(self):
        super().__init__(
            title="Affine Cipher - PayVeri Security",
            themename="darkly",   # ganti: darkly, flatly, vapor, morph, solar
            size=(800, 600),
            resizable=(False, False)
        )

        # Header
        tb.Label(self, text="🔐 Affine Cipher - PayVeri Token System", 
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        # Mode
        self.mode_var = tb.StringVar(value="encrypt")
        mode_frame = tb.Frame(self)
        mode_frame.pack(pady=5)
        tb.Radiobutton(mode_frame, text="Enkripsi (Plain → Cipher)", 
                       variable=self.mode_var, value="encrypt", bootstyle="info").pack(side=LEFT, padx=10)
        tb.Radiobutton(mode_frame, text="Dekripsi (Cipher → Plain)", 
                       variable=self.mode_var, value="decrypt", bootstyle="success").pack(side=LEFT, padx=10)

        # Input
        tb.Label(self, text="Masukkan Teks:", font=("Segoe UI", 11)).pack(pady=(10, 3))
        self.input_box = tb.Text(self, height=6, font=("Consolas", 12))
        self.input_box.pack(fill=X, padx=30, pady=5)

        # Keys
        key_frame = tb.Frame(self)
        key_frame.pack(pady=5)
        tb.Label(key_frame, text="Nilai a (coprime 26):").grid(row=0, column=0, padx=5)
        self.a_entry = tb.Entry(key_frame, width=6)
        self.a_entry.insert(0, "5")
        self.a_entry.grid(row=0, column=1, padx=5)

        tb.Label(key_frame, text="Nilai b (0–25):").grid(row=0, column=2, padx=5)
        self.b_entry = tb.Entry(key_frame, width=6)
        self.b_entry.insert(0, "8")
        self.b_entry.grid(row=0, column=3, padx=5)

        tb.Button(key_frame, text="✅ Cek Kunci", bootstyle="secondary", 
                  command=self.check_keys).grid(row=0, column=4, padx=5)

        # Buttons
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=10)
        tb.Button(btn_frame, text="🚀 Jalankan", bootstyle="primary", command=self.run_cipher, width=15).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="🧹 Bersihkan", bootstyle="danger", command=self.clear_text, width=12).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="📋 Salin Hasil", bootstyle="success", command=self.copy_output, width=12).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="🎯 Contoh Otomatis", bootstyle="info", command=self.sample_input, width=15).pack(side=LEFT, padx=5)

        # Output
        tb.Label(self, text="Hasil Output:", font=("Segoe UI", 11)).pack(pady=(10, 3))
        self.output_box = tb.Text(self, height=6, font=("Consolas", 12))
        self.output_box.pack(fill=X, padx=30, pady=5)

        # Status bar
        self.status = tb.Label(self, text="Ready", bootstyle="inverse-secondary", anchor="w")
        self.status.pack(fill=X, pady=(5, 0))
        

        # Watermark (posisi pojok kanan bawah)
        wm_label = tb.Label(
        self,
        text="© 2025 | Made by PIKI 💡",
        font=("Segoe UI", 9, "italic"),
        foreground="#AAAAAA",   # warna abu-abu lembut biar elegan
        background=self.cget("background")  # samain warna dengan window
        )
        wm_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)


    # -----------------------------
    # 🔧 Functionality
    # -----------------------------
    def check_keys(self):
        try:
            a = int(self.a_entry.get())
            b = int(self.b_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka integer untuk a dan b.")
            return

        if gcd(a, 26) != 1:
            messagebox.showerror("Kunci a Salah", f"Nilai a={a} tidak coprime dengan 26.\nGunakan salah satu: 1,3,5,7,9,11,15,17,19,21,23,25.")
            return
        if not (0 <= b < 26):
            messagebox.showerror("Kunci b Salah", "Nilai b harus antara 0–25.")
            return
        messagebox.showinfo("Valid", f"Kunci OK ✅ (a={a}, b={b})")
        self.status.config(text=f"Kunci valid: (a={a}, b={b})")

    def run_cipher(self):
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Kosong", "Masukkan teks terlebih dahulu.")
            return
        try:
            a = int(self.a_entry.get())
            b = int(self.b_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Kunci harus berupa angka.")
            return

        if gcd(a, 26) != 1:
            messagebox.showerror("Error", "Nilai a tidak coprime dengan 26.")
            return

        try:
            if self.mode_var.get() == "encrypt":
                result = affine_encrypt(text, a, b)
                self.status.config(text="Enkripsi selesai ✅")
            else:
                result = affine_decrypt(text, a, b)
                self.status.config(text="Dekripsi selesai ✅")
        except Exception as e:
            messagebox.showerror("Kesalahan", str(e))
            return

        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", result)

    def clear_text(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.status.config(text="Dibersihkan 🧹")

    def copy_output(self):
        result = self.output_box.get("1.0", "end").strip()
        if not result:
            messagebox.showinfo("Kosong", "Tidak ada output untuk disalin.")
            return
        pyperclip.copy(result)
        messagebox.showinfo("Disalin", "Output berhasil disalin ke clipboard 📋")

    def sample_input(self):
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", "PayVeri2025-Token")
        self.a_entry.delete(0, "end"); self.a_entry.insert(0, "5")
        self.b_entry.delete(0, "end"); self.b_entry.insert(0, "8")
        self.status.config(text="Contoh token dimuat 🎯")

# -----------------------------
# 🚀 Run
# -----------------------------
if __name__ == "__main__":
    app = AffineCipherApp()
    app.mainloop()
