# coding: utf-8
import xml.etree.ElementTree as ET
from db import Bookmark, Collection, BK, get_col_titles, get_bk_titles, create_db, db_close
import typer
from os import path
from sqlite3 import connect

db = 'DB.db'

file_pref = 'C:\\Users\\mholo\\AppData\\Roaming\\SQL Developer\\system23.1.0.097.1607\\o.sqldeveloper\\product-preferences.xml'
final_tag = '</ide:preferences>\n'

app = typer.Typer()

if not path.exists(db): create_db(con=connect(db))
con = connect(db)

@app.command()
def add_bk_to_col(id_bk: int = None, id_col: int = None) -> None:
    if not id_bk:
        bk = get_choose_bk_by_user(con=con)
    else:
        bk = BK(con=con, t=tuple([id_bk]))
    if not id_col:
        c = get_choose_col_by_user(con=con)
    else:
        c = Collection(con=con, t=tuple([id_col]))
    bk.id_col = c.id
    bk.update(con=con)
    db_close(con=con)

@app.command()
def create_col(title: str = None, descr: str = None) -> None:
    c = Collection(con=con, t=tuple([]))
    if not title:
        c.name = get_title_by_user().strip()
    else:
        c.name = title
    if not descr:
        c.descr = get_descr_by_user().strip()
    else:
        c.descr = descr
    c.save(con=con)
    db_close(con=con)

@app.command()
def delete_col(id: int = None) -> None:
    if not id: 
        c = get_choose_col_by_user(con=con)
    else:
        c = Collection(con=con, t=tuple([id]))
    c.delete(con=con)
    db_close(con=con)

@app.command()
def delete_bk(id: int = None) -> None:
    if not id: 
        bk = get_choose_bk_by_user(con=con)
    else:
        bk = BK(con=con, t=tuple([id]))
    bk.delete(con=con)
    db_close(con=con)

@app.command()
def list_col() -> None:
    l_col = get_col_titles(con=con)
    print('id\tname\t\tdescription')
    print('-'*50)
    for i in range(len(l_col)): print('{id}\t{title}\t{descr}'.format(id=l_col[i].id, title=l_col[i].name, descr=l_col[i].descr))
    print('-'*50)
    db_close(con=con)

@app.command()
def list_bk() -> None:
    l_bk = get_bk_titles(con=con)
    print('id\tname\t\tdescription')
    print('-'*50)
    for i in range(len(l_bk)): print('{id}\t{title}\t{descr}'.format(id=l_bk[i].id, title=l_bk[i].name, descr=l_bk[i].descr))
    print('-'*50)
    con.close()

@app.command()
def list_marks(id: int = None):
    if not id: 
        bk = get_choose_bk_by_user(con=con)
    else:
        bk = BK(con=con, t=tuple([id]))
    for mark in bk.bk_list: print(mark, '\n')
    con.close()

@app.command()
def load_bk(id: int = None):
    """
    Load chosen BK from DB into preferences
    """
    if not id: 
        bk = get_choose_bk_by_user(con=con)
    else:
        bk = BK(con=con, t=tuple([id]))
    save_xml_bk(bk=bk)
    con.close()

@app.command()
def load_col(id: int = None):
    """
    Load chosen collection into preferences
    """
    if not id: 
        c = get_choose_col_by_user(con=con)
    else:
        c = Collection(con=con, t=tuple([id]))
    save_xml_col(col=c)
    con.close()

@app.command()
def replace(id: int = None):
    """
    Replace bk in DB
    """
    if not id: 
        bk_old = get_choose_bk_by_user(con=con)
    else:
        bk_old = BK(con=con, t=tuple([id]))
    bk_new = get_xml_bk(file_pref)
    bk_new.id = bk_old.id
    bk_new.name = bk_old.name
    bk_new.descr = bk_old.descr
    bk_new.save(con=con)
    db_close(con=con)

@app.command()
def save_bk(title: str = None, descr: str = None):
    """
    Save current BookmarkWorksheet into DB
    """
    bk = get_xml_bk(file_pref)
    if not title:
        bk.name = get_title_by_user()
    else:
        bk.name = title
    if not descr:
        bk.descr = get_descr_by_user().strip()
    else:
        bk.descr = descr
    bk.save(con=con)
    db_close(con=con)

@app.command()
def update_bk(id: int = None, title: str = None, descr: str = None):
    if not id: 
        bk = get_choose_bk_by_user(con=con)
    else:
        bk = BK(con=con, t=tuple([id]))
    bk.name = title
    bk.descr = descr
    bk.update(con=con)
    db_close(con=con)

