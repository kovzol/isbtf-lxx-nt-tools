#!/usr/bin/python3

from isbtf_lxx_nt.tools import *
from bibref.tools import *

gnt = "SBLGNT"

set_bibref_path("bibref")

def object_nt_bibref(o):
    """
    Extract data from NT object in bibref format.
    :param o: input object
    :return: various parts of the object as dict
    """
    ret = dict()
    # Search for exact position of the quotation text in gnt:
    bibref_passage_container = f'{o["book"]} {o["chapter"]}:{o["verse_start"]} {o["chapter"]}:{o["verse_end"]}'
    l_container = lookup_n(1, gnt + " " + bibref_passage_container)
    f_container = find_n(1, gnt)[0] # TODO: This may be a longer list, fix this issue.
    qlatin = text_n(2, o["quotation_text"])
    q = find_n(2, gnt)
    for m in q:
        if f_container[1] <= m[1] and m[2] <= f_container[2]:
            match = m
            break
    ret["q_fullform"] = f'{match[0]} ({match[1]}-{match[2]})'
    ret["q_verseonly"] = ret["q_fullform"].split(' ', 1)[1]
    ret["q_azform"] = qlatin

    # Search for exact position of the intro text in gnt:
    bibref_passage_container = f'{o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]} {o["intro_chapter"]}:{o["intro_verse_end"]}'
    l_container = lookup_n(1, gnt + " " + bibref_passage_container)
    f_container = find_n(1, gnt)[0] # TODO: This may be a longer list, fix this issue.
    qlatin = text_n(2, o["intro_text"])
    q = find_n(2, gnt)
    for m in q:
        if f_container[1] <= m[1] and m[2] <= f_container[2]:
            match = m
            break
    ret["i_fullform"] = f'{match[0]} ({match[1]}-{match[2]})'
    ret["i_verseonly"] = ret["i_fullform"].split(' ', 1)[1]
    ret["i_azform"] = qlatin
    return ret

print(passage_str_list("Lk 1 2"))
o = get_object("3918")
print(f'{o["quotation_text"]}: {o["book"]} {o["chapter"]}:{o["verse_start"]}-{o["verse_end"]}')
print(f'{o["intro_text"]}: {o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]}-{o["intro_verse_end"]}')

# print(getrefs_maxlength("SBLGNT LXX Psalms 2"))
print(text_n(1, o["quotation_text"]))
print(find_n(1, "LXX"))
# print(find_n(1, "SBLGNT"))

print(text_n(2, o["intro_text"]))
print(find_n(2, "SBLGNT"))

print(object_nt_bibref(o))
