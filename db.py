# coding: utf-8
from sqlite3 import connect

class Collection:
    id = None
    name = None
    descr = None

    def __init__(self, con: connect, t: tuple):
        if len(t) == 0:
            self.id = None
            self.name = None
            self.descr = None
            self.bk_list = list()
        else:
            if len(t) == 1:
                self.id = t[0]
                self.get_col(con=con)
                self.bk_list = self.get_bks(con=con)
            else:
                self.id = t[0]
                self.name = t[1]
                self.descr = t[2]
                self.bk_list = self.get_bks(con=con)

    def __str__(self) -> str:
        return 'id: {id}\nname: {name}\ndescr: {descr}'.format(id=self.id, name=self.name, descr=self.descr)

    def delete(self, con: connect) -> None:
        cur = con.cursor()
        for bk in self.bk_list: bk.unset_col(con=con)
        cur.execute("""
                    delete from collection
                    where id = {id_col}
                """.format(id_col=self.id))
        

    def delete_bks(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    delete from bk
                    where id_col = {id_col}
                """.format(id_col=self.id))

    def get_col(self, con: connect):
        cur = con.cursor()
        cur.execute("""
                    select name,
                            descr
                    from collection
                    where id = {id};
                """.format(id=self.id))
        t = cur.fetchone()
        self.name = t[0]
        self.descr = t[1]

    def ins(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    insert into collection(name, descr)
                    values('{name}', '{descr}')
                """.format(name=self.name, descr=self.descr))
        cur.execute("""
                    select max(id)
                    from collection;
                """)
        self.id = cur.fetchone()[0]

    def save(self, con: connect) -> None:
        if self.id not in (None, 0):
            self.delete_bks()
            for bk in self.bk_list: 
                bk.id_col = self.id
                bk.save()
        else:
            self.ins(con=con)
            for bk in self.bk_list: 
                bk.id_col = self.id

    def get_bks(self, con: connect):
        cur = con.cursor()
        cur.execute("""
                        select id,
                            id_col,
                            name,
                            descr
                        from bk
                        where id_col = {id_col}
                        order by id desc;
                    """.format(id_col = self.id))
        return [BK(con=con,t=result) for result in cur.fetchall()]

