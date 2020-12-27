from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relationship, synonym
from .connection import metadata, db_session
from ..models import User, Post, Comment
from datetime import datetime
import uuid

def generate_unique_id():
    """
    Genere un identifiant unique.
    """
    return str(uuid.uuid1())

"""
Définit la table user
"""
user = Table('user', metadata,
            Column('id', String, default=generate_unique_id, primary_key=True),
            Column('username', String(30), unique=True, nullable=False),
            Column('password_hash', String(100), nullable=False),
            Column('is_admin', Boolean, nullable=False),
            Column('is_banned', Boolean, nullable=False),
            Column('created_at', DateTime, default=datetime.now, nullable=False),
            Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
        )

"""
Définit la table post
"""
post = Table('post', metadata,
            Column('id', String, default=generate_unique_id, primary_key=True),
            Column('title', String(200), unique=True, nullable=False),
            Column('body', String, nullable=False),
            Column('created_at', DateTime, default=datetime.now, nullable=False),
            Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
            Column('author_id', String, ForeignKey('user.id'), nullable=False)
        )

"""
Définit la table comment
"""
comment = Table('comment', metadata,
            Column('id', String, default=generate_unique_id, primary_key=True),
            Column('body', String, nullable=False),
            Column('author_id', String, ForeignKey('user.id'), nullable=False),
            Column('post_id', String, ForeignKey('post.id'), nullable=False),
            Column('parent_comment_id', String, ForeignKey('comment.id'), nullable=True),
            Column('created_at', DateTime, default=datetime.now, nullable=False),
            Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
        )


def start_mappers():
    """
    Lie les classes du modèles aux tables de la base de données.
    """
    mapper(User, user, properties={
        'posts': relationship(Post, backref="author"),
        'username': synonym(
            "_User__username", 
            map_column=True,
            descriptor=User.username
        ),
        'password_hash': synonym(
            "_User__password_hash", 
            map_column=True,
            descriptor=User.password_hash
        ),
        'is_admin': synonym(
            "_User__is_admin", 
            map_column=True,
            descriptor=User.is_admin
        ),
        'is_banned': synonym(
            "_User__is_banned", 
            map_column=True,
            descriptor=User.is_banned
        )
    })

    mapper(Post, post, properties={
        'comments': relationship(Comment, 
            backref="post",
        ),
        'title': synonym(
            "_Post__title", 
            map_column=True,
            descriptor=Post.title
        ),
        'body': synonym(
            "_Post__body", 
            map_column=True,
            descriptor=Post.body
        )
    })

    mapper(Comment, comment, properties={
        'author': relationship(User),
        'child_comment': relationship(Comment, uselist=False),
        'body': synonym(
            "_Comment__body", 
            map_column=True,
            descriptor=Comment.body
        ),
    })