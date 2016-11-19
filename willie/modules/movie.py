# -*- coding: utf8 -*-

import json
import willie.web as web
import willie.module


@willie.module.commands('movie', 'imdb', 'peli', 'pelicula', 'film')
def movie(bot, trigger):
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
                message = '[Movie] Error from the imdb API'
    else:
        link = '\x0302http://imdb.com/title/' + data['imdbID'] + '\x0F'
        ratingraw = data['imdbRating']
        if ratingraw < 5:
            rating = '\x0304' + ratingraw + '\x0F'
        elif ratingraw >= 5 and rating < 7:
            rating = '\x0307' + ratingraw + '\x0F'
        else:
            rating = '\x0303' + ratingraw + '\x0F'
        if bot.config.lang == 'ca':
            message = '\x02\x0301,04IMDB\x0F\x02 - ' + data['Title'] + '\x0F' +  \
                    u' | Director: ' + data['Director'] + \
                    u' | Any: ' + data['Year'] + \
                    u' | Valoració: ' + rating + ' i han votat ' + data['imdbVotes'] + ' persones.' + \
                    u' | Gènere: ' + data['Genre'] + \
                    u' | Premis: ' + data['Awards'] + \
                    u' | Duració: ' + data['Runtime'] + \
                    ' | Link a IMDB: ' + link
        elif bot.config.lang == 'es':
            message = '\x02\x0301,04IMDB\x0F\x02 - ' + data['Title'] + '\x0F' +  \
                    u' | Director: ' + data['Director'] + \
                    u' | Año: ' + data['Year'] + \
                    u' | Valoración: ' + rating + ' y han votado ' + data['imdbVotes'] + ' personas.' + \
                    u' | Género: ' + data['Genre'] + \
                    u' | Premios: ' + data['Awards'] + \
                    u' | Duración: ' + data['Runtime'] + \
                    ' | Link a IMDB: ' + link
        else:
            message = '\x02\x0301,04IMDB\x0F\x02 - ' + data['Title'] + '\x0F' + \
                      ' | Director: ' + data['Director'] + \
                      ' | Year: ' + data['Year'] + \
                      ' | Rating: ' + rating + ' and ' + data['imdbVotes'] + ' people have voted.' + \
                      ' | Genre: ' + data['Genre'] + \
                      ' | Awards: ' + data['Awards'] + \
                      ' | Runtime: ' + data['Runtime'] + \
                      ' | IMDB Link: ' + link
    bot.say(message)
