from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
#from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    password = Column(String)
    email = Column(String, default=None)
    partner = Column(String, default='Partner')
    scratch_time_user = Column(Integer, default=0)
    scratch_time_partner = Column(Integer, default=0)
    user_sex = Column(String, default=None)
    partner_sex = Column(String, default=None)
    is_active = Column(Boolean, default=False)

    #comments = relationship('Comment', back_populates='users')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    user_login = Column(String)  #, ForeignKey('users.id'))
    comment = Column(String)
    date_of_creation = Column(DateTime)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    test = Column(Boolean, default=True)

    #users = relationship('User', back_populates='comments')

#  alembic revision --autogenerate -m 'initial'
#  alembic upgrade +2 две версии включая текущую для апгрейда
#  alembic downgrade -1 на предыдущую для даунгрейда
#  alembic current получить информацию о текущей версии
#  alembic history --verbose история миграций, более подробнее можно почитать в документации.
#  alembic downgrade base даунгрейд в самое начало миграций
#  alembic upgrade head применение самой последней созданной миграции
