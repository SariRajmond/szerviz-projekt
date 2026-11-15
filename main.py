import tkinter as tk
from tkinter import messagebox
from sajat_modul_sr import SzervizKezeloSR, sr_adat_ellenorzo, sr_penz_formazo, sr_statisztika_kiir


class AppSR:
    def __init__(self, ablak):
        self.ablak = ablak
        self.ablak.title("Gépjármű Szerviz- és Fenntartási Költség Követő (BSUMOC)")
        self.ablak.geometry("680x550")

        self.kezelo = SzervizKezeloSR()
        self.megjelenitett_indexek = []

        tk.Label(self.ablak, text="Gépjármű Szerviz- és Költségkövető", font=("Arial", 14, "bold")).pack(pady=10)

        keret_bevitel = tk.Frame(self.ablak)
        keret_bevitel.pack(pady=5)

        tk.Label(keret_bevitel, text="Dátum (ÉÉÉÉ.HH.NN):").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.entry_datum = tk.Entry(keret_bevitel, width=25)
        self.entry_datum.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(keret_bevitel, text="Szerviz Típusa / Munkálat:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.entry_tipus = tk.Entry(keret_bevitel, width=25)
        self.entry_tipus.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(keret_bevitel, text="Költség (Ft):").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.entry_osszeg = tk.Entry(keret_bevitel, width=25)
        self.entry_osszeg.grid(row=2, column=1, padx=5, pady=3)

        keret_gombok = tk.Frame(self.ablak)
        keret_gombok.pack(pady=8)

        self.gomb_mentes = tk.Button(keret_gombok, text="Tétel Rögzítése", bg="lightgreen", width=18, command=self.sr_tetel_rogzites_esemeny)
        self.gomb_mentes.grid(row=0, column=0, padx=5)

        self.gomb_torles = tk.Button(keret_gombok, text="Kijelölt Törlése", bg="salmon", width=18, command=self.sr_tetel_torles_esemeny)
        self.gomb_torles.grid(row=0, column=1, padx=5)

        keret_kereses = tk.Frame(self.ablak)
        keret_kereses.pack(pady=5)

        tk.Label(keret_kereses, text="Keresés / Szűrés:").grid(row=0, column=0, padx=5)
        self.entry_kereses = tk.Entry(keret_kereses, width=25)
        self.entry_kereses.grid(row=0, column=1, padx=5)

        self.gomb_szures = tk.Button(keret_kereses, text="Szűrés", command=self.sr_szures_esemeny)
        self.gomb_szures.grid(row=0, column=2, padx=5)

        self.gomb_osszes = tk.Button(keret_kereses, text="Összes mutása", command=self.sr_szures_torles_esemeny)
        self.gomb_osszes.grid(row=0, column=3, padx=5)

        self.listbox_tetelek = tk.Listbox(self.ablak, width=80, height=12)
        self.listbox_tetelek.pack(pady=5)

        self.label_statisztika = tk.Label(self.ablak, text="", font=("Arial", 10, "bold"))
        self.label_statisztika.pack(pady=10)

        self.sr_lista_frissit()

    def sr_tetel_rogzites_esemeny(self):
        datum = self.entry_datum.get()
        tipus = self.entry_tipus.get()
        osszeg = self.entry_osszeg.get()

        sikeres, uzenet = sr_adat_ellenorzo(datum, tipus, osszeg)
        if not sikeres:
            messagebox.showerror("Adatbevitel Hiba", uzenet)
            return

        if messagebox.askyesno("Megerősítés", "Biztosan rögzíteni szeretnéd az új szerviztételt?"):
            self.kezelo.sr_uj_tetel_hozzaad(datum, tipus, osszeg)
            self.entry_datum.delete(0, tk.END)
            self.entry_tipus.delete(0, tk.END)
            self.entry_osszeg.delete(0, tk.END)
            self.sr_lista_frissit()
            messagebox.showinfo("Siker", "A szerviztétel sikeresen rögzítve és elmentve a CSV fájlba!")

    def sr_tetel_torles_esemeny(self):
        kijeloles = self.listbox_tetelek.curselection()
        if not kijeloles:
            messagebox.showwarning("Figyelmeztetés", "Kérlek, válassz ki egy tételt a listából a törléshez!")
            return

        listbox_index = kijeloles[0]
        valodi_index = self.megjelenitett_indexek[listbox_index]

        if messagebox.askyesno("Törlés megerősítése", "Biztosan törölni szeretnéd a kijelölt szerviztételt?"):
            self.kezelo.sr_tetel_torlese(valodi_index)
            self.sr_lista_frissit(self.entry_kereses.get())
            messagebox.showinfo("Törölve", "A tétel sikeresen törölve lett!")

    def sr_szures_esemeny(self):
        kulcsszo = self.entry_kereses.get()
        self.sr_lista_frissit(kulcsszo)

    def sr_szures_torles_esemeny(self):
        self.entry_kereses.delete(0, tk.END)
        self.sr_lista_frissit()

    def sr_lista_frissit(self, kulcsszo=""):
        self.listbox_tetelek.delete(0, tk.END)
        self.megjelenitett_indexek.clear()

        talalatok = self.kezelo.sr_kereses(kulcsszo)
        szurt_tetelek = []

        for eredeti_index, tetel in talalatok:
            sor = f"{tetel['datum']}  |  {tetel['tipus']}  -  {sr_penz_formazo(tetel['osszeg'])}"
            self.listbox_tetelek.insert(tk.END, sor)
            self.megjelenitett_indexek.append(eredeti_index)
            szurt_tetelek.append(tetel)

        ossz = self.kezelo.sr_koltsseg_osszegzes(szurt_tetelek)
        atlag = self.kezelo.sr_atlag_koltseg(szurt_tetelek)
        szoveg = sr_statisztika_kiir(len(szurt_tetelek), ossz, atlag)
        self.label_statisztika.config(text=szoveg)


if __name__ == "__main__":
    root_ablak = tk.Tk()
    app = AppSR(root_ablak)
    root_ablak.mainloop()