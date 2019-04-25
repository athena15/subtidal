import os

import click

from subtidal.download import download


@click.command()
@click.argument('directory', default=os.getcwd(), required=True)
# @click.option('--min-size-mb', '-s', type=click.INT,
#               help='Minimum size (in MB) that video files must be for subtitles to be downloaded.')
@click.option('--verbose', '-v', is_flag=True, help='Prints more output to the console.')
@click.option('--language', '-l', default='eng',
              help='Desired language for subtitles, expressed as a 3-letter ISO-639-3 code. '
                   'Visit https://bit.ly/29fjNpm for a list of language codes.')
def download_subtitles(directory, language, verbose=False):
    download(directory, language, verbose)


if __name__ == '__main__':
    download_subtitles()
