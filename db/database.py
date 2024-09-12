import os
import psycopg2

from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, URL, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from db.meta import metadata, Article, Author, Hab
from habr_parser import get_info, print_info

load_dotenv()

username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database_name = os.getenv('DB_NAME')
db_url = URL.create('postgresql+psycopg2',
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                    database=database_name
                    )
async_db_url = URL.create('postgresql+asyncpg',
                          username=username,
                          password=password,
                          host=host,
                          port=port,
                          database=database_name
                          )

engine = create_engine(db_url, echo=True, pool_size=10)
async_engine = create_async_engine(async_db_url, echo=True, pool_size=10)

session = sessionmaker(engine)
async_session = async_sessionmaker(async_engine)


def create_db(db_name='habrs'):
    """
    Создание БД
    """
    connection = psycopg2.connect(user=username, password=password)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    # cursor.execute(f"drop database {db_name}")
    cursor.execute(f'create database {db_name}')
    cursor.close()
    connection.close()


def create_table() -> Session:
    """
    Создание таблиц
    """
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
    return Session(bind=engine)


async def insert_and_update_data(links, hab, hab_title):
    """
    Обновление информации в БД
    Ничего не возвращает, выводит в консоль информацию о новых статьях, добавленных в БД"""
    async with async_session() as s:
        async_engine.echo = False
        for link in links:
            url_article, title, date, author_name, author_url = get_info(link)
            query_article = (select(Article).filter_by(title=title))
            res = await s.execute(query_article)
            result = res.unique().scalars().all()
            query_author = (select(Author).filter_by(name=author_name))
            auth = await s.execute(query_author)
            aut = auth.unique().scalars().first()
            query_hab = (select(Hab).filter_by(link=hab))
            h = await s.execute(query_hab)
            h = h.unique().scalars().first()
            if len(result) == 0:
                print_info(hab_title, hab, title, date, author_name, author_url, url_article)
                if aut is None:
                    author = Author(name=author_name, link=author_url)
                    if h is None:
                        new_hab = Hab(link=hab, title=hab_title)
                        article = Article(title=title, date=date, link=url_article)
                        author.articles = [article]
                        new_hab.articles = [article]
                        s.add_all([author, new_hab])
                    else:
                        article = Article(title=title, date=date, link=url_article, hab=h)
                        author.articles = [article]
                        s.add(author)
                else:
                    if h is None:
                        new_hab = Hab(link=hab, title=hab_title)
                        article = Article(title=title, date=date, link=url_article, author=aut)
                        new_hab.articles = [article]
                        s.add(new_hab)
                    else:
                        article = Article(title=title, date=date, link=url_article, hab=h, author=aut)
                        s.add(article)
        await s.commit()
        async_engine.echo = True


def main():
    create_db()
    create_table()


if __name__ == '__main__':
    main()
