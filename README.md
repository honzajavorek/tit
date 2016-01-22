# tit

Better [titulky.com](http://www.titulky.com/) search.


## Installation

```shell
$ pip install tit
```


## Usage

Just run `tit` with the video file. It will output links to results
of titulky.com search, but only those, which look like they **could** fit
to your version of the video.

```shell
$ tit 'Peaceful.Warrior[2006]DvDrip[Eng]-aXXo.avi'
http://www.titulky.com/Peaceful-Warrior-72671.htm
http://www.titulky.com/Peaceful-Warrior-88676.htm
http://www.titulky.com/Peaceful-Warrior-88677.htm
```


### Extra Options

- `--all` - Avoids smart filtering.
- `--csfd=<link or film ID>` - Specify correct ČSFD link.
- `--help` - Displays help.
- `--open` - Automatically opens all links in your preferred browser.
- `--version` - Displays version of your `tit`.


### Interactive Mode

You can also run `tit` interactively:

```shell
$ tit
[o] Peaceful.Warrior[2006]DvDrip[Eng]-aXXo.avi
[ ] sample.MOV

[o] http://www.csfd.cz/film/222209-pokojny-bojovnik/
[ ] http://www.csfd.cz/film/55326-peaceful-alley/
[ ] http://www.csfd.cz/film/239341-peaceful-neighbors/
[ ] http://www.csfd.cz/film/181372-peaceful-oblivion/

http://www.titulky.com/Peaceful-Warrior-72671.htm
http://www.titulky.com/Peaceful-Warrior-88676.htm
http://www.titulky.com/Peaceful-Warrior-88677.htm
Open in browser? [Y/n]
```


## Name

The name is obviously taken from the beginning of the word *titulky.com*, but
it is also a [family of small birds](https://en.wikipedia.org/wiki/Tit_%28bird%29),
quite [popularized by Monty Python](https://www.youtube.com/watch?v=YQ7Tak6fK9w).
