from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()
post_type = Enum('reel', 'post', 'story', name="post_type_enum")

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    post: Mapped[List['Post']] = relationship(
        back_populates='user',
    )
    comment: Mapped['Comment'] = relationship(
        back_populates='user'
    )
    follower_from: Mapped[List['Follower']]=relationship(
        'Follower',
        back_populates='user_from',
        foreign_keys='Follower.user_from_id'
    )
    follower_to: Mapped[List['Follower']]=relationship(
        'Follower',
        back_populates='user_to',
        foreign_keys='Follower.user_to_id'
    )


class Follower(db.Model):
    __tablename__="folowers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_from: Mapped['User']=relationship(
        'User',
        back_populates='follower_from',
        foreign_keys=[user_from_id]
       
    )
    user_to: Mapped['User']= relationship(
        'User',
        back_populates='follower_to',
        foreign_keys=[user_to_id],
    )
class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped['User'] = relationship(
        back_populates='post',
    )
    media: Mapped[List['Media']] = relationship(
        back_populates = 'post',
    )
    comment: Mapped[List['Comment']] = relationship(
        back_populates = 'post',
    )
    

class Media(db.Model):
    __tablename__ = "Medias"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(post_type, nullable=False)
    url: Mapped[str] = mapped_column(String(120),  nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    post: Mapped['Post'] = relationship(
        back_populates='media',

    )
   
class Comment(db.Model):
    __tablename__ = "Comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120),  nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped['User'] = relationship(
        back_populates= 'comment',
    )
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    post: Mapped['Post'] = relationship(
        back_populates='comment',
    )



