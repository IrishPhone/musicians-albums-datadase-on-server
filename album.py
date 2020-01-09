import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def album_exists(album):
    """
    Проверяет, есть ли альбом в базе
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.album == album).all()
    return bool(albums)

def append(album_data):
    session = connect_db()
    new_album = Album()
    new_album.year = album_data["year"]
    new_album.artist = album_data["artist"]
    new_album.genre = album_data["genre"]
    new_album.album = album_data["album"]
    session.add(new_album)
    session.commit()

    #return "Альбом добавлен в базу"