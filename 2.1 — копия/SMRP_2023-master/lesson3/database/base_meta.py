import sqlalchemy.ext.declarative as dec
import sqlalchemy as sa
import sqlalchemy.orm as orm

Base = dec.declarative_base()


__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        __factory

    if not db_file:
        raise AttributeError("Не задано имя файлы файла базы данных")

    connection_string = f'sqlite:///{db_file}'
    print(f"Подключение к БД: {connection_string}")

    engine = sa.create_engine(connection_string)
    session_maker = orm.sessionmaker(engine, expire_on_commit=False)
    __factory = orm.scoped_session(session_maker)

def create_session():
    return __factory