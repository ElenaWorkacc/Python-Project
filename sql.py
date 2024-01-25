import psycopg2 as ps2

connection = ps2.connect(
    database='postgres',
    user='postgres',
    password='1',
    host='localhost',
    port='5432'
)

cursor = connection.cursor()

Q_createRoles = """
CREATE TABLE IF NOT EXISTS "roles" (
id serial NOT NULL PRIMARY KEY,
item varchar(50) NOT NULL
)
"""

Q_insertRoles = """
INSERT INTO roles (item) VALUES
('user'),
('admin');
"""

Q_createUser = """
CREATE TABLE IF NOT EXISTS users (
   id serial NOT NULL PRIMARY KEY,
   lastname varchar(50) NOT NULL,
   firstname varchar(50) NOT NULL,
   patronymic varchar(50) NOT NULL,
   login varchar(50) NOT NULL,
   password varchar(10) NOT NULL,
   "role_id" int NOT NULL DEFAULT 1,
   exist bool NOT NULL,
   
   FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET DEFAULT
)
"""

# Q_insertUser = """
# INSERT INTO users (lastname, firstname, patronymic, login, password) VALUES
# ('Николаев', 'Петр', 'Владимирович', 'samm4el', 48361),
# ('Иванов', 'Сергей', 'Александрович', 'full_dev', 96587),
# ('Захарова', 'Елена', 'Васильевна', 'work_python', 10236),
# ('Гуляев', 'Антон', 'Сергеевич', 'act_md', 35851),
# ('Ширяев', 'Денис', 'Дмитриевич', 'back_dev', 79511);
# """

Q_createPhone = """
CREATE TABLE IF NOT EXISTS phones (
   id serial NOT NULL PRIMARY KEY,
   title varchar(50) NOT NULL,
   count_memory int NOT NULL,
   oper_memory int NOT NULL,
   processor varchar(50) NOT NULL
)
"""

Q_insertPhone = """
INSERT INTO phones (title, count_memory, oper_memory, processor) VALUES
('Samsung Galaxy', '128', '6', 'A16 Bionic'),
('Huavey', '64', '4', 'Snapdragon 8 Gen 2'),
('Nokia', '64', '4', 'Tensor G2'),
('Honor', '256', '8', 'Snapdragon 8 Plus Gen 1'),
('Xiaomi', '512', '12', 'Dimensity 9000 Plus');
"""

Q_updateLastname = """
UPDATE users SET lastname = 'Иванов'
WHERE id = 2
"""

Q_updateRole = """
UPDATE users SET role_id = 2
WHERE id = 1
"""



cursor.execute(Q_updateRole)
connection.commit()
cursor.close()
connection.close()