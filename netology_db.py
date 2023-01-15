import psycopg2

#conn = psycopg2.connect(database="netology_bd", user="postgres", password="postgres")
#with conn.cursor() as cur:

def create_db(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id_user SERIAL PRIMARY KEY,
            first_name VARCHAR(50) TEXT,
            last_name  VARCHAR(50) TEXT,
            email VARCHAR(40) TEXT
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id_phone SERIAL,
            id_user INTEGER REFERENCES users(id_user)
            phone_number INT NOT NULL
        ); 
    """)
#conn.commit()


def add_user(conn, first_name, last_name, email, phone_number=None):
    cur.execute("""
        INSERT INTO users(first_name, last_name, email) 
        VALUES(%s, %s, %s)
        """, (first_name, last_name, email))
    cur.execute("""
        SELECT id_user FROM users
        ORDER BY id_user DESC
        LIMIT 1
        """)
    id_user = cur.fetchone()[0]
    if phone_number is None:
        return id_user
    else:
        add_number(conn, id_user, phone_number)
        return id_user


def add_number(conn, id_user, phone_number):
    cur.execute("""
        INSERT INTO phones(id_user, phone_number) 
        VALUES(%S, %S)
        """, (id_user, phone_number))
    return id_user


def change_user(conn, id_user, first_name=None, last_name=None, email=None, phone_number=None):
    cur.execute("""
        UPDATE users SET first_name=%s WHERE id=%s; 
    """, (first_name, id_user))
    cur.execute("""
        SELECT * FROM users
        WHERE id=%s
        """, (id, ))

    info = cur.fetchone()
    if first_name is None:
        first_name = info[1]
    if last_name is None:
        last_name = info[2]
    if email is None:
        email = info[3]

    cur.execute("""
        UPDATE phones SET phone_number=%s WHERE id_user=%s
    """, (phone_number))
    cur.execute("""
        SELECT * FROM phones;
    """)
    return phone_number


def delete_phone(conn, phone_number):
    cur.execute("""
        DELETE FROM phones WHERE phone_number=%s;   
        """, (phone_number, ))
    return phone_number


def delete_user(conn, id_user):
    cur.execute("""
        DELETE FROM users WHERE id_user=%s;
        """, (id_user, ))
    cur.execute("""
        DELETE FROM phones WHERE id_user=%s
        """, (id_user, ))
    return id_user

def find_user(conn, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name is None:
        first_name = '%'
    else:
        first_name = '%' + first_name + '%'
    if last_name is None:
        last_name = '%'
    else:
        last_name = '%' + last_name + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone_number is None:
        cur.execute("""
            SELECT u.id_user, u.first_name, u.last_name, u.email, p.phone_number FROM users u
            JOIN phones p ON u.id_user = p.id_user
            WHERE u.fisrt_name LIKE %s AND u.last_name LIKE %s
            AND .uemail LIKE %s
            """, (first_name, last_name, email))
    else:
        cur.execute("""
            SELECT u.id_user, u.first_name, u.last_name, u.email, p.phone_number FROM users u
            JOIN phones p ON c.id_user = p.id_user
            WHERE u.first_name LIKE %s AND u.last_name LIKE %s
            AND u.email LIKE %s AND p.phone_number like %s
            """, (first_name, last_name, email, phone_number))
    return cur.fetchall()


with psycopg2.connect(database="netology_db", user="postgres", password="  ") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        print("База данных создана")

        user1 = add_user(cur, "Ivan", "Ivanov", "ivanmail@com")
        user2 = add_user(cur, "Petr", "Petrov", "petrmail@com")
        user3 = add_user(cur, "Nick", "Nickolaev", "nick@mail.com")
        print("Данные добавлены")
        

