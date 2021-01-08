from marshmallow import Schema, fields
import datetime

class UserProfileSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    is_admin = fields.Boolean()
    is_banned = fields.Boolean()
    created_at = fields.Function(lambda obj: obj.created_at)
    updated_at = fields.Function(lambda obj: obj.updated_at)
    posts = fields.Nested('PostSchema', many=True,
        only=(
            'id',
            'title',
            'body',
            'created_at',
            'updated_at'
        ))

class PostSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    body = fields.Str()
    created_at = fields.Function(lambda obj: obj.created_at)
    updated_at = fields.Function(lambda obj: obj.updated_at)
    author = fields.Nested('UserProfileSchema', 
        only=(
            'id',
            'username'
            ))
    comments = fields.Nested('CommentSchema', many=True,
        only=(
            'id',
            'body',
            'author',
            'created_at',
            'updated_at'
            ))

class CommentSchema(Schema):
    id = fields.Str()
    body = fields.Str()
    created_at = fields.Function(lambda obj: obj.created_at)
    updated_at = fields.Function(lambda obj: obj.updated_at)
    author = fields.Nested('UserProfileSchema',
        only=(
            'id',
            'username',
            ))
    post = fields.Nested('PostSchema',
        only=(
            'id',
            'title',
            'body',
            'created_at',
            'updated_at'
        ))
    child_comment = fields.Nested('CommentSchema')
    