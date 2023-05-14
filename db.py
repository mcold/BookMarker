# coding: utf-8
from sqlite3 import connect

db = 'DB.db'

class Bookmark:
    id = 0
    id_bk = 0
    line = 0
    hotkey = -1
    url = ''
    descr = ''

    def __init__(self, t: tuple):
        if len(t) == 0:
            self.id = None
            self.id_bk = None
            self.line = None
            self.hotkey = None
            self.url = None
            self.descr = None
        else:
            if len(t) == 1:
                self.id = t[0]
                self = self.get_mark()
            else:
                self.id = t[0]
                self.id_bk = t[1]
                self.line = t[2]
                self.hotkey = t[3]
                self.url = t[4]
                self.descr = t[5]
    
    def __repr__(self) -> str:
        res = '         <hash>\n'
        res += '            <value n="line" v="{line}"/>\n'.format(line=self.line)
        res += '            <value n="ordinal" v="{hotkey}"/>\n'.format(hotkey=self.hotkey)
        res += '            <url n="url" path="{url}"/>\n'.format(url=self.url)
        res += '         </hash>\n'
        return res
    
    def __str__(self) -> str:
        return 'id: {id}\nid_bk: {id_bk}\nline: {line}\nhotkey: {hotkey}\nurl: {url}\ndescr: {descr}'.format(id=self.id, id_bk=self.id_bk, line=self.line, hotkey=self.hotkey, url=self.url, descr=self.descr)
    
    def change_descr(self) -> str:
        while True:
            x = input("Description: \n")
            if x not in (None, '', '\n'): self.descr = x

    def change_hotkey(self) -> str:
        while True:
            x = input("Hotkey: \n")
            if x not in (None, '', '\n'): self.hotkey = x

    def change_line(self) -> str:
        while True:
            x = input("Line: \n")
            if x not in (None, '', '\n'): self.line = x

    def get_mark(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                            select id,
                                id_bk,
                                line,
                                hotkey,
                                url,
                                descr
                            from bookmark
                            where id = {id}
                            order by id desc;
                        """.format(id = self.id))
        return Bookmark(cur.fetchone())

    def ins(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                        insert into bookmark(id_bk, line, hotkey, url, descr)
                        values({id_bk}, {line}, {hotkey}, '{url}', '{descr}')
                    """.format(id_bk=self.id_bk, line=self.line, hotkey=self.hotkey, url=self.url, descr=self.descr))
    
    def update(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                        update bookmark
                           set line={line},
                               hotkey={hotkey},
                               url='{url}',
                               descr = '{descr}'
                          where id = {id_mark}
                    """.format(line=self.line, hotkey=self.hotkey, url=self.url, descr=self.descr, id_mark=self.id))
    
    def save(self) -> None:
        self.ins()

class BK:
    id = 0
    name = ''
    descr = ''
    bk_list = list()

    def __init__(self, t: tuple):
        if len(t) == 0:
            self.id = None
            self.name = None
            self.descr = None
            self.bk_list = list()
        else:
            if len(t) == 1:
                self.id = t[0]
                self.get_bk()
                self.bk_list = self.get_bks()
            else:
                self.id = t[0]
                self.name = t[1]
                self.descr = t[2]
                self.bk_list = self.get_bks()
    
    def __repr__(self) -> str:
        res = '   <hash n="WorksheetBookmarkOptions">\n'
        res += '      <list n="persistedWorksheetBookmarks">\n'
        res += ''.join([x.__repr__() for x in self.bk_list])
        res += '      </list>\n'
        res += '   </hash>\n'
        return res

    def get_bk(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                        select name,
                            descr
                        from bk
                        where id = {id};
                    """.format(id=self.id))
        t = cur.fetchone()
        self.name = t[0]
        self.descr = t[1]

    def get_bks(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                            select id,
                                id_bk,
                                line,
                                hotkey,
                                url,
                                descr
                            from bookmark
                            where id_bk = {id_bk}
                            order by id desc;
                        """.format(id_bk = self.id))
        return [Bookmark(result) for result in cur.fetchall()]

    def ins(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                        insert into bk(name, descr)
                        values('{name}', '{descr}')
                    """.format(name=self.name, descr=self.descr))
            cur.execute("""
                        select max(id)
                        from bk;
                    """)
        self.id = cur.fetchone()[0]

    def delete(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                        delete from bk
                        where id = {id_bk}
                    """.format(id_bk=self.id))

    def delete_bkmarks(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                        delete from bookmark
                        where id_bk = {id_bk}
                    """.format(id_bk=self.id))

    def save(self) -> None:
        if self.id not in (None, 0):
            self.delete_bkmarks()
            for bk_mark in self.bk_list: 
                bk_mark.id_bk = self.id
                bk_mark.save()
        else:
            self.ins()
            for bk_mark in self.bk_list: 
                bk_mark.id_bk = self.id
                bk_mark.save()

    def update(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                        update bk
                           set name = '{name}',
                               descr = '{descr}'
                        where id = {id_bk}
                    """.format(name=self.name, descr=self.descr, id_bk=self.id))  


def get_bk_titles(name: str = None, descr: str = None) -> list:
    if name is None: name = ''
    if descr is None: descr = ''
    with connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                    select id,
                           name,
                           descr
                     from bk
                     where lower(name) like lower('%{name}%')
                       and lower(descr) like lower('%{descr}%')
                    order by name asc;
                """.format(name=name, descr=descr))
    return [BK(result) for result in cur.fetchall()]

def get_id_last_bk():
    with connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                    select max(id)
                     from bk;
                """)
    return cur.fetchone()[0]

def create_db():
    with connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                    create table if not exists bk(id    integer primary key autoincrement,
                              name  text,
                              descr text);
                    """)
        cur.execute("""
                    create table if not exists bookmark(id      integer primary key autoincrement,
                                id_bk   integer references bk(id) on delete cascade,
                                line    integer,
                                hotkey  integer,
                                url     text,
                                descr   text);
                    """)

if __name__ == "__main__":
    pass