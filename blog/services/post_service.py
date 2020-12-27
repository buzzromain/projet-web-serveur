from blog.data_access import db_session
from blog import models
from .exceptions import ResourceNotFound

class PostService:
    @staticmethod
    def create_post(title, body, author_id):
        """
        Créer un post
        """
        user = db_session.query(models.User).get(author_id)
        post = models.Post.create_new_post(title, body, user)
        db_session.add(post)
        db_session.commit()
        return post

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
    def delete_post(id):
        """
        Supprimer un post à partir de son identifiant
        """
        post = db_session.query(models.Post).get(id)
        if post is None:
            raise ResourceNotFound("Resource not found")
        for comment in post.comments:
            db_session.delete(comment)
        db_session.delete(post)
        db_session.commit()
        return True