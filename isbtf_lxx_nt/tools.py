# Convert ISBTF's internal book names into SWORD names
books_isbtf_sword = {
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

def passage_str_list(passage):
    """
    Convert a string passage into a list
    :param passage: passage as string
    :return: passage as list of book, chapter, verse
    """
    passage_arr = passage.split(" ")
    if passage_arr[0] in books_isbtf_sword:
        book = books_isbtf_sword[passage_arr[0]]
    else:
        book = passage_arr[0]
    chapter = passage_arr[1].replace(",", "")
    verse = passage_arr[2]
    return book, chapter, verse

