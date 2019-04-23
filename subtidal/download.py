import os
import re

import click
from babelfish import Language
from subliminal import Video, download_best_subtitles, save_subtitles
from tqdm import tqdm


def download(directory, verbose=False):
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
    videos = []

    # Walk the file path, identifying video files that do not have a .srt (subtitle) file in the same folder.
    # Then collect the file and directory names within list 'videos' that we will iterate over later.
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f'>>> Error: "{directory}" is not a valid directory. Please try again.')
        return 0
    print('>>> Walking the file tree...')
    for subdir, dirs, files in os.walk(directory):
        if verbose:
            print(subdir)
        if not [i for i in files if i.endswith('.srt')]:
            for file in files:
                if file.endswith((".mp4", ".avi", ".mkv")):
                    # file_path = os.path.join(subdir, file)
                    if not file.startswith('.'):  # and os.path.getsize(file_path) > min_size_mb * 1e6:
                        videos.append([file, subdir])

    # check to see if video files found
    if not videos:
        if verbose:
            print('No movie files found in folder.')
        return 0

    # iterate over 'videos' and download subtitles
    print('>>> Downloading subtitles...')
    for file, subdir in tqdm(videos):

        try:
            video = Video.fromname(file)

        except ValueError:
            if verbose:
                print(f'Could not find a match for file: {file}')
            continue

        try:
            os.chdir(subdir)
            best_subtitles = download_best_subtitles([video], {Language('eng')},
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

        try:
            movie_title = re.split('.avi|.mp4|.mkv', file)[0]
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
            break

        successful += 1

    print()
    print(f'>>> Finished!')
    print(f'>>> Fetched {successful} / {len(videos)} subtitle files successfully.')
    return


@click.command()
@click.argument('directory', default=os.getcwd(), required=True)
# @click.option('--min-size-mb', '-s', type=click.INT,
#               help='Minimum size (in MB) that video files must be for subtitles to be downloaded.')
@click.option('--verbose', '-v', is_flag=True, help='Prints more output to the console.')
def download_subtitles(directory, verbose=False):
    download(directory, verbose)



if __name__ == '__main__':
    # download_subtitles()
    # download('/Volumes/Media/', verbose=True)
    print(os.getcwd())
    download('/Users/brennerheintz/Movies/', verbose=True)
