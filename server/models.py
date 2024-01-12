from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Author(db.Model, SerializerMixin):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author must have a name.")
        author = type(self).query.filter_by(name=value).first()
        if author:
            raise ValueError("Author names must be unique.")
        return value

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone numbers must have 10 digits.")
        return phone_number

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary must be under 250 characters.")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category

    @validates("title")
    def validate_title(self, key, title):
        click_baits = ["Won't Believe", "Secret", "Top", "Guess"]
        for bait in click_baits:
            if bait in title:
                return title
        raise ValueError("Not clickbait-y enough.")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"
