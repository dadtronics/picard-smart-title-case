# -*- coding: utf-8 -*-

# Smart Title Case plugin for MusicBrainz Picard (Picard 3.0 format).
#
# Original: Copyright (C) 2017 Sophist.
# Based on the Title Case plugin by Javier Kohen (Copyright 2007).
# Updated for use with Picard v2.0 by Bob Swift (rdswift).
# Ported to the Picard 3.0 (plugins3) format.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import re
import unicodedata

from picard import log

title_tags = ['title', 'album']
artist_tags = [
    ('artist', 'artists'),
    ('artistsort', '~artists_sort'),
    ('albumartist', '~albumartists'),
    ('albumartistsort', '~albumartists_sort'),
    ]
title_re = re.compile(r'\w[^-,/\s\u2010\u2011]*')


def match_word(match):
    word = match.group(0)
    if word == word.lower():
        word = word[0].upper() + word[1:]
    return word


def string_title_match(match_word, string):
    return title_re.sub(match_word, string)


def string_cleanup(string):
    if not string:
        return ""
    return unicodedata.normalize("NFKC", string)


def string_title_case(string):
    """Title-case a string using a less destructive method than str.title.
    >>> string_title_case('make title case')
    'Make Title Case'
    >>> string_title_case('Already Title Case')
    'Already Title Case'
    >>> string_title_case('mIxEd cAsE')
    'mIxEd cAsE'
    >>> string_title_case('a')
    'A'
    >>> string_title_case("apostrophe's apostrophe's")
    "Apostrophe's Apostrophe's"
    >>> string_title_case('(bracketed text)')
    '(Bracketed Text)'
    >>> string_title_case("'single quotes'")
    "'Single Quotes'"
    >>> string_title_case('"double quotes"')
    '"Double Quotes"'
    >>> string_title_case('a,b')
    'A,B'
    >>> string_title_case('a-b')
    'A-B'
    >>> string_title_case('a/b')
    'A/B'
    >>> string_title_case('flügel')
    'Flügel'
    >>> string_title_case('HARVEST STORY by 杉山清貴')
    'HARVEST STORY By 杉山清貴'
    """
    return string_title_match(match_word, string_cleanup(string))


def artist_title_case(text, artists, artists_upper):
    """
    Use the array of artists and the joined string
    to identify artists to make title case
    and the join strings to leave as-is.

    >>> artist_title_case('the beatles feat. the who', ['the beatles', 'the who'], ['The Beatles', 'The Who'])
    'The Beatles feat. The Who'
    >>> artist_title_case('kesha feat. 3OH!3', ['kesha', '3OH!3'], ['Kesha', '3OH!3'])
    'Kesha feat. 3OH!3'
    """
    find = "^(" + r")(\s+\S+?\s+)(".join((map(re.escape, map(string_cleanup, artists)))) + ")(.*$)"
    replace = "".join([r"%s\g<%d>" % (a, x * 2 + 2) for x, a in enumerate(artists_upper)])
    result = re.sub(find, replace, string_cleanup(text))
    return result


def title_case(item, metadata, *args):
    for name in title_tags:
        if name in metadata:
            values = metadata.getall(name)
            new_values = [string_title_case(v) for v in values]
            if values != new_values:
                log.debug("SmartTitleCase: %s: %r replaced with %r", name, values, new_values)
                metadata[name] = new_values
    for artist_string, artists_list in artist_tags:
        if artist_string in metadata and artists_list in metadata:
            artist = metadata.getall(artist_string)
            artists = metadata.getall(artists_list)
            new_artists = list(map(string_title_case, artists))
            new_artist = [artist_title_case(x, artists, new_artists) for x in artist]
            if artists != new_artists and artist != new_artist:
                log.debug("SmartTitleCase: %s: %s replaced with %s", artist_string, artist, new_artist)
                log.debug("SmartTitleCase: %s: %r replaced with %r", artists_list, artists, new_artists)
                metadata[artist_string] = new_artist
                metadata[artists_list] = new_artists
            elif artists != new_artists or artist != new_artist:
                if artists != new_artists:
                    log.warning("SmartTitleCase: %s changed, %s wasn't", artists_list, artist_string)
                    log.warning("SmartTitleCase: %s: %r changed to %r", artists_list, artists, new_artists)
                    log.warning("SmartTitleCase: %s: %r unchanged", artist_string, artist)
                else:
                    log.warning("SmartTitleCase: %s changed, %s wasn't", artist_string, artists_list)
                    log.warning("SmartTitleCase: %s: %r changed to %r", artist_string, artist, new_artist)
                    log.warning("SmartTitleCase: %s: %r unchanged", artists_list, artists)


def enable(api) -> None:
    """Picard 3.0 entry point: register album and track metadata processors."""
    from picard.metadata import album_metadata_processors, track_metadata_processors

    album_metadata_processors.register(__name__, title_case)
    track_metadata_processors.register(__name__, title_case)
    log.info("Smart Title Case: enabled")


def disable() -> None:
    log.info("Smart Title Case: disabled")
