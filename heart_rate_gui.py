import os
import customtkinter as ctk 
from tkinter import messagebox
import joblib
import pandas as pd
from PIL import Image, ImageTk

# Pastikan instalasi: pip install customtkinter pandas pillow

class HeartRateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🫀 Prediksi Detak Jantung")
        self.geometry("480x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Path direktori saat ini
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Load model dan encoder
        try:
            self.model = joblib.load(os.path.join(base_dir, 'detak_jantung_model.pkl'))
            self.le_gender = joblib.load(os.path.join(base_dir, 'encoder_gender.pkl'))
            self.le_target = joblib.load(os.path.join(base_dir, 'encoder_target.pkl'))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal load model: {e}")
            self.destroy()
            return

        # Header dengan ikon
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(10, 20))

        # Load image ikon
        icon_path = os.path.join(base_dir, 'heart_rate_icon.png')
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((64, 64), Image.ANTIALIAS)
            self.icon_img = ImageTk.PhotoImage(img)
            ctk.CTkLabel(header, image=self.icon_img, text="").pack(side="left", padx=(20, 10))

        ctk.CTkLabel(header, text="Heart Rate Predictor", font=(None, 24, "bold")).pack(side="left", pady=15)

        # Frame input
        form = ctk.CTkFrame(self)
        form.pack(padx=20, pady=10, fill="both", expand=True)

        self.entries = {}
        fields = ["Usia", "Jenis Kelamin", "Istirahat (bpm)", "Maksimum (bpm)", "Sistolik", "Diastolik"]
        for i, field in enumerate(fields):
            ctk.CTkLabel(form, text=field).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            if field == "Jenis Kelamin":
                widget = ctk.CTkOptionMenu(form, values=["Laki-laki", "Perempuan"], width=180)
                widget.set("Laki-laki")
            else:
                widget = ctk.CTkEntry(form, width=180, placeholder_text=f"Masukkan {field}")
            widget.grid(row=i, column=1, pady=5, padx=5)
            self.entries[field] = widget

        # Tombol prediksi
        predict_btn = ctk.CTkButton(self, text="Prediksi Sekarang", command=self.predict)
        predict_btn.pack(pady=(10, 5))

        # Tombol reset
        reset_btn = ctk.CTkButton(self, text="Hapus Semua Data", fg_color="#D32F2F", hover_color="#B71C1C", command=self.reset)
        reset_btn.pack(pady=(5, 20))

        # Label hasil
        self.result_label = ctk.CTkLabel(self, text="", font=(None, 20, "bold"))
        self.result_label.pack(pady=10)

        # Zone info frame
        self.zone_frame = ctk.CTkFrame(self)
        self.zone_frame.pack(padx=20, fill="x")

    def predict(self):
        try:
            # Validasi dan ambil input
            usia = int(self.entries["Usia"].get().strip())
            gender = self.entries["Jenis Kelamin"].get()
            rest = int(self.entries["Istirahat (bpm)"].get().strip())
            maxb = int(self.entries["Maksimum (bpm)"].get().strip())
            sys = int(self.entries["Sistolik"].get().strip())
            dia = int(self.entries["Diastolik"].get().strip())

            if rest >= maxb:
                raise ValueError("Istirahat BPM harus lebih kecil dari Maksimum BPM.")

            # Buat DataFrame untuk prediksi
            gender_enc = self.le_gender.transform([gender])[0]
            df = pd.DataFrame([[usia, gender_enc, rest, maxb, sys, dia]],
                              columns=["Usia", "Jenis Kelamin", "Detak Jantung Istirahat (bpm)",
                                       "Detak Jantung Maksimum (bpm)", "Tekanan Darah Sistolik (mmHg)",
                                       "Tekanan Darah Diastolik (mmHg)"])
            pred = self.model.predict(df)[0]
            kategori = self.le_target.inverse_transform([pred])[0]

            # Tampilkan hasil
            self.result_label.configure(text=f"Hasil: {kategori}")
            self.show_zone_info(kategori)
        except Exception as e:
            messagebox.showerror(title="Error", message=str(e))

    def show_zone_info(self, kategori):
        # Bersihkan frame
        for widget in self.zone_frame.winfo_children():
            widget.destroy()

        # Info zona berdasarkan kategori
        zones = {
            "Resting": "< 50% max HR (Zone 1)",
            "Warm Up": "50-60% max HR (Zone 2)",
            "Fat Burn": "60-70% max HR (Zone 3)",
            "Cardio": "70-80% max HR (Zone 4)",
            "Extreme": "> 80% max HR (Zone 5)"
        }
        info = zones.get(kategori, "N/A")
        ctk.CTkLabel(self.zone_frame, text=f"Zona: {info}", font=(None, 16)).pack(pady=10)

    def reset(self):
        # Hapus semua input dan hasil
        for field, widget in self.entries.items():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, 'end')
            else:
                widget.set("Laki-laki")
        self.result_label.configure(text="")
        for widget in self.zone_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = HeartRateApp()
    app.mainloop()
