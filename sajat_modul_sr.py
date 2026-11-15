import csv
import os

def sr_adat_ellenorzo(datum, tipus, osszeg):
    if not datum.strip() or not tipus.strip() or not osszeg.strip():
        return False, "Minden mezőt kötelező kitölteni!"
    try:
        float(osszeg)
        if float(osszeg) < 0:
            return False, "Az összeg nem lehet negatív!"
    except ValueError:
        return False, "A költség mezőbe érvényes számot kell írni!"
    return True, "OK"

def sr_penz_formazo(osszeg):
    try:
        return f"{float(osszeg):,.0f} Ft"
    except ValueError:
        return "0 Ft"

def sr_statisztika_kiir(tetelek_szama, ossz_koltseg):
    return f"Összes tétel: {tetelek_szama} db | Teljes költség: {sr_penz_formazo(ossz_koltseg)}"


class SzervizKezeloSR:
    
    def __init__(self, fajl_nev="szerviz_naplo.csv"):
        self.fajl_nev = fajl_nev
        self.tetelek = []
        self.sr_tetelek_betoltese()

    def sr_tetelek_betoltese(self):
        if os.path.exists(self.fajl_nev):
            try:
                with open(self.fajl_nev, mode="r", encoding="utf-8") as f:
                    olvaso = csv.reader(f)
                    for sor in olvaso:
                        if len(sor) == 3:
                            self.tetelek.append({"datum": sor[0], "tipus": sor[1], "osszeg": float(sor[2])})
            except Exception:
                pass

    def sr_uj_tetel_hozzaad(self, datum, tipus, osszeg):
        uj_elem = {"datum": datum, "tipus": tipus, "osszeg": float(osszeg)}
        self.tetelek.append(uj_elem)
        self.sr_fajlba_ment()

    def sr_koltsseg_osszegzes(self):
        return sum(t["osszeg"] for t in self.tetelek)

    def sr_fajlba_ment(self):
        try:
            with open(self.fajl_nev, mode="w", newline="", encoding="utf-8") as f:
                iro = csv.writer(f)
                for t in self.tetelek:
                    iro.writerow([t["datum"], t["tipus"], t["osszeg"]])
        except Exception:
                pass