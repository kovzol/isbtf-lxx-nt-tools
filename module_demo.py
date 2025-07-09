#!/usr/bin/python3

from isbtf_lxx_nt.tools import *
from bibref.tools import *

print(passage_str_list("Lk 1 2"))
o = get_object("3918")
print(f'{o["quotation_text"]}: {o["book"]} {o["chapter"]}:{o["verse_start"]}-{o["verse_end"]}')
print(f'{o["intro_text"]}: {o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]}-{o["intro_verse_end"]}')

# print(getrefs_maxlength("SBLGNT LXX Psalms 2"))
print(text_n(1, o["quotation_text"]))
print(find_n(1, "LXX"))
print(find_n(1, "SBLGNT"))
