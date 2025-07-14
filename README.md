# Tools for manipulating the ISBTF LXX-NT database

This project aims at collecting the database entries from ISBTF's LXX-NT
project and saving them as bibref statements. The project is a work in progress.

To run `generate-brst.py`, you need to have the bibref Python module also.
You can find it in https://github.com/kovzol/bibref, folder `py`.

Both Python files require the BeautifulSoup4 Python library. For example,
on Ubuntu Linux systems, you need to have the package `python3-bs4` to have
it provided. See the corresponding GitHub Action for details.

## Status

* 358 entries of the database can be identified.
* 220 of these entries (non-mosaic ones) can be converted into a bibref statement,
  - 15 of them already contained the perfect verbatim OT fragment match,
  - 50 of them were improved on the OT part by using a substring of the given OT verse,
  - 155 of them were improved on the OT part by using a fuzzy substring of the given OT verse.

## Author

This project is maintained by Zoltán Kovács <zoltan@geogebra.org>.
