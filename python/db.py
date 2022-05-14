import sqlite3

database_file = '../db/mercari.sqlite3'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_items():
    return db_exec("SELECT items.id, items.name, category.name, items.image FROM items INNER JOIN category ON items.category = category.id")

def get_new_id(table):
    max_id = db_exec(f"SELECT MAX (id) FROM {table}")
    max_id = max_id[0]['MAX (id)']
    if not max_id:
        max_id = 0
    new_id = max_id + 1
    return new_id

def find_item(value):
    if type(value) is int:
        return db_exec(f"SELECT * FROM items WHERE id = {value}")

    return db_exec(f"SELECT * FROM items WHERE name = '{value}'")

def add_item(name, category, image):
    id = db_exec(f"SELECT * FROM category WHERE name = '{category}'")
    if id:
        id = id[0]['id']
    if not id:
        id = get_new_id("category")
        db_exec(f"INSERT INTO category VALUES ({id}, '{category}')")

    new_id = get_new_id("items")
    db_exec(f"INSERT INTO items VALUES ({new_id}, '{name}', {id}, '{image}')")

def db_exec(instruction):
    conn = sqlite3.connect(database_file)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(instruction)

    ret = c.fetchall()

    conn.commit()
    conn.close()

    return ret
