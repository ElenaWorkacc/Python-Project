import sys

import psycopg2 as ps2

connection = ps2.connect(
    database='postgres',
    user='postgres',
    password='1',
    host='localhost',
    port='5432'
)

class User:
    def __init__(self, id, lastname, firstname, patronymic, login, password, role_id, exist):
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.patronymic = patronymic
        self.login = login
        self.password = password
        self.role_id = role_id
        self.exist = exist

class Phone:
    def __init__(self, id, title, count_memory, oper_memory, processor):
        self.id = id
        self.title = title
        self.count_memory = count_memory
        self.oper_memory = oper_memory
        self.processor = processor

class UserModule:
    def __init__(self, connection):
        self.connection = connection
        self.cur = connection.cursor()

        # Получить пользователя по логину и паролю

    def get_user_by_credentials(self, login, password):
        self.cur.execute("SELECT * FROM Users WHERE login=%s AND password=%s AND exist=true", (login, password))
        record = self.cur.fetchone()

        if record is None:
            return None

        return User(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7])

        # Получить всех пользователей

    def get_all_users(self):
        self.cur.execute("SELECT * FROM Users WHERE exist=true")
        records = self.cur.fetchall()

        return [User(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]) for record in records]

        # Добавить нового пользователя

    def add_user(self, lastname, firstname, patronymic, login, password, role_id="1"):
        self.cur.execute("INSERT INTO Users (lastname, firstname, patronymic, login, password, role_id, exist) "
                         "VALUES (%s, %s, %s, %s, %s, %s, true)",
                         (lastname, firstname, patronymic, login, password, role_id))
        self.connection.commit()

        # Удалить пользователя по id

    def delete_user(self, id):
        self.cur.execute("UPDATE Users SET exist=false WHERE id=%s", (id,))
        self.connection.commit()

        # Сменить роль пользователя по id

    def change_user_role(self, id, new_role):
        self.cur.execute("UPDATE Users SET role_id=%s WHERE id=%s AND exist=true", (new_role, id))
        self.connection.commit()

class PhoneModule:
    def __init__(self, connection):
        self.connection = connection
        self.cur = connection.cursor()

    # Получить один телефон

    def get_phone(self):
        phone_title = input("Введите название телефона, который хотите купить: ")
        phone_count_memory = int(input("Введите объем памяти, который вам необходим: "))
        self.cur.execute("SELECT title, count_memory FROM Phones WHERE title=%s AND count_memory=%s",
                         (phone_title, phone_count_memory))
        phone = self.cur.fetchone()
        return phone

    # Получить все телефоны
    def get_all_phones(self):
        self.cur.execute("SELECT * FROM Phones")
        records = self.cur.fetchall()

        return [Phone(record[0], record[1], record[2], record[3], record[4]) for record in records]

    # Добавить новый телефон
    def add_phone(self, title, count_memory, oper_memory, processor):
        self.cur.execute("INSERT INTO Phones (title, count_memory, oper_memory, processor) VALUES (%s, %s, %s, %s)",
                         (title, count_memory, oper_memory, processor))
        self.connection.commit()

    # Покупки или отказ от нее
    def get_answer(self):
        answer = input("Хотите купить? Введите Да или Нет: ")

        if answer == "Да":
            phone = phone_module.get_phone()
            if phone:
                print(f"Поздравляю с успешной покупкой {phone[1]} ГБ")
            else:
                print("Такого телефона не существует")
        else:
            print(f"Будем рады видеть вас снова")

    # Удалить телефон по id
    def delete_phone(self, id):
        self.cur.execute("DELETE FROM Phones WHERE id=%s", (id,))
        self.connection.commit()

# Функция для вывода меню и обработки выбора пользователя
def main_menu():
    print("1. Авторизация")
    print("2. Регистрация")
    print("3. Выйти из приложения")

    choice = input("Введите номер действия: ")

    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        sys.exit()
    else:
        print("Некорректный выбор")

# Функция для обработки авторизации пользователя
def login():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    user = user_module.get_user_by_credentials(login, password)

    if user is None:
        print("Неверный логин или пароль")
        main_menu()
    elif user.role_id == 1:
        show_phones()
    elif user.role_id == 2:
        admin_menu(user)
    else:
        print("Неверный логин или пароль")
        main_menu()

# Функция для обработки регистрации нового пользователя
def register():
    lastname = input("Введите Фамилию: ")
    firstname = input("Введите Имя: ")
    patronymic = input("Введите Отчество: ")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    user_module.add_user(lastname, firstname, patronymic, login, password)

    print("Пользователь успешно зарегистрирован")
    main_menu()

# Функция для вывода списка телефонов
def show_phones():
    phones = phone_module.get_all_phones()

    if len(phones) == 0:
        print("Телефоны не найдены")
        main_menu()
    else:
        for phone in phones:
            print(f"{phone.title} ({phone.count_memory} ГБ памяти, {phone.oper_memory} ГБ ОЗУ, {phone.processor})")

        phone_module.get_answer()

# Функция для вывода меню администратора и обработки выбора пользователя
def admin_menu(admin):
    print("1. Добавить телефон")
    print("2. Удалить телефон")
    print("3. Просмотреть информацию о пользователях")
    print("4. Сменить роль пользователю")
    print("5. Выйти")

    choice = input("Введите номер действия: ")

    if choice == "1":
        add_phone(admin)
    elif choice == "2":
        delete_phone(id)
    elif choice == "3":
        show_users(admin)
    elif choice == "4":
        change_user_role(admin)
    elif choice == "5":
        main_menu()
    else:
        print("Некорректный ввод, попробуйте еще раз.")
        admin_menu(admin)

# Функция для обработки добавления нового телефона
def add_phone(admin):
    title = input("Введите название телефона: ")
    count_memory = input("Введите кол-во памяти (в ГБ): ")
    oper_memory = int(input("Введите кол-во оперативной памяти (в ГБ): "))
    processor = input("Введите тип процессора: ")

    phone_module.add_phone(title, count_memory, oper_memory, processor)

    print("Телефон успешно добавлен в базу данных")
    admin_menu(admin)


# Функция для обработки удаления телефона по id
def delete_phone(admin):
    id = int(input("Введите ID телефона: "))
    phone_module.delete_phone(id)
    print("Телефон успешно удален из базы данных")
    admin_menu(admin)


# Функция для вывода списка пользователей
def show_users(admin):
    if admin.role_id != 2:
        print("Недостаточно прав для выполнения операции")
        admin_menu(admin)

    users = user_module.get_all_users()

    if len(users) == 0:
        print("Пользователи не найдены")
        admin_menu(admin)
    else:
        for user in users:
            print(f"{user.id}. {user.lastname} {user.firstname} {user.patronymic} ({user.login}, {user.role_id})")

    get_action(admin)

# Функция для выбора действия админом после вывода списка пользоватей
def get_action(admin):
    action = input("Желаете продолжить? Да или Нет: ")
    if action == "Да":
        admin_menu(admin)
    else:
        print(f"Благодарю за выбор нашего приложения")

# Функция для обработки смены роли пользователю по id
def change_user_role(admin):
    if admin.role_id != 2:
        print("Недостаточно прав для выполнения операции")
        admin_menu(admin)

    user_id = int(input("Введите ID пользователя: "))
    new_role = int(input("Введите новую роль пользователя: "))

    user_module.change_user_role(user_id, new_role)

    print("Роль пользователя успешно изменена")
    admin_menu(admin)

# Создание объектов для работы с модулями базы данных
user_module = UserModule(connection)
phone_module = PhoneModule(connection)

# Вывод главного меню
main_menu()