from marshmallow import Schema, fields

class UserProfileSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Str()
    username = fields.Str()
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
    id = fields.Str()
    title = fields.Str()
    body = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    author = fields.Nested('UserProfileSchema', 
        only=(
            'id',
            'username'
            ))
    comments = fields.Nested('CommentSchema', many=True,
        only=(
            'id',
            'body',
            'author'
            ))

class CommentSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Str()
    body = fields.Str()
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
    