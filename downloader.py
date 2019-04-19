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
@click.option('--min_size_mb', '-s', type=click.INT,
              help='Minimum size (in mb) of video file to use to search for subtitles.')
def download_subtitles_for_all_movies_in_directory(directory, min_size_mb=100):
    """
    Takes in a directory path, walks through the file tree, and downloads subtitles for any video files found.
    Renames the subtitle file to match the video's name (in order to make it compatible with Roku Media Player.)

    :param directory: str
    :param min_size_mb: int
    :return: None
    """
    successful = 0
    total = 0
    print('Walking the file tree...')
    for subdir, dirs, files in os.walk(directory):
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
    download_subtitles_for_all_movies_in_directory()
#
# # download_subtitles_for_all_movies_in_directory(os.getcwd())
