import psycopg2


def case1(user_input):
    conn = psycopg2.connect(database="test", user="postgres", password="secret", host="localhost", port="5432")
    cur = conn.cursor()
    # todo
    cur.execute("SELECT * FROM users WHERE username = %s", (user_input,))


def some_function():
    # 未使用的变量
    unused_variable = 10
    # 可能的 SQL 注入风险
    user_input = "some_user_input"
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    # 硬编码密码
    password = "password1234"
    # 复杂度过高的函数
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)
    # 未处理的异常
    try:
        result = 1 / 0
    except ZeroDivisionError:
        pass
    # 缺少文档字符串
    def inner_function():
        pass
    # 未使用的函数
    def another_unused_function():
        print("This function is not used")
    # 可能的资源泄漏
    file = open("example.txt", "r")
    content = file.read()
    # 未关闭文件资源

def some_function2():
    # 未使用的变量
    unused_variable = 10
    # 可能的 SQL 注入风险
    user_input = "some_user_input"
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    # 硬编码密码
    password = "password1234"
    # 复杂度过高的函数
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)
    # 未处理的异常
    try:
        result = 1 / 0
    except ZeroDivisionError:
        pass
    # 缺少文档字符串
    def inner_function():
        pass
    # 未使用的函数
    def another_unused_function():
        print("This function is not used")
    # 可能的资源泄漏
    file = open("example.txt", "r")
    content = file.read()


if __name__ == "__main__":
    some_function()
