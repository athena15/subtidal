import os

import click

from subtidal.download import download


@click.command()
@click.argument('directory', default=os.getcwd(), required=True)
# @click.option('--min-size-mb', '-s', type=click.INT,
#               help='Minimum size (in MB) that video files must be for subtitles to be downloaded.')
@click.option('--language', '-l', help=')
@click.option('--verbose', '-v', is_flag=True, help='Prints more output to the console.')
def download_subtitles(directory, verbose=False):
    download(directory, verbose)


if __name__ == '__main__':
    download_subtitles()