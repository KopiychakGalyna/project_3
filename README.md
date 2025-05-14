
# Popis projektu

Tento projekt slouží k stažení výsledků parlamentních voleb z roku 2017 z webu [volby.cz](https://www.volby.cz). Skript umí zpracovat libovolný okres (územní celek) podle zadané URL adresy. Vybere si odkazy na jednotlivé obce a stáhne informace o počtu voličů, platných hlasů a hlasy pro každou stranu. Vše uloží do přehledné tabulky .csv.

# Použití

Skript se spouští z příkazové řádky pomocí dvou argumentů:

python main.py "<odkaz-na-okres-z-volby.cz>" "nazev_vystupniho_souboru.csv"

Například:

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2104" "vysledky_benesov.csv"

# Použité nástroje

Pracuji ve Visual Studio Code, používám PowerShell a verzi Pythonu 3.13.2.  

# Virtuální prostředí a instalace knihoven

Doporučuji si nejprve vytvořit virtuální prostředí:

python -m venv moje_virt_prostredi

Aktivace (Windows):

.\moje_virt_prostredi\Scripts\Activate.ps1

Pak nainstaluj knihovny z requirements.txt:

pip install -r requirements.txt

Seznam knihoven najdeš v `requirements.txt`. Byl vygenerován automaticky pomocí:

pip freeze > requirements.txt

# Požadované knihovny

* requests
* beautifulsoup4

#  Spuštění skriptu

Skript spouštěj pomocí dvou argumentů:
- První argument: URL stránky s výběrem obcí (např. Benešov)
- Druhý argument: název výstupního CSV souboru (musí končit `.csv`)

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"


# Ukázka výsledku

Po spuštění se v terminálu vypisují zpracované obce a vytvoří se soubor s uloženými daty např.:

Načítám data z URL: https://www.volby.cz/...
Výstupní soubor: vysledky_benesov.csv
Nalezeno obcí: 114
Zpracovávám obec: Benešov
Zpracovávám obec: Bernartice
Zpracovávám obec: Bílkovice
Zpracovávám obec: Blažejovice
...
Zpracovávám obec: Zvěstov
Výsledky byly uloženy do souboru: vysledky_benesov.csv
Hotovo.

#  Výstup

Skript vytvoří soubor `.csv`, který obsahuje:

- Kód obce
- Název obce
- Počet voličů v seznamu
- Vydané obálky
- Platné hlasy
- Hlasy pro jednotlivé strany

# Poznámky

* Skript kontroluje, jestli argumenty byly zadány správně.
* Pokud argument chybí nebo nemá formát URL/CSV, vypíše se chyba a skript skončí.





