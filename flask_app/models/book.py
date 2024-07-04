from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Book:
    db_name = "mvcusersbooks"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.nrOfPages = data['nrOfPages']
        self.price = data['price']
        self.author = data['author']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO books (title, description, nrOfPages, price, author, user_id) VALUES (%(title)s, %(description)s, %(nrOfPages)s, %(price)s, %(author)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
     

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.db_name).query_db(query)
        books = []
        if results:
            for book in results:
                books.append(book)
        return books

    @classmethod
    def get_book_by_id(cls, data):
        query = "SELECT * FROM books LEFT JOIN users on books.user_id = users.id WHERE books.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            comments = []
            query2 = "SELECT * FROM comments left join users on comments.user_id = users.id where comments.book_id = %(id)s;"
            result2 = connectToMySQL(cls.db_name).query_db(query2, data)
            if result2:
                for comment in result2:
                    comments.append(comment)
            result[0]['comments'] = comments
            query3 = "SELECT users.firstName, users.lastName FROM likes left join users on likes.user_id = users.id where likes.book_id = %(id)s;"
            result3 = connectToMySQL(cls.db_name).query_db(query3, data)
            likes = []
            if result3:
                for like in result3:
                    likes.append(like)
            result[0]['likes'] = likes
            return result[0]
        return False
    
    @classmethod
    def get_comment_by_id(cls, data):
        query = "SELECT * FROM comments where comments.id = %(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_all_book_comments(cls, data):
        query ="DELETE FROM comments where comments.book_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE books set description = %(description)s, price=%(price)s, nrOfPages = %(nrOfPages)s WHERE books.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    # functionality for comments
    @classmethod
    def addComment(cls, data):
        query = "INSERT INTO comments (comment, user_id, book_id) VALUES (%(comment)s, %(user_id)s, %(book_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def update_comment(cls, data):
        query = "UPDATE comments set comment = %(comment)s where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
      

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def removeLike(cls, data):
        query = "DELETE FROM likes WHERE book_id=%(book_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_users_who_liked_by_book_id(cls, data):
        query ="SELECT user_id FROM likes where book_id = %(book_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        usersId = []
        if results:
            for userId in results:
                usersId.append(userId['user_id'])
        return usersId
                

    @staticmethod
    def validate_book(book):
        is_valid = True
        if len(book['title'])< 2:
            flash('Title should be more  or equal to 2 characters', 'title')
            is_valid = False
        if len(book['description'])< 10:
            flash('Description should be more  or equal to 10 characters', 'description')
            is_valid = False
        if len(book['nrOfPages'])< 1:
            flash('Number of pages is required', 'nrOfPages')
            is_valid = False
        if len(book['price'])< 1:
            flash('Price is required', 'price')
            is_valid = False
        if len(book['author'])< 2:
            flash('Author name should be more  or equal to 2 characters', 'author')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_bookUpdate(book):
        is_valid = True
        if len(book['description'])< 10:
            flash('Description should be more  or equal to 10 characters', 'description')
            is_valid = False
        if len(book['nrOfPages'])< 1:
            flash('Number of pages is required', 'nrOfPages')
            is_valid = False
        if len(book['price'])< 1:
            flash('Price is required', 'price')
            is_valid = False
        return is_valid