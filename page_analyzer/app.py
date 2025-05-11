import os

import psycopg

from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, get_flashed_messages, url_for

from page_analyzer.repository import UrlRepository
from page_analyzer.validator import validate

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg.connect(DATABASE_URL)
conn.autocommit = True
repo = UrlRepository(conn)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template(
        'urls/index.html'
    )

@app.get('/urls')
def get_urls():
    urls = repo.get_content()
    return render_template(
        'urls/urls.html',
        urls=urls
    )


@app.post('/urls')
def url_post():
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        flash('Некорректный URL', 'danger')
        return redirect('/')
    url_id = repo.save(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=url_id))


@app.route('/urls/<id>')
def show_url(id):
    url = repo.find(id)
    if url is None:
        return render_template(
        'urls/404.html'
    )
    return render_template(
        'urls/show_url.html',
        url=url
    )