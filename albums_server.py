from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

def russify(n):
    if n > 99:
        n = int(str(n)[-2:])
    if n < 15 and n > 10:
        return str(n) + " альбомов"

    last_digit = str(n)[-1]
    if last_digit == "1":
        return str(n) + " альбом"
    elif last_digit == "2" or last_digit == "3" or last_digit == "4":
        return str(n) + " альбома"
    else:
        return str(n) + " альбомов"

@route("/albums/<artist>")
def artist_get(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "<h3>Найдено {0} исполнителя {1}:</h3>".format(russify(len(albums_list)), artist)
        result += "Список альбомов {}<br>".format(artist)
        result += "<br>".join(album_names)
    return result

def album_valid(album_data):
    print(album_data["year"], album_data["year"].isdigit())
    return album_data["year"].isdigit()

@route("/albums", method="POST")
def album_post():

    album_data = {
            "year": request.forms.get("year"),
            "artist": request.forms.get("artist"),
            "genre": request.forms.get("genre"),
            "album": request.forms.get("album")
        }

    if album.album_exists(request.forms.get("album")):
        return HTTPError(409, "Альбом уже существует в базе")

    if not album_valid(album_data):
        return HTTPError(415, "Ошибка валидации данных")
    else:
        album_data["year"] = int(album_data["year"])
        album.append(album_data)
        return album_data


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
