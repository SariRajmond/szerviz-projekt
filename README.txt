# Gépjármű Szerviz- és Fenntartási Költség Követő

* **Név:** Sári Rajmond
* **Neptun-kód:** BSUMOC
* **Tantárgy:** Szkript nyelvek

## Feladat leírása
A program egy asztali, grafikus felületű gépjármű-napló, amellyel a felhasználó rögzítheti az elvégzett szerviztételeket és karbantartási költségeket. A program automatikusan összesíti a kiadásokat, lehetővé teszi a tételek szűrését, valamint CSV fájlba menti az adatokat a perzisztencia érdekében.

## Felhasználói leírás
* **Szükséges környezet:** Python 3.x.
* **Telepítés:** Nincs szükség külső könyvtárak telepítésére.
* **Indítás:** A program a `main.py` fájl futtatásával indítható el.

## Felépítés
* **Modulok:**
  * `sajat_modul_sr.py`: Tartalmazza a szerviztétel adatok kezelésére szolgáló `SzervizKezeloSR` osztályt, valamint a validáló és formázó függvényeket.
  * `main.py`: A grafikus felületet és a fő vezérlést megvalósító alkalmazás.
* **Függvények:**
  * `sr_adat_ellenorzo(...)`: Ellenőrzi a kitöltött mezők érvényességét.
  * `sr_penz_formazo(...)`: Pénzösszegek formázása.
  * `sr_statisztika_kiir(...)`: Eredmények formázása kiíratáshoz.
* **Osztályok:**
  * `SzervizKezeloSR`: Osztály a szerviztételek tárolására, hozzáadására, szűrésére és CSV fájlba történő mentésére/betöltésére.
    * Metódusai: `sr_tetelek_betoltese()`, `sr_uj_tetel_hozzaad()`, `sr_koltsseg_osszegzes()`.