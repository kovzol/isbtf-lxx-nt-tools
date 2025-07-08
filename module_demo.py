#!/usr/bin/python3

from isbtf_lxx_nt.tools import *

print(passage_str_list("Lk 1 2"))
o = get_object("3918")
print(o["quotation_text"], o["book"], o["chapter"])
