import sqlite3

# c = conn.cursor()
# c.execute("""CREATE TABLE items(
#     id INT,
#     name TEXT,
#     category TEXT,
#     value JSON
# )
# """)

database_file = '../db/mercari.sqlite3'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_items():
    return db_exec("SELECT * FROM items")

def get_new_id():
    max_id = db_exec("SELECT MAX (id) FROM items")
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
    new_id = get_new_id()
    db_exec(f"INSERT INTO items VALUES ({new_id}, '{name}', '{category}', '{image}')")


def db_exec(instruction):
    conn = sqlite3.connect(database_file)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(instruction)

    ret = c.fetchall()

    conn.commit()
    conn.close()

    return ret
