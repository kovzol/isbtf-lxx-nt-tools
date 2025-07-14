#!/usr/bin/python3

# This script creates an ad-hoc BRST file database, based on ISBTF's LXX_NT online archive.

# NT Bible texts will be based on the SWORD library, module SBLGNT:
gnt = "SBLGNT" # Alternatively, you can change this to StatResGNT.
# The folder to be generated with the BRST output:
generated_folder = "generated-brst"
# Stop after processing so many entries:
max_processing = 500
# If the bibref utility is installed, set it here explicitly. Otherwise comment this line
# and the bibref module will try to find a development version (currently under ../..).
from bibref.tools import *
set_bibref_path("bibref")

from isbtf_lxx_nt.tools import *
import os

def object_nt_bibref(o):
    """
    Extract data from NT object in bibref format.
    :param o: input object
    :return: various parts of the object as dict
    """
    ret = dict()
    o["quotation_text"] = ' '.join(o['quotation_text'].split()) # simplify whitespaces by single space
    # Search for exact position of the quotation text in gnt:
    bibref_passage_container = f'{o["book"]} {o["chapter"]}:{o["verse_start"]} {o["chapter"]}:{o["verse_end"]}'
    l_container = lookup_n(1, gnt + " " + bibref_passage_container)
    f_containers = find_n(1, gnt)
    match = None
    for container in f_containers:
        c_book = (container[0].split(" "))[0]
        if o["book"] == c_book:
            match = container # we assume that there is only one match per book, TODO: maybe check chapter also
            break
    if match == None:
        raise Exception(f'Cannot find {bibref_passage_container}')
    qlatin = text_n(2, o["quotation_text"])
    q = find_n(2, gnt)
    match = None
    for m in q:
        m_book = (m[0].split(" "))[0]
        if o["book"] == m_book and ((container[1] <= m[1] and m[1] <= container[2]) or (container[1] <= m[2] and m[2] <= container[2])):
            match = m
            break
    if match == None:
        # No exact match. Let's try a fuzzy-substring match:
        nt_verse = lookup_n(1, gnt + " " + container[0])
        best, qlatin_fuzzy = nearest12()
        print(f"Nearest fuzzy substring found: {qlatin} ~ {qlatin_fuzzy}: {best:.2f}%")
        latintext_n(2, qlatin_fuzzy)
        q = find_n(2, gnt)
        for m in q:
            m_book = (m[0].split(" "))[0]
            if o["book"] == m_book and ((container[1] <= m[1] and m[1] <= container[2]) or (container[1] <= m[2] and m[2] <= container[2])):
                match = m
                qlatin = qlatin_fuzzy
                o["quotation_text"] = latin_to_greek(qlatin)
            break
        if match == None:
            raise Exception(f'Quotation: Cannot identify "{o["quotation_text"]}" ~ {o["book"]} {o["chapter"]}:{o["verse_start"]} {o["chapter"]}:{o["verse_end"]}')
    ret["q_fullform"] = f'{match[0]} ({match[1]}-{match[2]}, length {match[2]-match[1]+1})'
    ret["q_verseonly"] = ret["q_fullform"].split(' ', 1)[1]
    ret["q_azform"] = qlatin
    ret["q_greek"] = o["quotation_text"]

    # Search for exact position of the intro text in gnt:
    if "intro_book" in o.keys() and "intro_text" in o.keys():
        bibref_passage_container = f'{o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]} {o["intro_chapter"]}:{o["intro_verse_end"]}'
        l_container = lookup_n(1, gnt + " " + bibref_passage_container)
        f_container = find_n(1, gnt)[0] # TODO: This may be a longer list, fix this issue.
        qlatin = text_n(2, o["intro_text"])
        q = find_n(2, gnt)
        match = None
        for m in q:
            m_book = (m[0].split(" "))[0]
            if o["intro_book"] == m_book and ((f_container[1] <= m[1] and m[1] <= f_container[2]) or (f_container[1] <= m[2] and m[2] <= f_container[2])):
                match = m
                break
        if match == None:
            raise Exception(f'Intro: Cannot identify "{o["intro_text"]}" ~ {o["intro_book"]} {o["intro_chapter"]}:{o["intro_verse_start"]} {o["intro_chapter"]}:{o["intro_verse_end"]}')
        ret["i_fullform"] = f'{match[0]} ({match[1]}-{match[2]}, length {match[2]-match[1]+1})'
        ret["i_verseonly"] = ret["i_fullform"].split(' ', 1)[1]
        ret["i_azform"] = qlatin
        ret["i_greek"] = o["intro_text"]
        ret["with_intro"] = True
    else:
        ret["with_intro"] = False
    ret["marked_quotation"] = o["marked_quotation"]
    return ret

