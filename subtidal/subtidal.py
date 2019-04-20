#!/usr/bin/env python3
import os
import re

import click
from babelfish import Language
from subliminal import Video, download_best_subtitles, save_subtitles


# # modify as needed
# directory = '/Volumes/Media/'
# min_filesize_in_mb = 100 # set minimum file size to avoid finding subtitles for sample clips, etc.

@click.command()
@click.argument('directory', default=os.getcwd(), required=True)
@click.option('--min-size-mb', '-s', type=click.INT,
              help='Minimum size (in MB) that video files must be for subtitles to be downloaded.')
@click.option('--verbose', '-v', is_flag=True, help='Prints more output to the console.')
def download_subtitles(directory, min_size_mb=100, verbose=False):
    """
    Takes in a directory path, walks through the file tree, and downloads subtitles for any video files found.
    Renames the subtitle file to match the video's name (in order to make it compatible with Roku Media Player.)

    :param str directory: Directory where video files or folders are located.
    :param int min_size_mb: [optional] Minimum size (in MB) that video files must be for subtitles to be downloaded.
    :param bool verbose: bool [optional] Prints more output to the console.

    Examples:
    1. download_subtitles('./Users/Laura/Movies')
    2. download_subtitles(directory='./Users/Tim/TV Shows', min_size_mb=250, verbose=True)
    """
    successful = 0
    total = 0
    print('Walking the file tree...')
    for subdir, dirs, files in os.walk(directory):
        if verbose:
            print(subdir)
        if not [i for i in files if i.endswith('.srt')]:
            for file in files:
                if file.endswith((".mp4", ".avi", ".mkv")):
                    file_path = os.path.join(subdir, file)
                    if not file.startswith('.') and os.path.getsize(file_path) > min_size_mb * 1e6:
                        total += 1
                        movie_title = re.split('.avi|.mp4|.mkv', file)[0]

                        try:
                            video = Video.fromname(file)

                        except ValueError:
                            break

                        try:
                            os.chdir(subdir)
                            best_subtitles = download_best_subtitles([video], {Language('eng')},
                                                                     providers=['opensubtitles', 'thesubdb','tvsubtitles'])
                            best_subtitle = best_subtitles[video][0]
                            save_subtitles(video, [best_subtitle])
                            print(f'Successfully downloaded subtitle for: {movie_title}')

                        except IndexError:
                            print(f'Unable to download subtitle for: {movie_title}')
                            break

                        try:
                            old_name = str(os.path.join(subdir, movie_title)) + '.en.srt'
                            new_name = str(os.path.join(subdir, movie_title)) + '.srt'
                            os.rename(old_name, new_name)

                        except FileNotFoundError:
                            print(f"Couldn't rename subtitle file for: {movie_title}.")
                            break

                        successful += 1

    print()
    print(f'>>> Finished!')
    print(f'>>> Fetched {successful} / {total} subtitle files successfully.')


if __name__ == '__main__':
    download_subtitles()
