from __future__ import annotations
from typing import List, NoReturn, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from . import User
    from . import Comment

import datetime
import uuid

"""
Module qui contient la classe Post
"""

class Post:
    """
    Classe representant un post du blog
    """

    def __init__(
        self,
        title: str,
        body: str,
        author: User,
        comments: Optional[List[Comment]] = None
        ) -> None:
        """
        Constructeur de la classe 
        """

        self.__title: str = title
        self.__body: str = body
        self.__author: User = author
        self.__comments: Optional[List[Comment]] = comments

    @classmethod
    def create_new_post(cls, title: str, body: str, author: User) -> Post:
        """
        Constructeur pour créer un nouveau post.
        """

        return cls(
            title=title,
            body=body,
            author=author,
            comments=list()
        )

    @property
    def title(self) -> str:
        """
        Obtenir le titre
        """

        return self.__title

    @title.setter
    def title(self, new_title: str) -> None:
        """
        Définir le titre
        """

        self.__title = new_title

    @property
    def body(self) -> str:
        """
        Obtenir le corps du post
        """

        return self.__body

    @body.setter
    def body(self, new_body: str) -> None:
        """
        Définir le corps du post
        """

        self.__body = new_body

    @property
    def author(self) -> User:
        """
        Obtenir l'auteur du post.
        """

        return self.__author

    @property
    def comments(self) -> Optional[List[Comment]]:
        """
        Obtenir la liste de commentaires.
        """

        return self.__comments