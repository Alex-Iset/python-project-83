import validators


def is_valid_url(url):
    return validators.url(url)


def validate(url):
    errors = {}
    if not url:
        errors['url'] = 'Поле URL не заполнено'
    if not is_valid_url(url) and len(url) < 255:
        errors['url'] = 'Некорректный URL'
    return errors
