#coding: utf-8

from imdbpie.imdbpie import Imdb


class ImdbSource(object):
    source = Imdb()

    @classmethod
    def find_by_title(cls, title):
        return cls.source.find_by_title(title)[0:5]

    @classmethod
    def find_by_id(cls, movie_id):
        return cls.source.find_movie_by_id(movie_id)

    @classmethod
    def choose_movie(cls, movies, option_template=u"{option}) {year} {title}"):
        # Build option strings.
        options = [option_template.format(option=i + 1, **movie)
                   for i, movie in enumerate(movies)]

        # Ask for user input.
        print '\n'.join(options)
        choice = raw_input(
            'Choose an option from the list (1-{}): '.format(len(movies)))

        try:
            movie = movies[int(choice if choice else 1) - 1]
        except ValueError:
            print '\nPlease, choose a number between 1 and {}.'.format(
                len(movies))
            movie = cls.choose_movie(movies, option_template)
        except IndexError:
            print '\nPlease, choose a number between 1 and {}.'.format(
                len(movies))
            movie = cls.choose_movie(movies, option_template)

        return cls.find_by_id(movie['imdb_id'])
