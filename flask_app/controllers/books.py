from flask_app import app
from flask import render_template, redirect, flash, session, request

from flask_app.models.book import Book

@app.route('/books')
def books():
    if 'user_id' in session:
        return render_template('books.html', books = Book.get_all())
    return redirect('/')


@app.route('/books/new')
def addBook():
    if 'user_id' in session:
        return render_template('addBook.html')
    
    return redirect('/')

@app.route('/book', methods = ['POST'])
def createBook():
    if 'user_id' not in session:
        return redirect('/')
    if not Book.validate_book(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'nrOfPages': request.form['nrOfPages'],
        'price': request.form['price'],
        'author': request.form['author'],
        'user_id': session['user_id'] # id e personit te loguar
    }
    Book.create(data)
    return redirect('/')


@app.route('/book/<int:id>')
def viewBook(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
        'book_id': id
    }
    book = Book.get_book_by_id(data)
    if book:
        usersWhoLikes = Book.get_users_who_liked_by_book_id(data)
        return render_template('book.html', book=book, usersWhoLikes= usersWhoLikes)
    return redirect('/')

@app.route('/book/edit/<int:id>')
def editBook(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    book = Book.get_book_by_id(data)
    if book and book['user_id'] == session['user_id']:
        return render_template('editBook.html', book=book)
    return redirect('/')


@app.route('/book/update/<int:id>', methods = ['POST'])
def updateBook(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    book = Book.get_book_by_id(data)
    if book and book['user_id'] == session['user_id']:
        if not Book.validate_bookUpdate(request.form):
            return redirect(request.referrer)
        data = {
            'description': request.form['description'],
            'nrOfPages': request.form['nrOfPages'],
            'price': request.form['price'],
            'id': id
        }
        Book.update(data)
        return redirect('/book/'+ str(id))
    return redirect('/')



@app.route('/book/delete/<int:id>')
def deleteBook(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
    }
    book = Book.get_book_by_id(data)
    if book['user_id'] == session['user_id']:
        Book.delete_all_book_comments(data)
        Book.delete(data)
    return redirect('/')

@app.route('/add/comment/<int:id>', methods = ['POST'])
def addComment(id):
    if 'user_id' not in session:
        return redirect('/')
    if len(request.form['comment'])<2:
        flash('The comment should be at least 2 characters', 'comment')
    data = {
        'comment': request.form['comment'],
        'user_id': session['user_id'],
        'book_id': id
    }
    Book.addComment(data)
    return redirect(request.referrer)

@app.route('/update/comment/<int:id>', methods = ['POST'])
def updateComment(id):
    if 'user_id' not in session:
        return redirect('/')
    if len(request.form['comment'])<2:
        flash('The comment should be at least 2 characters', 'comment')
    data = {
        'comment': request.form['comment'],
        'id': id
    }
    komenti = Book.get_comment_by_id(data)
    if komenti['user_id'] == session['user_id']:
        Book.update_comment(data)
    return redirect('/book/'+ str(komenti['book_id']))

@app.route('/delete/comment/<int:id>')
def deleteComment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    komenti = Book.get_comment_by_id(data)
    if komenti['user_id'] == session['user_id']:
        Book.delete_comment(data)
    return redirect(request.referrer)



@app.route('/edit/comment/<int:id>')
def editComment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    commenti = Book.get_comment_by_id(data)
    if commenti['user_id'] == session['user_id']:
        return render_template('editComment.html', commenti = commenti)
    return redirect('/')


@app.route('/add/like/<int:id>')
def addLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    usersWhoLikes = Book.get_users_who_liked_by_book_id(data)
    print(usersWhoLikes)
    if session['user_id'] not in usersWhoLikes:
        Book.addLike(data)
    return redirect(request.referrer)

@app.route('/remove/like/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    Book.removeLike(data)
    return redirect(request.referrer)