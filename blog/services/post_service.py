from blog.data_access import db_session
from blog import models
from .exceptions import ResourceNotFound, UnauthorizedUser

class PostService:
    @staticmethod
    def create_post(title, body, author_id):
        """
        Créer un post
        """
        user = db_session.query(models.User).get(author_id)
        if user.is_admin:
            post = models.Post.create_new_post(title, body, user)
            db_session.add(post)
            db_session.commit()
            return post
        else:
            raise UnauthorizedUser("User is not admin")

    @staticmethod
    def get_post_by_id(id):
        """
        Obtenir un post à partir de son identifiant
        """
        post = db_session.query(models.Post).get(id)
        if post is None:
            raise ResourceNotFound("Resource not found")
        return post

    @staticmethod
    def get_all_post():
        """
        Obtenir tous les posts du blog
        """
        return db_session.query(models.Post).all()

    @staticmethod
    def update_post_by_id(new_title, new_body, id, user_id):
        """
        Mettre à jour un post du blog
        """
        user = db_session.query(models.User).get(user_id)
        if user.is_admin:
            post = db_session.query(models.Post).get(id)
            if post is not None:
                post.title = new_title
                post.body = new_body
                db_session.commit()
                return post
            else:
                raise ResourceNotFound("Resource not found")
        else:
            raise UnauthorizedUser("User is not authorized")
        

    @staticmethod
    def delete_post(id, user_id):
        """
        Supprimer un post à partir de son identifiant
        """
        post = db_session.query(models.Post).get(id)
        if post is not None:
            user = db_session.query(models.User).get(user_id)
            if user.is_admin == False:
                raise UnauthorizedUser("User not authorized")
            for comment in post.comments:
                db_session.delete(comment)
            db_session.delete(post)
            db_session.commit()
            return True
        else:
            raise ResourceNotFound("Resource not found")