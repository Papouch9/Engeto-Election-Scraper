'''
ELECTIONS SCRAPER: Treti projekt do Engeto Online Python Akademie
author: Miroslav Kalík
email: mira.kalik@seznam.cz
discord: mira_47271
'''

import sys
import requests
import bs4
import csv

def nacti_jednotlive_obce(adresa: str) -> tuple:
    seznam = []
    try:
        html_soubor = requests.get(adresa)
    except:
        print("Nezadal jsi platnou adresu.\n"
              "Program bude ukončen.")
        exit()
    kod_okresu = adresa[-4:]
    rozdeleny_html_soubor = bs4.BeautifulSoup(html_soubor.text, features="html.parser")

    for tab in range(1, 4):
        nactene_obce = rozdeleny_html_soubor.find_all("td", {"class": "cislo", "headers": f"t{tab}sa1 t{tab}sb1"})
    for no in nactene_obce:
        seznam.append(no.get_text())
        #seznam[i] = (str(seznam[i])[87:93])
    return seznam, kod_okresu


def nacti_vysledky_obci(seznam_obci: tuple) -> list:
    okres = seznam_obci[1]
    celkova_statistika = []
    for i in seznam_obci[0]:
        strany = []
        hlasy = []
        adresa = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec={i}&xvyber={okres}"
        html_soubor = requests.get(adresa)
        rozdeleny_html_soubor = bs4.BeautifulSoup(html_soubor.text, features="html.parser")
        jmeno_obce = rozdeleny_html_soubor.select_one(".topline > h3:nth-child(4)").text[7:]
        registrovanych = rozdeleny_html_soubor.find("td", {"class": "cislo", "headers": "sa2"})
        obalek = rozdeleny_html_soubor.find("td", {"class": "cislo", "headers": "sa3"})
        platne_hlasy = rozdeleny_html_soubor.find("td", {"class": "cislo", "headers": "sa6"})
        statistika_obce = {"code": i,
                           "location": jmeno_obce.strip(),
                           "registered": registrovanych.text.replace('\xa0', ''),
                           "envelopes": obalek.text.replace('\xa0', ''),
                           "valid": platne_hlasy.text.replace('\xa0', '')}

        for tab in range(1, 3):
            nactene_strany = rozdeleny_html_soubor.find_all("td", {"class": "overflow_name", "headers": f"t{tab}sa1 t{tab}sb2"})
            for ns in nactene_strany:
                strany.append(ns.get_text())
            nactene_hlasy = rozdeleny_html_soubor.find_all("td", {"class": "cislo", "headers": f"t{tab}sa2 t{tab}sb3"})
            for nh in nactene_hlasy:
                hlasy.append(nh.get_text().replace('\xa0', ''))

        zaznamy = list(zip(strany, hlasy))
        statistika_obce.update(zaznamy)
        celkova_statistika.append(statistika_obce)
    return celkova_statistika

def zapis_do_souboru(soubor: str, statistika: list) -> None:
    with open(soubor, mode="w", encoding="UTF-8", newline='') as otevreny_soubor:
        zahlavi = statistika[0].keys()
        zapis = csv.DictWriter(otevreny_soubor, fieldnames=zahlavi)
        zapis.writeheader()
        zapis.writerows(statistika)
    print(f"Statistiky byly stazeny do souboru {soubor}.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Nezadal jsi povinný počet argumentů pro běh programu.\n"
              "Program bude nyní ukončen.")
        exit()
    else:
        zapis_do_souboru(sys.argv[1], nacti_vysledky_obci(nacti_jednotlive_obce(sys.argv[2])))

