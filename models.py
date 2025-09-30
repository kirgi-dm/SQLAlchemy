from sqlalchemy import ForeignKey, String, Integer, text, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, uniq_str, array_or_none
from sql_enums import *
from typing import List


class User(Base):
    username: Mapped[uniq_str]
    email: Mapped[uniq_str]
    password: Mapped[str]
    profile: Mapped['Profile'] = relationship(
        'Profile',
        back_populates='user',
        uselist=False,
        lazy='joined',
    )
    posts: Mapped[List['Post']] = relationship(
        'Post',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    comments: Mapped[List['Comment']] = relationship(
        'Comment',
        back_populates='user',
        cascade='all, delete-orphan',
    )


class Profile(Base):
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    age: Mapped[int] = mapped_column(Integer)
    interests: Mapped[array_or_none]
    contacts: Mapped[dict | None] = mapped_column(JSON)
    user : Mapped['User'] = relationship(
        'User',
        back_populates='profile',
        uselist=False,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)


class Post(Base):
    title: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
    main_photo_url: Mapped[str]
    photos_url: Mapped[array_or_none]
    status: Mapped[StatusPost] = mapped_column(
        default=StatusPost.PUBLISHED,
        server_default=text("'DRAFT'")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        'User',
        back_populates='posts',
        uselist=False,
    )
    comments: Mapped[List['Comment']] = relationship(
        'Comment',
        back_populates='post',
        cascade='all, delete-orphan',
    )


class Comment(Base):
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    rating: Mapped[RatingEnum] = mapped_column(default=RatingEnum.FIVE, server_default=text("'SEVEN'"))
    user: Mapped['User'] = relationship(
        'User',
        back_populates='comments',
    )
    post: Mapped['Post'] = relationship(
        'Post',
        back_populates='comments',
    )