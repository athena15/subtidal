# subtidal

*A command line utility for **batch downloading subtitles for all movies organized in a central media folder.***

Walks the file tree, visiting subfolders and downloading subtitles for each movie if they do not already exist.

Changes subtitle names so that they are automatically recognized by Roku Media Player, VLC, and others.

Makes quick work of central media folders and entire hard drives alike. Ideally, your central media folder will be organized as a repository of folders, with one movie or TV show each, but subtidal will still work if they're not quite that tidy.

***Motivation***

This is a personal project, but I hope it is of use to you. I got frustrated (or rather, was very mildly inconvenienced) because some of the movies I downloaded online didn't come included with subtitles, and I had to download them myself from sites like [opensubtitles.org](https://opensubtitles.org). Furthermore, even when subtitles were included with a movie, if the filename differed at all from the name of the movie, they weren't recognized by the Roku Media Player, so I set about to rectify that.

I have a huge, network-attached-storage media folder that acts as the central repository for all of the movies I download online, and I wanted to create a package that could download missing subtitles for every movie in it in one fell swoop. 

I imagined that as I downloaded new movies and TV shows into this central repository, I'd be able to run the package periodically via a cron job on my Raspberry Pi, so I'd never have to suffer the loathsome indignity of watching a show without having subtitles available ever again. This package is my attempt to make that vision a reality (or to make some fun out of laziness, depending on how you look at it), and in so doing, make a package available to the public on PyPI, which I had never done before.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install subtidal. From the command line:

```bash
pip install subtidal
```

## Quickstart
*Option 1: From the command line*

```bash
download-subtitles '/path/to/Your Movie Folder'
```
or: 
```bash
cd subtidal
python3 subtidal.py "/path/to/Your Movie Folder"
```

*Option 2: From Python*

```python
from subtidal.download import download_subtitles

# path only
download_subtitles("./path/to/Your Movie Folder")

# path + optional parameters
download_subtitles(directory="./path/to/Your Movie Folder", min_size_mb=100, verbose=True)
```

### Additional function & parameter info in the docstring
```python
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
```


## Contributing
Pull requests are welcome! Take the ball and run with it, kiddo.

## License
[MIT](https://choosealicense.com/licenses/mit/)