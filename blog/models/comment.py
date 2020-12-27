from __future__ import annotations
from typing import List, NoReturn, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from . import User
    from . import Post

import datetime
import uuid

"""
Module qui contient la classe Comment
"""

class Comment:
    """
    Classe representant un commentaire du blog
    """

    def __init__(
        self,
        body: str,
        author: User,
        post: Post,
        child_comment: Optional[Comment],
        ) -> None:
        """
        Constructeur de la classe 
        """

        self.__body: str = body
        self.author: User = author
        self.post: Post = post
        self.child_comment: Optional[Comment] = child_comment

    @classmethod
    def create_new_comment(cls, body: str, author: User, post: Post) -> Comment:
        """
        Constructeur pour créer un nouveau commentaire.
        """

        return cls(
            body=body,
            author=author,
            post=post,
            child_comment=None,
        )
        
    @property
    def body(self) -> str:
        """
        Obtenir le corps du commentaire
        """

        return self.__body

    @body.setter
    def body(self, new_body: str) -> None:
        """
        Définir le corps du commentaire
        """
        
        self.__body = new_body