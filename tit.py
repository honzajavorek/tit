
import os
import re

import sh
import click
import requests
from lxml import html


@click.command()
@click.argument('filename', required=False, type=click.Path(exists=True))
@click.option('--csfd', help='Specify correct CSFD.cz link.')
@click.option('--open/--no-open', default=False, help='Open subtitles in browser.')  # noqa
@click.version_option()
def cli(filename, csfd, open):
    """Finds titulky.com subtitles for given file."""
    if csfd:
        csfd_link = parse_csfd(csfd)
        film = {'url': csfd_link, 'name': get_film_name(csfd_link)}
    else:
        film = None

    if filename:
        urls = automatic_mode(filename, film=film)
    else:
        urls = interactive_mode(film=film)

    for url in urls:
        click.echo(url)
        if open:
            click.launch(url)


def automatic_mode(filename, film=None):
    basename = os.path.basename(filename)

    if not film:
        try:
            # take first search result
            film = next(search_film(basename))
        except StopIteration:
            raise click.ClickException(
                'Could not find corresponding CSFD.cz film. ' +
                'Try --csfd or interactive mode.'
            )

    return find_subtitles(film, basename)


def interactive_mode(film=None):
    filenames = find_video_files(os.getcwd())
    basenames = [os.path.basename(filename) for filename in filenames]
    if basenames:
        choices = list(zip(basenames, basenames))
        basename = prompt_choices('Which video file?', choices)
    else:
        raise click.ClickException(
            'No video file given in argument. ' +
            'No video files found in current working directory.'
        )

    if not film:
        choices = [
            ('{name} - {url}'.format(**found_film), found_film)
            for found_film in search_film(basename)
        ]
        film = prompt_choices('Which film?', choices[:5])

    return find_subtitles(film, basename)


def search_film(term):
    """
    Searches given term on CSFD.cz and generates {name, url} dictionaries
    for every search result.
    """
    html_tree = get_html_tree('http://www.csfd.cz/hledat/', params={'q': term})
    for search_result in html_tree.cssselect('#search-films a.film'):
        yield {
            'name': search_result.text_content().strip(),
            'url': search_result.get('href'),
        }


def get_film_name(url):
    """Requests given film URL (CSFD.cz) and returns name of the film."""
    html_tree = get_html_tree(url)
    return html_tree.cssselect('.info h1')[0].text_content().strip()


def find_subtitles(film, basename):
    """
    Finds suitable subtitles for given film and video file basename. The film
    is expected as {name, url} dictionary.
    """
    return [
        found_film['url'] for found_film
        in filter_subtitles(search_subtitles(film), basename)
    ]


def filter_subtitles(subtitles_list, basename):
    """
    Takes iterable of subtitles ({name, url} dictionaries) and filters out
    just those which might be suitable for given video file basename.
    """
    for subtitles in subtitles_list:
        res = requests.get(subtitles['url'])
        res.raise_for_status()

        # Very simple filtering. If the video file basename is mentioned on
        # the page, it's valid result. More sophisticated algorithm may be
        # employed in the future.
        if basename in res.text:
            yield subtitles


def search_subtitles(film):
    """
    Searches titulky.com for subtitles for given film. The film is expected
    as {name, url} dictionary. Yields subtitles in form of {name, url}
    dictionaries.
    """
    search_params = {'Fulltext': film['name']}
    html_tree = get_html_tree('http://www.titulky.com', params=search_params)
    rows = html_tree.cssselect('[id="contcont"] tr')

    header_row = [
        cell.text_content().strip().lower() for cell
        in rows[0].cssselect('td')
    ]
    regular_rows = rows[1:]

    for row in regular_rows:
        cells = [cell for cell in row.cssselect('td')]
        mapped_cells = dict(zip(header_row, cells))

        cd_count = int(mapped_cells['cd'].text_content().strip() or '1')
        if cd_count > 1:
            # Nobody uses CDs these days, all films are just one file.
            # Filtering them out at once.
            continue

        yield {
            'name': mapped_cells['název'].text_content().strip(),
            'url': mapped_cells['název'].cssselect('[href]')[0].get('href'),
        }


def find_video_files(dir):
    """
    Looks into given directory and returns filenames of all present video
    files, sorted from the largest one to the smallest one.
    """
    filenames = (os.path.join(dir, basename) for basename in os.listdir(dir))
    video_filenames = filter(is_video_file, filenames)
    return sorted(
        video_filenames,
        key=lambda file: os.stat(file).st_size,
        reverse=True
    )


def is_video_file(filename):
    """
    Determines whether given filename is video file or not. Uses UNIX
    utility called ``file`` (no Win support, sorry, Pull Requests welcomed).
    """
    result = sh.file(filename, mime=True)
    mime_type = result.replace('{}: '.format(filename), '')
    return 'video/' in mime_type


def parse_csfd(csfd):
    """
    Takes value of the ``--csfd`` option, parses it and returns CSFD.cz URL.
    """
    try:
        csfd_id = int(csfd)
    except (TypeError, ValueError):
        match = re.search(r'/film/(\d+)', csfd)
        if not match:
            raise ValueError('Invalid CSFD.cz link or ID: ' + csfd)
        csfd_id = int(match.group(1))
    return 'https://www.csfd.cz/film/{}/'.format(csfd_id)


def prompt_choices(prompt, choices):
    """
    Prompts user for given choices. Prompt is the prompt string, choices are
    expected as list of (label, value) tuples. Returns selected value. Does
    not prompt in case there is no or just one option.
    """
    if not choices:
        return None
    if len(choices) == 1:
        return choices[0][1]

    first = 1
    for n, (name, value) in enumerate(choices, start=first):
        click.echo('{: 3d}: {}'.format(n, name))

    answer_type = click.IntRange(min=first, max=n)
    answer = click.prompt(prompt, default=first, type=answer_type)
    click.echo('')  # new line

    # 1 is index of 'value' in the choice tuple.
    return choices[answer - first][1]


def get_html_tree(url, **kwargs):
    """Requests given URL and returns HTML DOM tree."""
    res = requests.get(url, **kwargs)
    res.raise_for_status()
    html_tree = html.fromstring(res.content)
    html_tree.make_links_absolute(res.url)
    return html_tree
