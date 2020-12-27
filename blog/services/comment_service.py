from blog.data_access import db_session
from blog import models
from .exceptions import ResourceNotFound

class CommentService:
    @staticmethod
    def create_comment(body, user_id, post_id):
        """
        Créer un nouveau commentaire
        """
        post = db_session.query(models.Post).get(post_id)
        if post is None:
            raise ResourceNotFound("Resource not found")
        user = db_session.query(models.User).get(user_id)
        comment = models.Comment.create_new_comment(body, user, post)
        db_session.add(comment)
        db_session.commit()
        return comment

    @staticmethod
    def get_comment_by_id(post_id, id):
        """
        Obtenir un commentaire à partir de son identifiant.
        """
        comment = db_session.query(models.Comment).filter(
            models.Comment.post_id==post_id and models.Comment.id==id
        ).one()

        if comment is None:
            raise ResourceNotFound("Resource not found")
        
        return comment
    
    @staticmethod
    def get_all_post_comments(post_id):
        """
        Obtenir tous les commentaires à partir de l'identifiant
        du post.
        """
        comments = db_session.query(models.Comment).filter(
            models.Comment.post_id==post_id
        ).all()

        if comments is None:
            raise ResourceNotFound("Resource not found")

        return comments

    @staticmethod
    def delete_comment(post_id, id):
        """
        Supprimer un commentaire à partir de son identifiant.
        """
        nb_comment = db_session.query(models.Comment).filter(models.Comment.post_id==post_id and models.Comment.id==id).delete()
        db_session.commit()

        if nb_comment == 1:
            return True
        else:
            return False