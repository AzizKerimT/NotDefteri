import customtkinter as ctk
from tkinter import messagebox
import os
from datetime import datetime

ctk.set_appearance_mode("System")  # "Dark", "Light", "System"
ctk.set_default_color_theme("blue")

NOT_KLASORU = "Notlar"
os.makedirs(NOT_KLASORU, exist_ok=True)

class NotDefteriApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Not Defteri")
        self.geometry("700x500")
        self.resizable(False, False)

        # Tema seçici
        self.tema_secici = ctk.CTkOptionMenu(self, values=["Dark", "Light", "System"], command=self.tema_degistir)
        self.tema_secici.set("System")
        self.tema_secici.pack(pady=10)

        # Başlık girişi
        self.baslik_giris = ctk.CTkEntry(self, placeholder_text="Not Başlığı")
        self.baslik_giris.pack(padx=20, pady=10, fill="x")

        # İçerik kutusu
        self.icerik_kutusu = ctk.CTkTextbox(self, height=150)
        self.icerik_kutusu.pack(padx=20, pady=10, fill="both", expand=True)

        # Butonlar
        btn_cerceve = ctk.CTkFrame(self)
        btn_cerceve.pack(pady=10)

        self.kaydet_btn = ctk.CTkButton(btn_cerceve, text="Kaydet", command=self.not_kaydet)
        self.kaydet_btn.pack(side="left", padx=10)

        self.sil_btn = ctk.CTkButton(btn_cerceve, text="Sil", command=self.not_sil)
        self.sil_btn.pack(side="left", padx=10)

        # Arama kutusu
        self.arama_giris = ctk.CTkEntry(self, placeholder_text="Not Ara (başlığa göre)", width=300)
        self.arama_giris.pack(pady=5)
        self.arama_giris.bind("<KeyRelease>", self.notlari_listele)

        # Not listesi
        self.not_listbox = ctk.CTkOptionMenu(self, values=["(Henüz not yok)"], command=self.not_ac)
        self.not_listbox.pack(pady=5, fill="x", padx=20)

        self.notlari_listele()

    def tema_degistir(self, tema):
        ctk.set_appearance_mode(tema)

    def not_kaydet(self):
        baslik = self.baslik_giris.get().strip()
        icerik = self.icerik_kutusu.get("0.0", "end").strip()

        if not baslik or not icerik:
            messagebox.showwarning("Eksik", "Başlık ve içerik boş olamaz.")
            return

        zaman = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dosya_adi = os.path.join(NOT_KLASORU, f"{baslik}_{zaman}.txt")
        with open(dosya_ani := dosya_adi, "w", encoding="utf-8") as f:
            f.write(f"Başlık: {baslik}\nTarih: {zaman}\n\n{icerik}")

        messagebox.showinfo("Kayıt Başarılı", f"{baslik} adlı not kaydedildi.")
        self.baslik_giris.delete(0, "end")
        self.icerik_kutusu.delete("0.0", "end")
        self.notlari_listele()

    def notlari_listele(self, event=None):
        arama = self.arama_giris.get().lower()
        dosyalar = os.listdir(NOT_KLASORU)
        filtreli = [d for d in dosyalar if arama in d.lower()]
        if filtreli:
            self.not_listbox.configure(values=filtreli)
            self.not_listbox.set(filtreli[0])
        else:
            self.not_listbox.configure(values=["(Not bulunamadı)"])
            self.not_listbox.set("(Not bulunamadı)")

    def not_ac(self, dosya_adi):
        if not dosya_adi or "(Not bulunamadı)" in dosya_adi:
            return
        yol = os.path.join(NOT_KLASORU, dosya_adi)
        if os.path.exists(yol):
            with open(yol, "r", encoding="utf-8") as f:
                veri = f.read()
            messagebox.showinfo("Not", veri)

    def not_sil(self):
        dosya_adi = self.not_listbox.get()
        if dosya_adi and "(Not bulunamadı)" not in dosya_adi:
            yol = os.path.join(NOT_KLASORU, dosya_adi)
            if os.path.exists(yol):
                os.remove(yol)
                messagebox.showinfo("Silindi", f"{dosya_adi} silindi.")
                self.notlari_listele()

if __name__ == "__main__":
    app = NotDefteriApp()
    app.mainloop()
