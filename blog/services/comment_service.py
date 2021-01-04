from blog.data_access import db_session
from blog import models
from .exceptions import ResourceNotFound, UnauthorizedUser

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
        if user.is_banned:
            raise UnauthorizedUser("User is not authorized")
        comment = models.Comment.create_new_comment(body, user, post)
        db_session.add(comment)
        db_session.commit()
        return comment

    @staticmethod
    def get_comment_by_id(post_id, comment_id):
        """
        Obtenir un commentaire à partir de son identifiant.
        """
        try:
            comments = db_session.query(models.Comment).filter(
                models.Comment.post_id==post_id, models.Comment.id==comment_id
            ).all()
            comment = comments[0]
        except:
            comment = None

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

        return comments

    @staticmethod
    def update_comment(new_body, post_id, comment_id, user_id):
        """
        Mettre à jour un commentaire à partir de son identifiant.
        """
        try:
            comments = db_session.query(models.Comment).filter(
                models.Comment.post_id==post_id, models.Comment.id==comment_id
            ).all()
            comment = comments[0]
        except:
            comment = None

        if comment is not None:
            user = db_session.query(models.User).get(user_id)
            if user.is_banned and user.id == user_id:
                raise UnauthorizedUser("User is not authorized")
            else:
                comment.body = new_body
                db_session.commit()
                return comment
        else:
            raise ResourceNotFound("Resource not found")


    @staticmethod
    def delete_comment(post_id, comment_id, user_id):
        """
        Supprimer un commentaire à partir de son identifiant.
        """
        try:
            comments = db_session.query(models.Comment).filter(
                models.Comment.post_id==post_id, models.Comment.id==comment_id
            ).all()
            comment = comments[0]
        except:
            comment = None

        if comment is not None:
            user = db_session.query(models.User).get(user_id)

            if comment.author.id == user.id or user.is_admin:
                db_session.delete(comment)
                db_session.commit()
                return True
            else:
                raise UnauthorizedUser("User is not authorized")
        else:
            raise ResourceNotFound("Resource not found")
