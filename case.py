import psycopg2


def case1(user_input):
    conn = psycopg2.connect(database="test", user="postgres", password="secret", host="localhost", port="5432")
    cur = conn.cursor()
    # todo
    cur.execute("SELECT * FROM users WHERE username = %s", (user_input,))
