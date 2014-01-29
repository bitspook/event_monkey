# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, Sequence, Text, Boolean, Date, UnicodeText, Unicode
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship, backref, validates

engine = create_engine("sqlite:///valentine_data.sqlite3")

Session = sessionmaker(engine)
session = Session()

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, Sequence("event_id_seq"),  primary_key=True)

    name = Column(String)
    event_type = Column(String)
    nationality = Column(String)
    language = Column(String)
    date = Column(Date)
    variable_date = Column(Boolean)

    def __repr__(self):
        return "<Event: {}>".format(self.name)

class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, Sequence("content_key_seq"), primary_key=True)

    content_type = Column(Unicode)
    title = Column(Unicode)
    description = Column(Unicode)
    keywords = Column(Unicode)
    body = Column(UnicodeText)
    language = Column(Unicode)
    script = Column(Unicode)

    event_id = Column(Integer, ForeignKey(Event.id))
    event = relationship("Event", backref=backref("content_list"), foreign_keys=[event_id])

    def __repr__(self):
        return "<Content: {}>".format(self.content_type)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, Sequence("tags_key_seq"), primary_key=True)
    tag = Column(String)
    content_list = relationship("Content", backref=backref("tags"), secondary="tags_table")

    def __repr__(self):
        return "<Tag: {}>".format(self.tag)


tags_table = Table('tags_table', Base.metadata,
                   Column('tag_id', Integer, ForeignKey('tags.id')),
                   Column('content_id', Integer, ForeignKey('content.id'))
        )
