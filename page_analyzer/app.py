import os

import requests

from bs4 import BeautifulSoup

from w3lib.url import canonicalize_url

from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, url_for, abort

from page_analyzer.repository import DataBase, get_db, close_db
from page_analyzer.validator import validate

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.teardown_appcontext(close_db)


@app.errorhandler(Exception)
def handle_exception(error):
    if error.code == 404:
        return render_template('errors/404.html'), 404
    elif error.code == 500:
        return render_template('errors/500.html'), 500


@app.get('/')
def index():
    return render_template('urls/index.html')


@app.get('/urls')
def get_urls():
    repo = DataBase(get_db(DATABASE_URL))
    urls = repo.get_urls()
    for url in urls:
        last_check = repo.get_last_check(url['id'])
        url['last_check'] = last_check
    return render_template(
        'urls/urls.html',
        urls=urls
    )


@app.post('/urls')
def url_post():
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        flash(errors, 'danger')
        return redirect('/', code=422)
    repo = DataBase(get_db(DATABASE_URL))
    norm_url = canonicalize_url(url).rstrip('/')
    exist_url = repo.get_url(norm_url)
    if exist_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=exist_url['id']))
    url_id = repo.save_url(norm_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=url_id))


@app.get('/urls/<int:id>')
def show_url(id):
    repo = DataBase(get_db(DATABASE_URL))
    url = repo.find_url(id)
    if url is None:
        abort(404)
    checks = repo.get_checks(id)
    return render_template(
        'urls/show_url.html',
        url=url,
        checks=checks
    )


@app.post('/urls/<int:id>/checks')
def check_url(id):
    repo = DataBase(get_db(DATABASE_URL))
    url = repo.find_url(id)
    try:
        response = requests.get(url['name'], timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        description_tag = soup.find("meta", attrs={"name": "description"})
        info = {
            'h1': soup.h1.string if soup.h1 else '',
            'title': soup.title.string if soup.title else '',
            'description': (
                description_tag["content"]
                if description_tag and "content" in description_tag.attrs
                else ''
            ),
        }
        repo.save_check(
            url_id=id,
            status_code=response.status_code,
            h1=info['h1'],
            title=info['title'],
            description=info['description']
        )
        flash('Страница успешно проверена', 'success')
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for('show_url', id=id))