class BK:
    id = None
    id_col = None
    name = None
    descr = None
    mark_list = list()

    def __init__(self, con: connect, t: tuple):
        if len(t) == 0:
            self.id = None
            self.id_col = None
            self.name = None
            self.descr = None
            self.mark_list = list()
        else:
            if len(t) == 1:
                self.id = t[0]
                self.get_bk(con=con)
                self.mark_list = self.get_marks(con=con)
            else:
                self.id = t[0]
                self.id_col = t[1]
                self.name = t[2]
                self.descr = t[3]
                self.mark_list = self.get_marks(con=con)
    
    def __repr__(self) -> str:
        res = '   <hash n="WorksheetBookmarkOptions">\n'
        res += '      <list n="persistedWorksheetBookmarks">\n'
        res += ''.join([x.__repr__() for x in self.mark_list])
        res += '      </list>\n'
        res += '   </hash>\n'
        return res
    
    def __str__(self) -> str:
        return '\n'.join([x.__str__() for x in self.mark_list])

    def get_bk(self, con: connect):
        cur = con.cursor()
        cur.execute("""
                    select id_col,
                            name,
                            descr
                        from bk
                        where id = {id};
                """.format(id=self.id))
        t = cur.fetchone()
        self.id_col = t[0]
        self.name = t[1]
        self.descr = t[2]

    def get_marks(self, con: connect):
        cur = con.cursor()
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
        return [Bookmark(con=con,t=result) for result in cur.fetchall()]

    def ins(self, con: connect) -> None:
        cur = con.cursor()
        if self.id_col:
            cur.execute("""
                        insert into bk(id_col, name, descr)
                        values({id_col}, '{name}', '{descr}')
                    """.format(id_col=self.id_col, name=self.name, descr=self.descr))
        else:
            cur.execute("""
                        insert into bk(name, descr)
                        values('{name}', '{descr}')
                    """.format(name=self.name, descr=self.descr))                        
        cur.execute("""
                    select max(id)
                    from bk;
                """)
        self.id = cur.fetchone()[0]

    def delete(self, con: connect) -> None:
        # for mark in self.mark_list: mark.unset_bk(con=con) # TODO: check deletion
        cur = con.cursor()
        cur.execute("""
                    delete from bk
                    where id = {id_bk}
                """.format(id_bk=self.id))

    def delete_bkmarks(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    delete from bookmark
                    where id_bk = {id_bk}
                """.format(id_bk=self.id))

    def save(self, con: connect) -> None:
        if self.id not in (None, 0):
            self.delete_bkmarks(con=con)
            for bk_mark in self.mark_list: 
                bk_mark.id_bk = self.id
                bk_mark.save(con=con)
        else:
            self.ins(con=con)
            for bk_mark in self.mark_list: 
                bk_mark.id_bk = self.id
                bk_mark.save(con=con)

    def unset_col(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    update bk
                        set id_col = null
                    where id = {id_bk}
                """.format(id_bk=self.id))

    def update(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    update bk
                        set id_col = '{id_col}',
                            name = '{name}',
                            descr = '{descr}'
                    where id = {id_bk}
                """.format(id_col=self.id_col, name=self.name, descr=self.descr, id_bk=self.id))

class Bookmark:
    id = None
    id_bk = None
    line = None
    hotkey = None
    url = None
    descr = None

    def __init__(self, con: connect, t: tuple):
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
                self = self.get_mark(con=con)
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
        return 'id: {id}\nid_bk: {id_bk}\nline: {line}\nhotkey: {hotkey}\nurl: {url}\ndescr: {descr}\n'.format(id=self.id, id_bk=self.id_bk, line=self.line, hotkey=self.hotkey, url=self.url, descr=self.descr)
    
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

    def get_mark(self, con: connect) -> None:
        cur = con.cursor()
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

    def ins(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    insert into bookmark(id_bk, line, hotkey, url, descr)
                    values({id_bk}, {line}, {hotkey}, '{url}', '{descr}')
                """.format(id_bk=self.id_bk, line=self.line, hotkey=self.hotkey, url=self.url, descr=self.descr))

    def unset_bk(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    update bookmark
                        set id_bk = null
                    where id = {id_mark}
                """.format(id_mark=self.id))

    def update(self, con: connect) -> None:
        cur = con.cursor()
        cur.execute("""
                    update bookmark
                        set line={line},
                            hotkey={hotkey},
                            url='{url}',
                            descr = '{descr}'
                        where id = {id_mark}
                """.format(line=self.line, hotkey=self.hotkey, url=self.url, descr=self.descr, id_mark=self.id))

    def save(self, con: connect) -> None:
        self.ins(con=con)


def get_col_titles(con: connect, name: str = None, descr: str = None) -> list:
    if name is None: name = ''
    if descr is None: descr = ''
    cur = con.cursor()
    cur.execute("""
                select id,
                        name,
                        descr
                    from collection
                    where lower(name) like lower('%{name}%')
                    and lower(descr) like lower('%{descr}%')
                order by name asc;
            """.format(name=name, descr=descr))
    return [Collection(con=con,t=result) for result in cur.fetchall()]

def get_bk_titles(con: connect, name: str = None, descr: str = None) -> list:
    if name is None: name = ''
    if descr is None: descr = ''
    cur = con.cursor()
    cur.execute("""
                select id,
                        id_col,
                        name,
                        descr
                    from bk
                    where lower(name) like lower('%{name}%')
                    and lower(descr) like lower('%{descr}%')
                order by name asc;
            """.format(name=name, descr=descr))
    return [BK(con=con,t=result) for result in cur.fetchall()]

def get_id_last_col(con: connect):
    cur = con.cursor()
    cur.execute("""
                select max(id)
                    from collection;
            """)
    return cur.fetchone()[0]

def get_id_last_bk(con: connect):
    cur = con.cursor()
    cur.execute("""
                select max(id)
                    from bk;
            """)
    return cur.fetchone()[0]

def create_db(con: connect) -> None:
    cur = con.cursor()
    cur.execute("""
                create table if not exists collection(id    integer primary key autoincrement,
                                                        name  text,
                                                        descr text);
                """)
    cur.execute("""
                create table if not exists bk(id     integer primary key autoincrement,
                                                id_col integer references collection(id) on delete cascade,
                                                name   text,
                                                descr  text);
                """)
    cur.execute("""
                create table if not exists bookmark(id      integer primary key autoincrement,
                                                    id_bk   integer references bk(id) on delete cascade,
                                                    line    integer,
                                                    hotkey  integer,
                                                    url     text,
                                                    descr   text);
                """)

def db_close(con: connect) -> None:
    con.commit()
    con.close()

if __name__ == "__main__":
    pass