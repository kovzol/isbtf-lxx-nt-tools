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
    match = None
    for m in q:
        if f_container[1] <= m[1] and m[2] <= f_container[2]:
            match = m
            break
    if match == None:
        raise Exception(f'Cannot identify "{o["quotation_text"]}" ~ {o["book"]} {o["chapter"]}:{o["verse_start"]} {o["chapter"]}:{o["verse_end"]}')
    ret["q_fullform"] = f'{match[0]} ({match[1]}-{match[2]}, length {match[2]-match[1]+1})'
    ret["q_verseonly"] = ret["q_fullform"].split(' ', 1)[1]
    ret["q_azform"] = qlatin
    ret["q_greek"] = o["quotation_text"]

    # Search for exact position of the intro text in gnt:
    bibref_passage_container = f'{o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]} {o["intro_chapter"]}:{o["intro_verse_end"]}'
    l_container = lookup_n(1, gnt + " " + bibref_passage_container)
    f_container = find_n(1, gnt)[0] # TODO: This may be a longer list, fix this issue.
    qlatin = text_n(2, o["intro_text"])
    q = find_n(2, gnt)
    match = None
    for m in q:
        if f_container[1] <= m[1] and m[2] <= f_container[2]:
            match = m
            break
    if match == None:
        raise Exception(f'Cannot identify "{o["intro_text"]}" ~ {o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]} {o["intro_chapter"]}:{o["intro_verse_end"]}')
    ret["i_fullform"] = f'{match[0]} ({match[1]}-{match[2]}, length {match[2]-match[1]+1})'
    ret["i_verseonly"] = ret["i_fullform"].split(' ', 1)[1]
    ret["i_azform"] = qlatin
    ret["i_greek"] = o["intro_text"]
    return ret

def object_ot_bibref(o):
    """
    Extract data from OT object in bibref format.
    :param o: input object
    :return: various parts of the object as dict
    """
    ret = dict()
    # Search for exact position of the quotation text in gnt:
    bibref_passage_container = f'{o["book"]} {o["chapter"]}:{o["verse_start"]}'
    l_container = lookup_n(1, "LXX" + " " + bibref_passage_container)
    f_container = find_n(1, "LXX")[0] # TODO: This may be a longer list, fix this issue.
    qlatin = text_n(2, o["quoted_text"])
    q = find_n(2, "LXX")
    ret["unique"] = (len(q) == 1)
    match = None
    for m in q:
        if f_container[1] <= m[1] and m[2] <= f_container[2]:
            match = m
            break
    if match == None:
        raise Exception(f'Cannot identify "{o["quoted_text"]}" ~ {o["book"]} {o["chapter"]}:{o["verse_start"]}')
    ret["q_fullform"] = f'{match[0]} ({match[1]}-{match[2]}, length {match[2]-match[1]+1})'
    ret["q_verseonly"] = ret["q_fullform"].split(' ', 1)[1]
    ret["q_azform"] = qlatin
    ret["q_greek"] = o["quoted_text"]
    return ret


# print(passage_str_list("Lk 1 2"))
# o = get_object("3918")
# print(object_nt_bibref(o))

# print(f'{o["quotation_text"]}: {o["book"]} {o["chapter"]}:{o["verse_start"]}-{o["verse_end"]}')
# print(f'{o["intro_text"]}: {o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]}-{o["intro_verse_end"]}')

# print(getrefs_maxlength("SBLGNT LXX Psalms 2"))
# print(text_n(1, o["quotation_text"]))
# print(find_n(1, "LXX"))
# print(find_n(1, "SBLGNT"))

# print(text_n(2, o["intro_text"]))
# print(find_n(2, "SBLGNT"))

# o = get_object("845")
# print(o)

# print(extract_nt_objects("Acta"))

def object_nt_brst(nt_obj):
    ret = ""
    identifier = passage_str_list(nt_obj[0])
    identifier = f"{identifier[0]}-{identifier[1]},{identifier[2]}"
    ret += f"Statement {identifier} connects\n"
    if len(nt_obj) == 2: # simple case: one-to-one correspondence
        print(nt_obj[1][0])
        br_obj_nt = object_nt_bibref(get_object(nt_obj[1][0][0]))
        ret += f' {gnt} {br_obj_nt["q_fullform"]} with\n'
        br_obj_ot = object_ot_bibref(get_object(nt_obj[1][0][1]))
        ret += f' LXX {br_obj_ot["q_fullform"]} based on\n'
        ret += f'  introduction {br_obj_nt["i_verseonly"]} a-z form {br_obj_nt["i_azform"]} moreover\n'
        ret += f'  fragment {br_obj_nt["q_verseonly"]} a-z form {br_obj_nt["q_azform"]}\n'
        ret += f'   matches LXX {br_obj_ot["q_fullform"]} a-z form {br_obj_ot["q_azform"]}\n'
        if br_obj_ot["unique"]:
            ret += '    unique in Old Testament\n'
        distance = jaccard(br_obj_nt["q_greek"], br_obj_ot["q_greek"])
        if distance == 0:
            ret += '    verbatim\n'
        else:
            ret += f"    differing by {distance:4.2f}%\n"
        ret += '  providing an overall cover of 100.00%.\n'
        return ret
    return None

max_processing = 500
count = 0
for ntb in nt_books_isbtf:
    nt_objects = extract_nt_objects(ntb)
    print(f"{ntb} contains {len(nt_objects)} entries.")
    for nt_obj in nt_objects:
        try:
            processed = object_nt_brst(nt_obj)
            if processed != None and len(processed) > 2: # FIXME
                filename = (processed.split(" "))[1] + ".brst"
                # print(filename, processed)
                with open(filename, "w") as f:
                    f.write(processed)
                count += 1
        except Exception as inst:
            print(inst)
        if count >= max_processing:
            break
    if count >= max_processing:
        break
print(f"{count} entries processed")

# o = get_object("3797")
# print(o)
# print(object_nt_bibref(o))
# 
# o = get_object("329")
# print(o)
# print(object_ot_bibref(o))
# 
# o = get_object("4987")
# print(o)
# print(object_nt_bibref(o))
# 
# o = get_object("333")
# print(o)
# print(object_ot_bibref(o))
