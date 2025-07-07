#!/usr/bin/python3

# This is a basic demo that reads all files from html-re/ and shows the entries in a simple way.

from bs4 import BeautifulSoup
import os

html_re_folder = "isbtf_lxx_nt/html-re"

books_translated_de = {
    'Mt': "Matthew",
    'Jes': "Isaiah",
    '1Chr': "I_Chronicles",
    'Kön_I': "I_Kings",
    'Kön_II': "II_Kings",
    'Kön_III': "III_Kings", # ?
    'Kön_IV': "IV_Kings", # ?
    'Mi': "Micah",
    'Hos': "Hosea",
    'Jer': "Jeremiah",
    'Ri': "Judges",
    'Dtn': "Deuteronomy",
    'Ps': "Psalms",
    'Ex': "Exodus",
    'Mal': "Malachi",
    'Jona': "Jonah",
    'Lev': "Leviticus",
    'Gen': "Genesis",
    'Sach': "Zechariah",
    'Jos': "Joshua",
    'Dan': "Daniel",
    'Num': "Numbers",
    'Sir': "Sirach",
    'Hab': "Habakkuk",
    'Spr': "Proverbs",
    'Ijob': "Job",
    'Koh': "Ecclesiastes",
    'Röm': "Romans",
    '2Tim': "II_Timothy",
    '1Tim': "I_Timothy",
    '1Kor': "I_Corinthians",
    '2Kor': "II_Corinthians",
    'Od': "Odes",
    'Mk': "Mark",
    'Ez': "Ezekiel",
    'Eph': "Ephesians",
    'Acta': "Acts",
    '2Esdr': "II_Esdras", # ?
    'Am': "Amos",
    'Gal': "Galatians",
    'Jud': "Jude",
    'Jak': "James",
    'Joh': "John",
    'Hag': "Haggai",
    '1Petr': "I_Peter",
    'Hebr': "Hebrews",
    'Lk': "Luke"
    }

def detect_passage(passage):
    passage_arr = passage.split(" ")
    if passage_arr[0] in books_translated_de:
        book = books_translated_de[passage_arr[0]]
    else:
        book = passage_arr[0]
    chapter = passage_arr[1].replace(",", "")
    verse = passage_arr[2]
    return book, chapter, verse

def get_object(nr):
    marked_quotation = False
    waitfor = ""
    object_html = open(html_re_folder + "/" + nr + ".html", "r")
    soup = BeautifulSoup(object_html, "lxml")
    tds = soup.find_all("td")
    for td in tds:
        item = td.get_text()
        if waitfor == "quotation_text":
            quotation_text = item
        if item == "\nmarkiertes Zitat":
            marked_quotation = True
        if item.endswith("Zitattext ohne Akzente"):
            waitfor = "quotation_text"
        else:
            waitfor = ""
    if marked_quotation:
        print(quotation_text)
    object_html.close()

directory = os.fsencode(html_re_folder + "/.")

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".html"): 
        source = open(html_re_folder + "/" + filename, "r")
        soup = BeautifulSoup(source, "lxml")
        lis = soup.find_all('li')
        for li in lis:
            item = li.get_text()
            a = str(li.a)
            if "(Neues Testament)" in item:
                lines = item.splitlines()
                for line in lines:
                    line = line.replace("Kön ", "Kön_")
                    if "(Neues Testament)" in line:
                        print()
                        first_paren = line.index('(')
                        nt_passage = line[0:first_paren-1]
                        nt_book, nt_chapter, nt_verse = detect_passage(nt_passage)
                        print(f"{nt_book}-{nt_chapter},{nt_verse} refers to", end='')
                    if "(LXX-Zitat-Adresse)" in line:
                        first_paren = line.index('(')
                        ot_passage = line[0:first_paren-1]
                        ot_book, ot_chapter, ot_verse = detect_passage(ot_passage)
                        print(f" {ot_book} {ot_chapter}:{ot_verse}", end='')
                # print()
            else:
                if "(NT-Zitat-Adresse)" in item:
                    first_paren = a.index('(')
                    first_comma = a.index(',')
                    object_nr = a[first_paren+1:first_comma]
                    print(f" obj={object_nr}", end='')
                    get_object(object_nr)
        source.close()
