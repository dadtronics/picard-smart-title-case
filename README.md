# Smart Title Case (Picard 3.0)

MusicBrainz Picard plugin that capitalizes the first character of every
word in album/track titles and artist names.

- Leaves words containing embedded uppercase as-is, e.g. `USA` or `DoA`.
- For artist/albumartist, title-cases only the artists and leaves join
  phrases untouched, e.g. `The Beatles feat. The Who`.

Original plugin: **Sophist** (2017), based on an earlier plugin by
**Javier Kohen** (2007); updated for Picard 2.0 by **Bob Swift (rdswift)**.
This repository is a faithful port to the Picard 3.0 plugin format
(`title_case()` logic is unchanged; only the registration/entry point
was updated).

## Install (Picard 3.x)

Option A — let Picard do it (GUI: Options → Plugins → "Install from URL",
or CLI):

```
picard-cli plugins install https://github.com/dadtronics/picard-smart-title-case
```

Option B — clone into the plugins directory:

```
git clone https://github.com/dadtronics/picard-smart-title-case "%APPDATA%/MusicBrainz/Picard/plugins3/smart_title_case"
```

(Delete the `.git` folder inside afterwards if you like.)

Then enable the plugin (Options → Plugins, or `picard-cli plugins enable`).

## Notes

- Runs as both an album- and track-level metadata processor, so it
  applies to album titles/album artists and track titles/artists.
- Changes are in-memory until you save the tags.

## License

GPL-2.0-or-later. See `LICENSE`.
