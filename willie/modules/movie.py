# -*- coding: utf8 -*-

import json
import willie.web as web
import willie.module


@willie.module.commands('movie', 'imdb', 'peli', 'pelicula', 'film')
@willie.module.example('.movie Movie Title')
def movie(bot, trigger):
    """
    Returns some information about a movie, like Title, Year, Rating, Genre and IMDB Link.
    """
    if not trigger.group(2):
        return
    word = trigger.group(2).rstrip()
    word = word.replace(" ", "+")
    uri = "http://www.omdbapi.com/?t=" + word
    u = web.get_urllib_object(uri, 30)
    data = json.load(u)  # data is a Dict containing all the information we need
    u.close()
    if data['Response'] == 'False':
        if 'Error' in data:
            message = '[MOVIE] %s' % data['Error']
        else:
            bot.debug(__file__, 'Got an error from the imdb api, search phrase was %s' % word, 'warning')
            bot.debug(__file__, str(data), 'warning')
            if bot.config.lang == 'ca':
                message = u'[Pel·lícula] Error de l\'API d\'imdb'
            elif bot.config.lang == 'es':
                message = u'[Película] Error de la API de imdb'
            else:
                message = '[MOVIE] Error from the imdb API'
    else:
        if bot.config.lang == 'ca':
            message = u'[Pel·lícula] Títol: ' + data['Title'] + \
                    u' | Director: ' + data['Director'] + \
                    u' | Any: ' + data['Year'] + \
                    u' | Valoració: ' + data['imdbRating'] + ' i ' + data['imdbVotes'] + ' persones han votat.' + \
                    u' | Gènere: ' + data['Genre'] + \
                    u' | Premis: ' + data['Awards'] + \
                    u' | Duració: ' + data['Runtime'] + \
                    ' | Link a IMDB: http://imdb.com/title/' + data['imdbID']
        elif bot.config.lang == 'es':
            message = u'[Película] Título: ' + data['Title'] + \
                    u' | Director: ' + data['Director'] + \
                    u' | Año: ' + data['Year'] + \
                    u' | Valoración: ' + data['imdbRating'] + ' y ' + data['imdbVotes'] + ' personas han votado.' + \
                    u' | Género: ' + data['Genre'] + \
                    u' | Premios: ' + data['Awards'] + \
                    u' | Duración: ' + data['Runtime'] + \
                    ' | Link a IMDB: http://imdb.com/title/' + data['imdbID']
        else:
            message = '[MOVIE] Title: ' + data['Title'] + \
                      ' | Director: ' + data['Director'] + \
                      ' | Year: ' + data['Year'] + \
                      ' | Rating: ' + data['imdbRating'] + ' and ' + data['imdbVotes'] + ' people have voted.' + \
                      ' | Genre: ' + data['Genre'] + \
                      ' | Awards: ' + data['Awards'] + \
                      ' | Runtime: ' + data['Runtime'] + \
                      ' | IMDB Link: http://imdb.com/title/' + data['imdbID']
    bot.say(message)
