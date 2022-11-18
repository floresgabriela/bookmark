from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# import re
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (username, password, created_at, updated_at) VALUES (%(username)s, %(password)s, NOW(), NOW());"
        results =  connectToMySQL('bookmark').query_db(query, data)
        return results
    
    @classmethod
    def get_one_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results =  connectToMySQL('bookmark').query_db(query, data)
        
        if not results or len(results) < 1:
            return False
        else:
            return cls(results[0])
        
    @staticmethod
    def validate_user(data):
        is_valid = True
        
        if len(data['username']) < 1:
            is_valid = False
            flash('Username must not be blank.', 'register')
            
        # if not EMAIL_REGEX.match(data['email']):
        #     is_valid = False
        #     flash('Invalid email address.', 'register')
            
        if len(data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters.', 'register')
            
        if data['password'] != data['confirm-password']:
            is_valid = False
            flash('Passwords must match.', 'register')
        
        return is_valid