import requests
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user_model import User

@app.route('/', methods=["POST", "GET"])
def index():
    return redirect(url_for('search'))

@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == 'POST':
        q = request.form['query']
        return redirect(url_for('retrieve', query = q))
    else:
        return render_template('index.html')

@app.route('/search/<query>')
def retrieve(query):
    search_query = query
    url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}&projection=full&maxResults=15&key=AIzaSyCTpXZvTmFbh4dcb4nev3AmI-dbvCkxrSg'
    response = requests.get(url)
    results = response.json()['items']
    books = get_books(results)
    return render_template('search.html', query = query, books = books)

def get_books(result):
    books = []
    for book in result:
        book_info = {
            'id' : book['id'],
            'thumbnail' : book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else 'https://savanisbookshop.com/uploads/image/savanisbookshop.jpeg',
            'title' : book['volumeInfo']['title'] if 'title' in book['volumeInfo'] else 'No title available.',
            'author' : book['volumeInfo']['authors'][0] if 'authors' in book['volumeInfo'] else 'No author available.',
            'publisher' : book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else 'No publisher available.',
            'description' : book['volumeInfo']['description'] if 'description' in book['volumeInfo'] else 'No description available.',
            'rating' : f"{book['volumeInfo']['averageRating']}/5" if 'averageRating' in book['volumeInfo'] else 'No rating available.',
            'link': book['volumeInfo']['infoLink'] if 'infoLink' in book['volumeInfo'] else ' '
        }
        
        books.append(book_info)
    return books

@app.route('/savebook')
def save():
    redirect('/dashboard')