#!/usr/bin/env python

import os
from argparse import ArgumentParser
from guessit import guess_file_info
from sources.imdb import ImdbSource


def main():
    parser = ArgumentParser(
        'Lookup, rename and organize movie files in your collection.')
    parser.add_argument('filepath', metavar='PATH',
                        help='A file to lookup metadata for.')
    parser.add_argument('--suggestion', default='',
                        help='A file to lookup metadata for.')
    parser.add_argument('--movie_dir_template',
                        default='{movie.year} {movie.title}',
                        help='A file to lookup metadata for.')
    parser.add_argument('--movie_file_template',
                        default='{movie.year} {movie.title}',
                        help='A file to lookup metadata for.')
    parser.add_argument('--movies_dir', default=os.path.expanduser('~/Movies'),
                        help='A file to lookup metadata for.')
    args = parser.parse_args()

    # Get possible matches
    source = ImdbSource()
    print 'Input: {}'.format(args.filepath)
    file_info = guess_file_info(args.filepath, 'autodetect')
    movie = source.choose_movie(source.find_by_title(
        args.suggestion if args.suggestion else file_info['title']))

    # Rename and move the movie file.
    os.renames(args.filepath, os.path.join(
        args.movies_dir,
        args.movie_dir_template.format(movie=movie),
        args.movie_file_template.format(movie=movie) + file_info['container']))

if __name__ == '__main__':
    main()
