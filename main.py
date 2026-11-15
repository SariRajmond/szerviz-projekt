import tkinter as tk
from tkinter import messagebox
from sajat_modul_sr import SzervizKezeloSR, sr_adat_ellenorzo, sr_penz_formazo, sr_statisztika_kiir

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gépjármű Szerviz- és Költségkövető (BSUMOC)")
        self.root.geometry("600x450")
        
        # Példányosítjuk a saját osztályunkat
        self.kezelo = SzervizKezeloSR()

        # --- GUI ELEMEK ---
        tk.Label(root, text="Gépjármű Szerviz Napló", font=("Arial", 14, "bold")).pack(pady=10)

        keret_bevitel = tk.Frame(root)
        keret_bevitel.pack(pady=5)

        tk.Label(keret_bevitel, text="Dátum (ÉÉÉÉ.HH.NN):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_datum = tk.Entry(keret_bevitel, width=20)
        self.entry_datum.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(keret_bevitel, text="Szerviz Típusa / Munkálat:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_tipus = tk.Entry(keret_bevitel, width=20)
        self.entry_tipus.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(keret_bevitel, text="Költség (Ft):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_osszeg = tk.Entry(keret_bevitel, width=20)
        self.entry_osszeg.grid(row=2, column=1, padx=5, pady=2)

        self.gomb_mentes = tk.Button(root, text="Tétel Rögzítése", bg="lightgreen", command=self.tetel_rogzites_esemeny)
        self.gomb_mentes.pack(pady=10)

        self.listbox_tetelek = tk.Listbox(root, width=70, height=10)
        self.listbox_tetelek.pack(pady=5)

        self.label_statisztika = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.label_statisztika.pack(pady=10)

        self.lista_frissit()

    def tetel_rogzites_esemeny(self):
        datum = self.entry_datum.get()
        tipus = self.entry_tipus.get()
        osszeg = self.entry_osszeg.get()

        sikeres, uzenet = sr_adat_ellenorzo(datum, tipus, osszeg)
        if not sikeres:
            messagebox.showerror("Hiba", uzenet)
            return

        self.kezelo.sr_uj_tetel_hozzaad(datum, tipus, osszeg)
        
        self.entry_datum.delete(0, tk.END)
        self.entry_tipus.delete(0, tk.END)
        self.entry_osszeg.delete(0, tk.END)

        self.lista_frissit()
        messagebox.showinfo("Siker", "A szerviztétel sikeresen rögzítve!")

    def lista_frissit(self):
        self.listbox_tetelek.delete(0, tk.END)
        for tetel in self.kezelo.tetelek:
            sor = f"{tetel['datum']} | {tetel['tipus']} - {sr_penz_formazo(tetel['osszeg'])}"
            self.listbox_tetelek.insert(tk.END, sor)
        
        ossz = self.kezelo.sr_koltsseg_osszegzes()
        szoveg = sr_statisztika_kiir(len(self.kezelo.tetelek), ossz)
        self.label_statisztika.config(text=szoveg)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()