def object_ot_bibref(o, quotation_greek = ""):
    """
    Extract data from OT object in bibref format.
    If quotation is given (provided from the NT entry), a refining of the output passage is expected.
    :param o: input object
    :return: various parts of the object as dict
    """
    ret = dict()
    # Search for exact position of the quotation text in LXX:
    bibref_passage_container = f'{o["book"]} {o["chapter"]}:{o["verse_start"]}'
    l_container = lookup_n(1, "LXX" + " " + bibref_passage_container)
    f_container = find_n(1, "LXX")[0] # TODO: This may be a longer list, fix this issue.
    qlatin = text_n(2, o["quoted_text"])

    if quotation_greek != "": # try to improve the output
        # We assume that the NT quotation is exactly identified by the ISBTF project, so we only have to
        # find the best matching OT text inside o["quoted_text"] (qlatin).
        # This requires only O(N^2) jaccard-comparisons where N is the length of qlatin.
        # Unfortunately, this is still too much, but a dynamic variant of the concept works well.
        # 1. Special case: if quotation is a substring of quoted text.
        quotation_azform = text_n(1, quotation_greek)
        p = qlatin.find(quotation_azform)
        if p != -1:
            o["quoted_text"] = quotation_greek
            print(f"Substring found: {quotation_azform} in {qlatin}")
            qlatin = quotation_azform
            text_n(2, quotation_greek) # continuing with this
            ret["auto_change"] = "substring"
        else:
            # 2. General case:
            latintext_n(1, qlatin)
            latintext_n(2, quotation_azform)
            best, qlatin = nearest12() # use the dynamic variant
            print(f"Nearest fuzzy substring found: {quotation_azform} ~ {qlatin}: {best:.2f}%")
            o["quoted_text"] = latin_to_greek(qlatin)
            text_n(2, o["quoted_text"])
            ret["auto_change"] = "substring_fuzzy"

    q = find_n(2, "LXX")
    ret["unique"] = (len(q) == 1)
    match = None
    for m in q:
        m_book = (m[0].split(" "))[0]
        if o["book"] == m_book and ((f_container[1] <= m[1] and m[1] <= f_container[2]) or (f_container[1] <= m[2] and m[2] <= f_container[2])):
            match = m
            break
    if match == None:
        raise Exception(f'Quoted text: Cannot identify "{o["quoted_text"]}" ~ {o["book"]} {o["chapter"]}:{o["verse_start"]}')
    ret["q_fullform"] = f'{match[0]} ({match[1]}-{match[2]}, length {match[2]-match[1]+1})'
    ret["q_verseonly"] = ret["q_fullform"].split(' ', 1)[1]
    ret["q_azform"] = qlatin
    ret["q_greek"] = o["quoted_text"]
    return ret

def object_nt_brst(nt_obj):
    ret_obj = dict()
    ret = ""
    identifier = passage_str_list(nt_obj[0])
    identifier = f"{identifier[0]}-{identifier[1]},{identifier[2]}"
    ret += f"Statement {identifier} connects\n"
    if len(nt_obj[1]) == 1: # simple case: one-to-one correspondence
        br_obj_nt = object_nt_bibref(get_object(nt_obj[1][0][0]))
#        if not br_obj_nt["marked_quotation"] or not br_obj_nt["with_intro"]:
        if not br_obj_nt["with_intro"]:
            # non-marked quotations are currently not handled
            return None
        ret += f' {gnt} {br_obj_nt["q_fullform"]} with\n'
        br_obj_ot = object_ot_bibref(get_object(nt_obj[1][0][1]), br_obj_nt["q_greek"])
        if "auto_change" in br_obj_ot.keys():
            ret_obj["auto_change"] = br_obj_ot["auto_change"]
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
        ret_obj["statement"] = ret
        return ret_obj
    return None

# Main loop...
if not os.path.exists(generated_folder):
    os.makedirs(generated_folder)

allcases = 0
count = 0
substring_type = 0
substring_fuzzy_type = 0

maxresults(100000)

for ntb in nt_books_isbtf:
# for ntb in ["Acta"]: # Use this to restrict run to certain books.
    nt_objects = extract_nt_objects(ntb)
    allcases += len(nt_objects)
    print(f"{ntb} contains {len(nt_objects)} entries.")
    for nt_obj in nt_objects:
        try:
            processed = object_nt_brst(nt_obj)
            if processed != None:
                statement = processed["statement"]
                filename = (statement.split(" "))[1] + ".brst"
                with open(generated_folder + "/" + filename, "w") as f:
                    f.write(statement)
                count += 1
                if "auto_change" in processed.keys():
                    if processed["auto_change"] == "substring":
                        substring_type += 1
                    if processed["auto_change"] == "substring_fuzzy":
                        substring_fuzzy_type += 1
        except KeyError:
            print(f"There is a fatal error when processing {nt_obj}:")
            raise
        except Exception as inst:
            print(f"There is a skippable error when processing {nt_obj}:")
            print(inst)
        if count >= max_processing:
            break
    if count >= max_processing:
        break
print(f"{count} of {allcases} entries have been processed.")
print(f"OT fragments were: {substring_type} substring type, {substring_fuzzy_type} substring-fuzzy type.")
