"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Galyna Kopiychak
email: galynakopiychak@outlook.com
"""
import sys  # práce s argumenty příkazové řádky
import requests  # stahování dat z internetu
from bs4 import BeautifulSoup  # práce s HTML strukturou
import csv  # práce s CSV soubory
from urllib.parse import urljoin  # spojení URL adres

def zkontroluj_argumenty() -> tuple[str, str]:
    """Zkontroluje počet argumentů a vrátí URL a název výstupního souboru."""
    if len(sys.argv) != 3:
        print("Zadej 2 argumenty: URL a název výstupního souboru.")
        print('Např.: python main.py "https://www.volby.cz/..." "vysledky.csv"')
        sys.exit(1)

    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    if not url.startswith("http"):
        print("Chyba: První argument musí být URL začínající na 'http'")
        sys.exit(1)

    if not vystupni_soubor.endswith(".csv"):
        print("Chyba: Druhý argument musí být název souboru končící na '.csv'")
        sys.exit(1)

    return url, vystupni_soubor

def stahni_html_stranku(odkaz: str) -> BeautifulSoup:
    """Stáhne HTML stránku a vrátí ji jako BeautifulSoup objekt."""
    try:
        odpoved = requests.get(odkaz)
        odpoved.raise_for_status()
        return BeautifulSoup(odpoved.text, "html.parser")
    except Exception as e:
        print(f"Chyba při načítání stránky: {e}")
        sys.exit(1)

def ziskej_obce(soup: BeautifulSoup, vychozi_url: str) -> list[tuple[str, str, str]]:
    """Získá seznam všech obcí (kód, název, odkaz)."""
    obce = []
    tabulky = soup.find_all("table")
    if not tabulky:
        print("Chyba: žádná tabulka na stránce.")
        sys.exit(1)
    
    for tabulka in tabulky:
        for radek in tabulka.find_all("tr"):
            bunky = radek.find_all("td")
            if len(bunky) >= 3:
                kod = bunky[0].text.strip()
                nazev = bunky[1].text.strip()
                odkaz_tag = bunky[0].find("a")
                if odkaz_tag and "href" in odkaz_tag.attrs:
                    uplny_odkaz = urljoin(vychozi_url, odkaz_tag["href"])
                    obce.append((kod, nazev, uplny_odkaz))
    return obce

def filtruj_tagy(soup: BeautifulSoup, typ: str) -> list[BeautifulSoup]:
    """Vrátí všechny HTML tagy daného typu."""
    return soup.find_all(typ) if soup else []

def najdi_podle_atributu(soup: BeautifulSoup, typ: str, atributy: dict[str, str]) -> BeautifulSoup | None:
    """Najde první tag podle typu a atributů."""
    return soup.find(typ, atributy) if soup else None

def ziskej_data_z_obce(obec_odkaz: str) -> tuple[str, str, str, dict[str, str]]:
    """Získá detailní data z jedné obce."""
    soup = stahni_html_stranku(obec_odkaz)
    tabulky = filtruj_tagy(soup, "table")

    try:
        registrovani = najdi_podle_atributu(tabulky[0], "td", {"headers": "sa2"}).text.strip().replace("\xa0", "")
        obalky = najdi_podle_atributu(tabulky[0], "td", {"headers": "sa3"}).text.strip().replace("\xa0", "")
        platne = najdi_podle_atributu(tabulky[0], "td", {"headers": "sa6"}).text.strip().replace("\xa0", "")
    except Exception as e:
        print(f"Chyba při získávání údajů o voličích: {e}")
        registrovani = obalky = platne = "0"

    strany: dict[str, str] = {}
    for tab in tabulky[1:]:
        for radek in tab.find_all("tr")[2:]:
            bunky = radek.find_all("td")
            if len(bunky) >= 3:
                strana = bunky[1].text.strip()
                hlasy = bunky[2].text.strip().replace("\xa0", "")
                if strana and strana != "-":
                    strany[strana] = hlasy

    return registrovani, obalky, platne, strany

def uloz_vysledky(data: list[dict[str, str | dict[str, str]]], vystupni_csv: str) -> None:
    """Uloží všechny výsledky do CSV souboru."""
    if not data:
        print("Žádná data k uložení.")
        return

    vsechny_strany = set()
    for obec in data:
        vsechny_strany.update(strana for strana in obec["strany"].keys() if strana and strana != "-")
    seznam_stran = sorted(vsechny_strany)

    hlavicka = ["code", "location", "registered", "envelopes", "valid"] + seznam_stran

    with open(vystupni_csv, "w", newline="", encoding="utf-8") as f:
        zapisovac = csv.writer(f, delimiter=";")
        zapisovac.writerow(hlavicka)
        for obec in data:
            radek = [
                obec["kod"],
                obec["nazev"],
                obec["voliči"],
                obec["obálky"],
                obec["platné"],
            ]
            for strana in seznam_stran:
                radek.append(obec["strany"].get(strana, "0"))
            zapisovac.writerow(radek)
    print(f"Výsledky byly uloženy do souboru: {vystupni_csv}")

if __name__ == "__main__":
    odkaz, vystup = zkontroluj_argumenty()
    print(f"Načítám data z URL: {odkaz}")
    print(f"Výstupní soubor: {vystup}")

    soup = stahni_html_stranku(odkaz)
    seznam_obci = ziskej_obce(soup, odkaz)
    print(f"Nalezeno obcí: {len(seznam_obci)}")

    data_vysledku = []
    for kod, nazev, obec_url in seznam_obci:
        print(f"Zpracovávám obec: {nazev}")
        voliči, obalky, platne, strany = ziskej_data_z_obce(obec_url)
        data_vysledku.append({
            "kod": kod,
            "nazev": nazev,
            "voliči": voliči,
            "obálky": obalky,
            "platné": platne,
            "strany": strany
        })

    uloz_vysledky(data_vysledku, vystup)
    print("Hotovo.")


