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
$ tit 'Black Hawk Down 2001.720p.x264.BRRip.GokU61.mp4'
http://www.titulky.com/Black-Hawk-Down-62960.htm
```


### Interactive Mode

You can also run `tit` interactively:

```shell
$ tit
  1: Black Hawk Down 2001.720p.x264.BRRip.GokU61.mp4
  2: Trhak-1980-DVDRip-cz.avi
Which video file? [1]:

  1: Černý jestřáb sestřelen - http://www.csfd.cz/film/8266-cerny-jestrab-sestrelen/
  2: Essence of Combat: Making 'Black Hawk Down', The - http://www.csfd.cz/film/132778-essence-of-combat-making-black-hawk-down-the/
  3: Black Mass: Špinavá hra - http://www.csfd.cz/film/283586-black-mass-spinava-hra/
  4: Černé duše - http://www.csfd.cz/film/385471-cerne-duse/
  5: Hádej kdo? - http://www.csfd.cz/film/181145-hadej-kdo/
Which film? [1]:

http://www.titulky.com/Black-Hawk-Down-62960.htm
```


### Extra Options

- `--open` - Automatically opens all links in your default browser.
- `--csfd=<link or film ID>` - Specify correct [CSFD.cz](http://www.csfd.cz/) link.


## Name

The name is obviously taken from the beginning of the word *titulky.com*, but
it is also a [family of small birds](https://en.wikipedia.org/wiki/Tit_%28bird%29),
quite [popularized by Monty Python](https://www.youtube.com/watch?v=YQ7Tak6fK9w).