@app.command()
def update_bk_marks_descr(id: int = None):
    if not id: 
        bk = get_choose_bk_by_user(con=con)
    else:
        bk = BK(con=con, t=tuple([id]))
    for mark in bk.bk_list:
        print(mark)
        print('-'*50)
        new_descr = input('Enter new description / enter to save current: ')
        mark.descr = new_descr
        mark.update(con=con)
        print('\n')
    db_close(con=con)

@app.command()
def update_bk_mark(id: int):
    mark = Bookmark(con=con, t=tuple([id]))
    mark.change_line(con=con)
    mark.change_hotkey(con=con)
    mark.change_descr(con=con)
    mark.update(con=con)
    db_close(con=con)

##############################################

def change_bk_descr():
    bk = get_choose_bk_by_user(con=con)
    bk.descr = get_descr_by_user()
    bk.update(con=con)
    db_close(con=con)

def change_bk_title():
    bk = get_choose_bk_by_user(con=con)
    bk.descr = get_title_by_user()
    bk.update(con=con)
    db_close(con=con)

def get_title_by_user() -> str:
    while True:
        x = input("Title: ")
        if x not in (None, '', '\n'): return x

def get_descr_by_user() -> str:
    while True:
        x = input("Description: ")
        if x not in (None, '', '\n'): return x

def get_choose_col_by_user() -> BK:
    l_col = get_col_titles(con=con)
    print('id\tname\t\tdescription')
    print('-'*50)
    for i in range(len(l_col)): print('{id}\t{title}\t{descr}'.format(id=l_col[i].id, title=l_col[i].name, descr=l_col[i].descr))
    print('-'*50)
    while True:
        x = int(input("Enter ID: "))
        for col in l_col:
            if col.id == x:
                return col
            else:
                continue

def get_choose_bk_by_user(con: connect) -> BK:
    l_bk = get_bk_titles(con=con)
    print('id\tname\t\tdescription')
    print('-'*50)
    for i in range(len(l_bk)): print('{id}\t{title}\t{descr}'.format(id=l_bk[i].id, title=l_bk[i].name, descr=l_bk[i].descr))
    print('-'*50)
    while True:
        x = int(input("Enter ID: "))
        for bk in l_bk:
            if bk.id == x:
                return bk
            else:
                continue

def get_xml_replace_bk(l_pref_lines: list, bk: BK) -> str:
    res_xml = ''
    for line in l_pref_lines:
        if line.find("WorksheetBookmarkOptions") < 0:
            res_xml += line
        else:
            break
    return res_xml + bk.__repr__() + final_tag

def get_xml_replace_col(l_pref_lines: list, col: Collection) -> str:
    res_xml = ''
    bk_res = BK(con=con, t=tuple([]))
    for line in l_pref_lines:
        if line.find("WorksheetBookmarkOptions") < 0:
            res_xml += line
        else:
            break
    for bk in col.bk_list:
        for mark in bk.mark_list: 
            mark.hotkey = -1
            bk_res.mark_list.append(mark)
    return res_xml + bk_res.__repr__() + final_tag

def get_xml_bk(file: str) -> BK:
    bk = BK(con=con, t=tuple())
    parser = ET.XMLParser()
    tree = ET.parse(file, parser=parser)
    root = tree.getroot()
    for hhash in root:
        if hhash.attrib['n'] == 'WorksheetBookmarkOptions':
            for hash_list in hhash:
                for hli in hash_list:
                    bkmark = Bookmark(con=con, t=tuple())
                    for bk_hash in hli:
                        if bk_hash.attrib['n'] == 'line': bkmark.line = bk_hash.attrib['v']
                        if bk_hash.attrib['n'] == 'ordinal': bkmark.hotkey = bk_hash.attrib['v']
                        if bk_hash.attrib['n'] == 'url': bkmark.url = bk_hash.attrib['path']
                    bk.mark_list.append(bkmark)
    return bk

def save_xml_bk(bk: BK) -> None:
    l_pref_lines = []
    with open(file_pref, mode = 'r', encoding='utf-8') as f: 
        for line in f.readlines():
            if line.find("WorksheetBookmarkOptions") < 0:
                l_pref_lines.append(line)
            else:
                break
    with open(file=file_pref, mode='w', encoding='utf-8') as f: f.write(get_xml_replace_bk(l_pref_lines=l_pref_lines, bk=bk))

def save_xml_col(col: Collection) -> None:
    l_pref_lines = []
    with open(file_pref, mode = 'r', encoding='utf-8') as f: 
        for line in f.readlines():
            if line.find("WorksheetBookmarkOptions") < 0:
                l_pref_lines.append(line)
            else:
                break
    with open(file=file_pref, mode='w', encoding='utf-8') as f: f.write(get_xml_replace_col(l_pref_lines=l_pref_lines, col=col))

if __name__ == "__main__":
    app()