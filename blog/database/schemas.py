from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Str()
    username = fields.Str()
    password_hash = fields.Str()
    is_admin = fields.Boolean()
    is_banned = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    posts = fields.Nested('PostSchema', many=True,
        only=(
            'id',
            'title',
            'body',
            'created_at',
            'updated_at'
        ))

class PostSchema(Schema):
    class Meta:
        ordered = True
    ordered = False
    id = fields.Str()
    title = fields.Str()
    body = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    author = fields.Nested('UserSchema', 
        only=(
            'id',
            'username',
            'password_hash',
            'is_admin',
            'is_banned',
            'created_at',
            'updated_at'
            ))

class CommentSchema(Schema):
    class Meta:
        ordered = True
    body = fields.Str()
    author = fields.Nested('UserSchema', 
        only=(
            'id',
            'username',
            'password_hash',
            'is_admin',
            'is_banned',
            'created_at',
            'updated_at'
            ))
    post = fields.Nested('PostSchema',
        only=(
            'id',
            'title',
            'body',
            'created_at',
            'updated_at'
        ))
    parent_comment = fields.Nested('CommentSchema')
    