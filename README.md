Ahoj,
tento program stahne a ulozi oficialni volebni vysledky v obcich, ktere se nachazeji ve volebnim okrsku, ktery si uzivatel vybere. 

Pokracujte v prikazovem radku:

Pro stazeni potrebnych knihoven pouzijte:
  pip install -r requirements.txt

Pro spusteni potrebneho virtualniho prostredi pouzijte:
  moje_prostredi\Scripts\Activate.ps1

Pro spusteni programu:
  python main.py <stranka_pozadovaneho_okresu> <jmeno_souboru_k_ulozeni>
  
  napr.
  
  python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky.csv"

ENJOY
