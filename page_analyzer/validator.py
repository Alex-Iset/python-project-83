import validators


def validate(url):
    if not url:
        return 'Поле URL не заполнено'
    if not validators.url(url):
        return 'Некорректный URL'
    if len(url) > 255:
        return 'URL не должен превышать 255 символов'
