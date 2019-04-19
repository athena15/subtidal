#!/usr/bin/env python3

import os
from subliminal import *
from babelfish import *
import re

directory = '/Volumes/Media/'

def download_subtitles_for_all_movies_in_directory(directory):
    """
    Function accepts a directory path, walks through the file tree recursively, and
    downloads subtitles for any video files without a subtitle file in the same folder.
    :param directory:
    :return:
    """

    successful_dls = 0
    total_dls = 0
    print('Walking the file tree...')
    for subdir, dirs, files in os.walk(directory):
        if not [i for i in files if i.endswith('.srt')]:
            for file in files:
                filepath = os.path.join(subdir, file)
                if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
                    if not file.startswith('.') and os.path.getsize(filepath) > 1e8:
                        total_dls += 1
                        movie_title = re.split('.avi|.mp4|.mkv', file)[0]

                        try:
                            video = Video.fromname(file)
                        except ValueError:
                            continue

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

                        except Error:
                            print("Couldn't rename file.")
                            break

                        successful_dls += 1

    print()
    print(f'>>> Finished!')
    print(f'>>> Fetched {successful_dls} / {total_dls} subtitle files successfully.')





download_subtitles_for_all_movies_in_directory(directory)

if __name__ == '__main__':
    # directory = input('Enter path of folder to get subtitles for (or drag and drop into Terminal): ')

    download_subtitles_for_all_movies_in_directory(directory)