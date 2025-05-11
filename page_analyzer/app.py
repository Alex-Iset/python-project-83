import os

from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, url_for

from page_analyzer.repository import UrlRepository, get_db, close_db
from page_analyzer.validator import validate

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.teardown_appcontext(close_db)


@app.get('/')
def index():
    return render_template(
        'urls/index.html'
    )

@app.get('/urls')
def get_urls():
    repo = UrlRepository(get_db(DATABASE_URL))
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
    repo = UrlRepository(get_db(DATABASE_URL))
    url_id = repo.save(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=url_id))


@app.route('/urls/<id>')
def show_url(id):
    repo = UrlRepository(get_db(DATABASE_URL))
    url = repo.find(id)
    if url is None:
        return render_template(
        'urls/404.html'
    )
    return render_template(
        'urls/show_url.html',
        url=url
    )