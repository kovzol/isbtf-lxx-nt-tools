from bs4 import BeautifulSoup
import os

html_re_folder = os.path.dirname(__file__) + "/html-re"

# Convert ISBTF's internal book names into SWORD names
books_isbtf_sword = {
    'Mt': "Matthew",
    'Jes': "Isaiah",
    '1Chr': "I_Chronicles",
    'Kön I': "I_Kings",
    'Kön II': "II_Kings",
    'Kön III': "III_Kings", # ?
    'Kön IV': "IV_Kings", # ?
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
    'Apg': "Acts",
    '2Esdr': "II_Esdras", # ?
    'Am': "Amos",
    'Gal': "Galatians",
    'Jud': "Jude",
    'Jak': "James",
    'Joh': "John",
    'Hag': "Haggai",
    '1Petr': "I_Peter",
    'Hebr': "Hebrews",
    'Lk': "Luke",
    'Joel': "Joel"
    }

nt_books_isbtf = ["Mt", "Mk", "Lk", "Joh", "Acta", "Röm", "1Kor", "2Kor",
    "Eph", "Gal", "1Tim", "2Tim", "Hebr", "1Petr", "Jud", "Jak"]

def passage_str_list(passage):
    """
    Convert a string passage into a list
    :param passage: passage as string (e.g. "Röm 2, 7")
    :return: passage as list of book, chapter, verse
    """
    # passage = passage.replace(" I", "_I") # change Kön I to Kön_I
    passage_arr = passage.split(" ")
    if passage_arr[0] in books_isbtf_sword:
        book = books_isbtf_sword[passage_arr[0]]
    else:
        book = passage_arr[0]
    chapter = passage_arr[1].replace(",", "")
    verse = passage_arr[2]
    return book, chapter, verse

def get_object(nr):
    ret = dict()
    marked_quotation = False
    waitfor = ""
    object_html = open(html_re_folder + "/" + str(nr) + ".html", "r")
    soup = BeautifulSoup(object_html, "lxml")
    tds = soup.find_all("td")

    keys = {
        "NTZ: Buch": "book",
        "NTZ: Kapitel": "chapter",
        "NTZ: Beginn Vers": "verse_start",
        "NTZ: Ende Vers": "verse_end",
        "NTZ: Zitattext ohne Akzente": "quotation_text",
        "NTZ: Einleitung Buch": "intro_book",
        "NTZ: Einleitung Kapitel": "intro_chapter",
        "NTZ: Einleitung Beginn Vers": "intro_verse_start",
        "NTZ: EInleitung Ende Vers": "intro_verse_end",
        "NTZ: Einleitungstext ohne Akzente": "intro_text",

        "LXX Buch": "book",
        "LXX Kapitel": "chapter",
        "LXX Beginn Vers": "verse_start",
        "LXX Basistext (ohne Akzente)": "quoted_text"
    }

    for td in tds:
        item = td.get_text().strip()
        waitfor_used = False
        for k in keys:
            if waitfor == keys[k]:
                if item != "": # empty items should not be stored
                    ret[keys[k]] = item
                waitfor = ""
                waitfor_used = True
                if not "testament" in keys:
                    if k.startswith("NTZ:"):
                        ret["testament"] = "n"
                    if k.startswith("LXX "):
                        ret["testament"] = "o"
        if waitfor_used:
            continue
        if item == "markiertes Zitat":
            marked_quotation = True
        for k in keys:
            if item == k:
                waitfor = keys[k]
    ret["marked_quotation"] = marked_quotation
    ret["book"] = books_isbtf_sword[ret["book"]]
    if "intro_book" in ret.keys() and ret["intro_book"] != "":
        try:
            ret["intro_book"] = books_isbtf_sword[ret["intro_book"]]
        except:
            print(f'No {ret["intro_book"]} found in books_isbtf_sword') # Warning?
    object_html.close()
    return ret

def extract_nt_objects(book):
    ret = []
    identifier = None
    nt_objects = []
    nt_ot_objects = []

    with open(html_re_folder + "/" + book + ".html") as file:
        lis = [line.rstrip() for line in file]

    for li in lis:
        items = str(li).split("<li>")

        for line in items:
            line = line.replace("Kön ", "Kön_")
            if "(Neues Testament)" in line:
                first_comma = line.index(',')
                first_paren = line.index('(')
                nt_head_object_nr = line[first_paren+1:first_comma] # e.g. 844
                first_paren_end = line.index(')')
                first_lxx_zitat = line.index(" (Neues Testament)")
                identifier = line[first_paren_end+3:first_lxx_zitat] # e.g. Acta 1, 20
            if "(NT-Zitat-Adresse)" in line:
                first_comma = line.index(',')
                first_paren = line.index('(')
                nt_obj = int(line[first_paren+1:first_comma]) # e.g. 3918 (this can be repeated for another fragment)
            if "(LXX-Zitat-Adresse)" in line:
                first_paren_end = line.index(')')
                first_lxx_zitat = line.index(" (LXX-Zitat-Adresse)")
                ot_passage = line[first_paren_end+3:first_lxx_zitat] # e.g. Ps 2, 7
                nt_objects.append([nt_obj, ot_passage]) # register this fragment pair for processing them below
            if "(LXX)" in line:
                for nt_obj in nt_objects:
                    entry = nt_obj[1] + " (LXX)"
                    if entry in line and not (entry + "]") in line:
                        first_paren = line.index('(')
                        first_comma = line.index(',')
                        ot_obj = int(line[first_paren+1:first_comma])
                        nt_ot_objects.append([nt_obj[0], ot_obj])
        if identifier != None and len(nt_ot_objects)>0 and len(nt_objects) == len(nt_ot_objects):
            ret.append([identifier, nt_ot_objects])
            identifier = None
            nt_objects = []
            nt_ot_objects = []
    return ret
