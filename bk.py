# coding: utf-8
import xml.etree.ElementTree as ET
from pathlib import Path
from db import Bookmark, BK, get_bk_titles, db, create_db
import typer
from os import path

file_pref = 'product-preferences.xml' # TODO: change to path
final_tag = '</ide:preferences>\n'

app = typer.Typer()

if not path.exists(db): create_db()

@app.command()
def list() -> None:
    l_bk = get_bk_titles()
    print('id\tname\t\tdescription')
    print('-'*50)
    for i in range(len(l_bk)): print('{id}\t{title}\t{descr}'.format(id=l_bk[i].id, title=l_bk[i].name, descr=l_bk[i].descr))
    print('-'*50)

@app.command()
def load(id: int = None):
    """
    Load chosen BK from DB into preferences
    """
    if not id: 
        bk = get_choose_bk_by_user()
    else:
        bk = BK(tuple([id]))
    save_xml_bk(bk=bk)

@app.command()
def replace(id: int = None):
    """
    Replace bk in DB
    """
    if not id: 
        bk_old = get_choose_bk_by_user()
    else:
        bk_old = BK(tuple([id]))
    bk_new = get_xml_bk(file_pref)
    bk_new.id = bk_old.id
    bk_new.name = bk_old.name
    bk_new.descr = bk_old.descr
    bk_new.save()

@app.command()
def save(title: str = None, descr: str = None):
    """
    Save current BookmarkWorksheet into DB
    """
    bk = get_xml_bk(file_pref)
    if not title:
        bk.name = get_bk_title_by_user()
    else:
        bk.name = title
    if not descr:
        bk.descr = get_bk_descr_by_user().strip()
    else:
        bk.descr = descr
    bk.save()

def change_descr():
    """
    Change description
    """
    bk = get_choose_bk_by_user()
    bk.descr = get_bk_descr_by_user()
    bk.update()

def change_title():
    """
    Change title
    """
    bk = get_choose_bk_by_user()
    bk.descr = get_bk_title_by_user()
    bk.update()

def get_bk_title_by_user() -> str:
    while True:
        x = input("Title: \n")
        if x not in (None, '', '\n'): return x

def get_bk_descr_by_user() -> str:
    while True:
        x = input("Description: \n")
        if x not in (None, '', '\n'): return x

def get_choose_bk_by_user() -> BK:
    l_bk = get_bk_titles()
    print('id\tname\t\tdescription')
    print('-'*50)
    for i in range(len(l_bk)): print('{id}\t{title}\t{descr}'.format(id=l_bk[i].id, title=l_bk[i].name, descr=l_bk[i].descr))
    print('-'*50)
    while True:
        x = int(input("Enter ID: \n"))
        for bk in l_bk:
            if bk.id == x:
                return bk
            else:
                continue

def get_xml_replace(l_pref_lines: list, bk: BK) -> str:
    res_xml = ''
    for line in l_pref_lines:
        if line.find("WorksheetBookmarkOptions") < 0:
            res_xml += line
        else:
            break
    return res_xml + bk.__repr__() + final_tag

def get_xml_bk(file: str) -> BK:
    bk = BK(tuple())
    parser = ET.XMLParser()
    tree = ET.parse(file, parser=parser)
    root = tree.getroot()
    for hhash in root:
        if hhash.attrib['n'] == 'WorksheetBookmarkOptions':
            for hash_list in hhash:
                for hli in hash_list:
                    bkmark = Bookmark(tuple())
                    for bk_hash in hli:
                        if bk_hash.attrib['n'] == 'line': bkmark.line = bk_hash.attrib['v']
                        if bk_hash.attrib['n'] == 'ordinal': bkmark.hotkey = bk_hash.attrib['v']
                        if bk_hash.attrib['n'] == 'url': bkmark.url = bk_hash.attrib['path']
                    bk.bk_list.append(bkmark)
    return bk

def save_xml_bk(bk: BK) -> None:
    l_pref_lines = []
    with open(file_pref, mode = 'r') as f: 
        for line in f.readlines():
            if line.find("WorksheetBookmarkOptions") < 0:
                l_pref_lines.append(line)
            else:
                break
    with open(file=file_pref, mode='w') as f: f.write(get_xml_replace(l_pref_lines=l_pref_lines, bk=bk))

if __name__ == "__main__":
    app()