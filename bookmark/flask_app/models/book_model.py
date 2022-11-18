from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.author = data['author']
        self.publisher = data['publisher']
        self.thumbnail = data['thumbnail']
        self.rating = data['rating']
        