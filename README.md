# Divine Insight Core

The canonical 78-card tarot dataset and schema notes shared by every Divine Insight branch.

Core is the trunk of the platform. Web, Mobile and Studio all consume a versioned
release of this repo rather than keeping their own copy of the card data. This
repo is public so those branches can fetch a release at build time without a token.
Core ships the datasets, schema conventions, planning docs, and
`scripts/validate_tarot_datasets.py`. GitHub Actions runs that script on every
pull request and on every push to `main`.

## What's here

```text
data/
  tarot_data_v1.6.1.json # current dataset (deck 4.6.1, schema 1.6.1)
  tarot_data_v1.6.json   # previous dataset, kept as a backward-compatibility fixture
  tarot_data_v1.5.json   # older dataset, kept as a backward-compatibility fixture
  tarot_data_v1.4.json   # older dataset, kept as a backward-compatibility fixture
explorer/                # static dataset browser (index.html + app.js + styles.css)
art/
  manifest.json          # slug -> artwork basename map for all 78 cards
scripts/
  validate_tarot_datasets.py  # schema, 78-card, and manifest checks for every release
academy/
  CURRICULUM.md          # Academy lesson plan
shop/
  CATALOG.md             # Shop product plan
CHANGELOG.md             # dataset and schema release notes
```

Academy and Shop live here as plans until either has running code of its own.

### Card explorer

`explorer/` is a static browser for the current dataset: no build step. Serve the repo root over HTTP and open `/explorer/`:

```bash
python3 -m http.server 4173
# http://localhost:4173/explorer/
```

Opening `explorer/index.html` as a `file://` URL fails. `fetch` of the dataset is blocked, and the page reports that it could not load the file.

`explorer/app.js` loads one relative path:

```js
var DATASET_PATH = "../data/tarot_data_v1.6.1.json";
```

When a release renames `tarot_data_vX.Y.json`, change `DATASET_PATH` in the same commit. The badge and footer show `deck_metadata.version` and `schema_version` from whatever file loaded.

The page searches name, arcana, suit, element, astrology, `short_description`, and upright and reversed keywords and descriptions. Search input is debounced 160ms. Filters are All, Major Arcana, Wands, Cups, Swords, and Pentacles. Sort is file order or A–Z by name. **Draw a random card** opens one card from the filtered list (`Math.random`). The modal shows number, name, arcana or suit, element, astrology, `short_description`, and upright and reversed keywords and descriptions. Arrow keys move inside the filtered list. Escape or a click on the backdrop closes it. Tags, life domains, positional text, and elemental weight are not shown.

`prefers-reduced-motion: reduce` skips the twinkling canvas and the card-grid stagger. The HTML comment `pages-branch-verify` in `explorer/index.html` is a Pages deploy marker. The script does not read it.

## Validating datasets

`scripts/validate_tarot_datasets.py` checks every `data/tarot_data_v*.json` and `art/manifest.json`. It takes no arguments. GitHub Actions runs it on every pull request and every push to `main` (`.github/workflows/validate-datasets.yml`, Python 3.12). Locally:

```bash
python3 scripts/validate_tarot_datasets.py
```

Exit 0 prints the file count and the versions it saw. Exit 1 prints `Dataset validation failed:` and one bullet per problem. The script needs Python 3.10 or newer (`list[str]`, `Any | None`).

What it requires:

- `data/` contains `tarot_data_v1.4.json`, `v1.5.json`, `v1.6.json`, and `v1.6.1.json`. Any other `tarot_data_v*.json` in that directory is checked too.
- Each file has `deck_metadata`, `taxonomy`, and `cards`. `deck_metadata.schema_version` equals the version in the filename. `total_cards` is 78 and `cards` has 78 objects.
- `art/manifest.json` `cards` has exactly 78 kebab-case slug keys, each with a non-empty asset id. Every dataset's slugs match that set exactly. Duplicate slugs fail.
- Schema 1.6 and 1.6.1 cards must have a non-empty `short_description`. Older files are not required to have that field, and the script does not reject it if they do.
- `id` equals `key`. `arcana` is `Major` or `Minor`. Major cards have `suit: null`, `card_type` `Major Arcana`, and `number` 0–21. Minor cards use suit Wands, Cups, Swords, or Pentacles, `number` 1–14, and `card_type` `Pip Card` (1–10) or `Court Card` (11–14).
- `element` and each `life_domains` entry are in that file's taxonomy. `elemental_weight` is a number. The script does not check that it is between 0 and 1.
- Upright and reversed meanings have a non-empty keyword list and a non-empty description. `positional_weights` and `positional_text` include `past`, `obstacle`, `present`, `future`, `advice`, and `hopes_fears`.

## Schema

Schema 1.6.1 is a data-only patch on 1.6: no card fields change. It swaps the Queen and
King of Wands astrology to the Golden Dawn attributions.

Schema 1.6 adds one card field, `short_description`, and fixes astrology on the court
cards and Aces. Readers that ignore unknown fields load 1.6 unchanged, and v1.5 and
v1.4 files still load against a 1.6 reader (they just lack `short_description`).

Each card carries: key, number, slug, name, `short_description`, arcana, suit, element,
`astrology`, keywords,
upright and reversed meanings, `elemental_weight`, `positional_weights`,
`positional_text`, `tags`, and `life_domains`.

## How branches consume Core

1. Core publishes a tagged release (currently `v1.6.1`) containing the dataset files.
2. Each branch pins a Core version in a `core.version` file and documents the
   dependency in its own `CORE.md`.
3. When Core ships a new version, each branch upgrades deliberately.

No branch edits card data locally. Changes land here first.

## Updating the dataset

1. Add the new `tarot_data_vX.Y.json` under `data/`.
2. Keep the previous version in place as a backward-compatibility fixture.
3. Add the new version to `EXPECTED_DATASET_VERSIONS` in `scripts/validate_tarot_datasets.py` when it should be required, and point `explorer/app.js` `DATASET_PATH` at the file the explorer should open.
4. Run `python3 scripts/validate_tarot_datasets.py`.
5. Record the change in CHANGELOG.md.
6. Tag a release so downstream branches can pin it.

## Branches of the platform

| Branch | Repo | What it is |
| --- | --- | --- |
| Core | mal494/divine-insight-core | this repo: dataset, schema, platform plans |
| Web | mal494/divine-insight-web | browser reading site with Stripe readings and tips |
| Mobile | mal494/divine-insight-mobile | Android app |
| Landing | mal494/divine-insight-landing | public marketing/landing site |
| Studio | mal494/divine-insight-studio | Unity app, data model and scoring engine |
| Academy | `academy/` here | learn to read tarot: lessons, practice, journal |
| Shop | `shop/` here | decks, merch, digital goods |

Arcana Path (mal494/tarot_game) is a sister brand, not a branch.

## License

- Code, scripts, and non-content documentation are under the MIT License
  (`LICENSE`).
- Original card text and dataset content — the files in `data/`, including
  meanings, descriptions, and similar fields — are under CC BY-NC 4.0
  (`LICENSE-CONTENT`). That license is a grant to other people. The copyright
  holder can keep using this text in the paid Web, Mobile, and Studio products.
- Rider-Waite-Smith images (Pamela Colman Smith, 1909) are public-domain source
  material. They are not stored in this repository, and neither MIT nor
  CC BY-NC is a copyright claim on them. `art/manifest.json` only maps a Core
  slug to a filename.

Copyright (c) 2026 Michael Lind.
