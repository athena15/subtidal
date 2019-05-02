#!/usr/bin/env python3

import os
import re

import click
from babelfish import Language
from subliminal import Video, download_best_subtitles, save_subtitles


def download(directory, language='eng', country=None, verbose=False):
    """
    Takes in a directory path, walks through the file tree, and downloads subtitles for any video files found.
    Renames the subtitle file to match the video's name (in order to make it compatible with Roku Media Player.)

    :param (str) directory: Directory where video files or folders are located.
    :param (str) language : [optional] Desired language for subtitles, expressed as a 3-letter ISO-639-3 code.
                            Visit https://bit.ly/29fjNpm for a list of language codes.
    :param (str) country : [optional] Country code (needed in addition to language code for certain languages).
    :param (bool) verbose : [optional] Prints more output to the console.

    Examples:
    1. download_subtitles('/Users/Laura/Movies')
    2. download_subtitles(directory='./Users/Tim/TV Shows', language='spa', verbose=True)
    """
    successful = 0
    videos = []

    # Walk the file path, identifying video files that do not have a matching .srt (subtitle) file in the same folder.
    # Then collect the file and directory names within list 'videos' that we will iterate over later.
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f'>>> Error: "{directory}" is not a valid directory. Please try again.')
        return False
    print('>>> Walking the file tree...')
    for subdir, dirs, files in os.walk(directory):
        if verbose:
            print(subdir)
        for file in files:
            if file.endswith((".mp4", ".avi", ".mkv")) and not file.startswith('.'):
                movie_title = re.split('.mp4|.avi|.mkv', file)[0]
                if os.path.isfile(str(os.path.join(subdir, movie_title) + '.srt')):
                    continue
                else:
                    videos.append([movie_title, file, subdir])

    # check to see if video files found
    if not videos:
        print('No movie files without subtitles found in folder.')
        return False

    # iterate over 'videos' and download subtitles
    with click.progressbar(videos, label='Searching for subtitles') as bar:
        for movie_title, file, subdir in bar:

            try:
                video = Video.fromname(file)

            except ValueError:
                if verbose:
                    print(f'Could not find a match for file: {file}')
                continue

            try:
                if language and country:
                    lang = Language(language, country)
                else:
                    lang = Language(language)
                os.chdir(subdir)
                best_subtitles = download_best_subtitles([video], {lang},
                                                         providers=['opensubtitles', 'thesubdb',
                                                                    'tvsubtitles'])
                best_subtitle = best_subtitles[video][0]
                save_subtitles(video, [best_subtitle])
                if verbose:
                    print(f'Successfully downloaded subtitle for: {file}')

            except IndexError:
                if verbose:
                    print(f'Subtitles not found online for: {file}')
                continue

            successful += 1

            if language == 'eng':
                try:
                    old_name = str(os.path.join(subdir, movie_title)) + '.en.srt'
                    new_name = str(os.path.join(subdir, movie_title)) + '.srt'
                    if verbose:
                        print(f'Old name: {old_name}')
                        print(f'New name: {new_name}')
                        print(f'Path    : {str(os.path.join(subdir, movie_title))}')
                    os.rename(old_name, new_name)

                except FileNotFoundError:
                    if verbose:
                        print(f"Couldn't rename subtitle file for: {movie_title}.")
                    continue



    print()
    print(f'>>> Finished!')
    print(f'>>> Fetched {successful} / {len(videos)} subtitle files successfully.')
    return


if __name__ == '__main__':
    download(os.getcwd())
