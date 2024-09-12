from sqlalchemy import MetaData, ForeignKey, Integer, Column, String
from sqlalchemy.orm import declarative_base, relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Author(Base):
    """Таблица с авторами статей"""
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    articles = relationship('Article', back_populates='author')


class Hab(Base):
    """Таблица с хабами"""
    __tablename__ = "habs"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    articles = relationship('Article', back_populates='hab')


class Article(Base):
    """Таблица со статьями"""
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    date = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="articles")
    hab_id = Column(Integer, ForeignKey('habs.id'))
    hab = relationship("Hab", back_populates="articles")
