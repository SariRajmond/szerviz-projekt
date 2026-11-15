import csv
import os

def sr_adat_ellenorzo(datum, tipus, osszeg):
    if not datum.strip() or not tipus.strip() or not osszeg.strip():
        return False, "Minden mezőt kötelező kitölteni!"
    try:
        ertek = float(osszeg)
        if ertek <= 0:
            return False, "Az összegnek pozitív számnak kell lennie!"
    except ValueError:
        return False, "A költség mezőbe érvényes számot kell írni!"
    return True, "OK"

def sr_penz_formazo(osszeg):
    try:
        return f"{float(osszeg):,.0f} Ft".replace(",", " ")
    except ValueError:
        return "0 Ft"

def sr_statisztika_kiir(tetelek_szama, ossz_koltseg, atlag_koltseg):
    return (f"Tételek: {tetelek_szama} db | "
            f"Összesen: {sr_penz_formazo(ossz_koltseg)} | "
            f"Átlag: {sr_penz_formazo(atlag_koltseg)}")


class SzervizKezeloSR:
    def __init__(self, fajl_nev="szerviz_naplo.csv"):
        self.fajl_nev = fajl_nev
        self.tetelek = []
        self.sr_tetelek_betoltese()

    def sr_tetelek_betoltese(self):
        self.tetelek.clear()
        if os.path.exists(self.fajl_nev):
            try:
                with open(self.fajl_nev, mode="r", encoding="utf-8") as f:
                    olvaso = csv.reader(f)
                    for sor in olvaso:
                        if len(sor) == 3:
                            self.tetelek.append({
                                "datum": sor[0],
                                "tipus": sor[1],
                                "osszeg": float(sor[2])
                            })
            except Exception:
                pass

    def sr_uj_tetel_hozzaad(self, datum, tipus, osszeg):
        uj_elem = {"datum": datum.strip(), "tipus": tipus.strip(), "osszeg": float(osszeg)}
        self.tetelek.append(uj_elem)
        self.sr_fajlba_ment()

    def sr_tetel_torlese(self, index):
        if 0 <= index < len(self.tetelek):
            del self.tetelek[index]
            self.sr_fajlba_ment()

    def sr_koltsseg_osszegzes(self, lista=None):
        cel_lista = self.tetelek if lista is None else lista
        return sum(t["osszeg"] for t in cel_lista)

    def sr_atlag_koltseg(self, lista=None):
        cel_lista = self.tetelek if lista is None else lista
        if not cel_lista:
            return 0.0
        return self.sr_koltsseg_osszegzes(cel_lista) / len(cel_lista)

    def sr_kereses(self, kulcsszo):
        k = kulcsszo.strip().lower()
        if not k:
            return list(enumerate(self.tetelek))
        return [
            (i, t) for i, t in enumerate(self.tetelek)
            if k in t["tipus"].lower() or k in t["datum"].lower()
        ]

    def sr_fajlba_ment(self):
        try:
            with open(self.fajl_nev, mode="w", newline="", encoding="utf-8") as f:
                iro = csv.writer(f)
                for t in self.tetelek:
                    iro.writerow([t["datum"], t["tipus"], t["osszeg"]])
        except Exception:
            pass