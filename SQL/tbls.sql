create table if not exists collection(id    integer primary key autoincrement,
                                      name  text,
                                      descr text);

create table if not exists bk(id     integer primary key autoincrement,
                              id_col integer references collection(id) on delete cascade,
                              name   text,
                              descr  text);

create table if not exists bookmark(id      integer primary key autoincrement,
                                    id_bk   integer references bk(id) on delete cascade,
                                    line    integer,
                                    hotkey  integer,
                                    url     text,
                                    descr   text);