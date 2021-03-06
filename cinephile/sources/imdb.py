#coding: utf-8

from imdbpie.imdbpie import Imdb


class ImdbSource(object):
    source = Imdb()

    @classmethod
    def find_by_id(cls, movie_id):
        return cls.source.find_movie_by_id(movie_id)

    @classmethod
    def find_by_title(cls, title, file_info=None):
        movies = cls.source.find_by_title(title)
        if file_info is not None \
           and unicode(file_info.get('title')) \
           == unicode(movies[0].get('title')) \
           and unicode(file_info.get('year', 'A')) == \
           unicode(movies[0].get('year', 'B')):
            return cls.find_by_id(movies[0]['imdb_id'])
        else:
            return cls.choose_movie(movies[0:9])

    @classmethod
    def choose_movie(cls, movies, option_template=u"{option}) {year} {title}"):
        # Build option strings.
        options = [option_template.format(option=i + 1, **movie)
                   for i, movie in enumerate(movies)]
        options.append(u'L) Lookup a different title')
        options.append(u'S) Skip this file')

        # Ask for user input.
        print '\n'.join(options)
        choice = raw_input(
            u'Choose an option from the list (1-{}): '.format(len(movies)))

        # Returning None indicates skipping.
        if choice == 'S':
            return None
        elif choice == 'L':
            return cls.find_by_title(raw_input(u'Title: '))
        else:
            try:
                movie = movies[int(choice if choice else 1) - 1]
            except ValueError:
                print u'\nPlease, choose a number between 1 and {}.'.format(
                    len(movies))
                movie = cls.choose_movie(movies, option_template)
            except IndexError:
                print u'\nPlease, choose a number between 1 and {}.'.format(
                    len(movies))
                movie = cls.choose_movie(movies, option_template)
            return cls.find_by_id(movie['imdb_id'])
