#!/bin/bash

# This is how the re database have been created.
# You don't have to run this script. It is only here for reference.

exit 1 # Remove this if you want to recreate the re database from scratch.

# 1. Download NT books.
for i in Mt Mk Lk 1Petr Hebr Jud 1Kor 2Kor Joh Gal Acta Eph Röm Jak 1Tim 2Tim; do
 test -r $i.html || wget -O $i.html "https://projekte.isbtf.de/lxx-nt/browser.php?buch=nt_buch&filter=$i"
 done

# 2. Download single entries.
# For this, you need to have a correct cookies.txt file, edit it when needed, first.
for i in `seq 1 30000`; do
 wget --load-cookies=cookies.txt -O $i.html "https://projekte.isbtf.de/lxx-nt/main.php?object_nr=$i"
 done

# 3. Remove files that are not necessary:
grep "bitte melden" *.html | cut -f1 -d: | xargs rm

# 4. Move all HTML downloads in the static file database.
mv *.html ../isbtf-lxx-nt/html-re
