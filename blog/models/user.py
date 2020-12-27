from __future__ import annotations
from typing import List, NoReturn, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from . import Post

import uuid
import datetime
import hashlib

"""
Module qui contient la classe User
"""

class User:
    """
    Classe representant un utilisateur du blog
    """

    def __init__(
        self,
        username: str,
        password_hash: str,
        is_admin: bool, 
        is_banned: bool,
        posts: Optional[List[Post]]
    ) -> None:
        """
        Constructeur de la classe 
        """

        self.__username: str = username
        self.__password_hash: str = password_hash
        self.__is_admin: bool = is_admin
        self.__is_banned: bool = is_banned
        self.posts: Optional[List[Post]] = posts

    @classmethod
    def create_new_user(
        cls,
        username: str,
        password: str,
        is_admin: bool = False,
        is_banned: bool = False,
        ) -> User:
        """
        Constructeur pour créer un nouvel utilisateur.
        """

        return cls(
            username=username,
            password_hash=hashlib.sha512(password.encode("utf-8")).hexdigest(),
            is_admin=is_admin,
            is_banned=is_banned,
            posts=list()
        )

    @property
    def username(self) -> str:
        """
        Obtenir le nom d'utilisateur.
        """

        return self.__username

    @username.setter
    def username(self, new_username: str) -> None:
        """
        Définir un nouveau nom d'utilisateur.
        """

        self.__username = new_username

    @property
    def is_admin(self) -> bool:
        """
        Obtenir le role de l'utilisateur.
        """

        return self.__is_admin

    @is_admin.setter
    def is_admin(self, new_state: bool) -> None:
        """
        Définir un rôle pour l'utilisateur.
        """

        self.__is_admin = new_state
    
    @property
    def is_banned(self) -> bool:
        """
        Obtenir le status de l'utilisateur.
        """
        
        return self.__is_banned

    @is_banned.setter
    def is_banned(self, new_state: bool) -> None:
        """
        Définir le status de l'utilisateur.
        """

        self.__is_banned = new_state

    @property
    def password_hash(self) -> str:
        """
        Obtenir le hash du mot de passe.
        """

        return self.__password_hash

    def set_password(self, new_password: str) -> None:
        """
        Définir un nouveau mot de passe
        """

        self.__password_hash = hashlib.sha512(new_password.encode("utf-8")).hexdigest()

    def check_password(self, password: str) -> bool:
        """
        Prend en paramètre un mot de passe et renvoie
        True si le mot de passe est le mot de passe de l'utilisateur
        False sinon.
        """ 

        if self.__password_hash == hashlib.sha512(password.encode("utf-8")).hexdigest():
            return True
        return False