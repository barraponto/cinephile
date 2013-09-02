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
    print u'\nInput: {}\n'.format(args.filepath)
    file_info = guess_file_info(args.filepath, 'autodetect')
    movie = source.find_by_title(
        args.suggestion if args.suggestion else file_info['title'],
        file_info)

    # If it returned none, it wants to skip.
    if movie is None:
        import sys
        print 'Skipping on {}.'.format(args.filepath)
        sys.exit()

    # Prepare the extension.
    file_extension = u''
    if file_info.get('cdNumber'):
        file_extension += u'.cd{}'.format(file_info['cdNumber'])
    if file_info.get('container'):
        file_extension += u'.{}'.format(file_info['container'])

    # Rename and move the movie file.
    os.renames(args.filepath, os.path.join(
        args.movies_dir,
        args.movie_dir_template.format(movie=movie),
        args.movie_file_template.format(movie=movie)
        + file_extension))

if __name__ == '__main__':
    main()
