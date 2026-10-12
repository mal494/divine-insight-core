# Divine Insight Core

The canonical 78-card tarot dataset and schema shared by every Divine Insight branch.

Core is the trunk of the platform. Web, Mobile and Studio all consume a versioned
release of this repo rather than keeping their own copy of the card data. This
repo is public so those branches can fetch a release at build time without a token.

## What's here

```text
data/
  tarot_data_v1.6.1.json # current dataset (deck 4.6.1, schema 1.6.1)
  tarot_data_v1.6.json   # previous dataset, kept as a backward-compatibility fixture
  tarot_data_v1.5.json   # older dataset, kept as a backward-compatibility fixture
  tarot_data_v1.4.json   # older dataset, kept as a backward-compatibility fixture
explorer/                # static card browser (GitHub Pages)
academy/                 # Academy plan: curriculum for learning to read tarot
shop/                    # Shop plan: decks, merch and digital goods
art/                     # artwork filename map (images live outside this repo)
```

Academy and Shop live here as plans until either has running code of its own.
The card explorer is a static page over the dataset; see below.

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

## Card explorer

`explorer/` is a static browser for the 78-card dataset: no build step and no
dependencies. GitHub Pages serves it at
`https://mal494.github.io/divine-insight-core/explorer/` (the landing page
links there). Locally, serve the repo root and open `/explorer/`:

```bash
python3 -m http.server 8080
# http://localhost:8080/explorer/
```

Opening `explorer/index.html` via `file://` fails. `fetch` of the dataset is
blocked, and the page says it could not load the file.

`explorer/app.js` loads a relative path:

```js
var DATASET_PATH = "../data/tarot_data_v1.6.1.json";
```

That file has to stay in sync with the current dataset name. When a release
renames `tarot_data_vX.Y.json`, bump `DATASET_PATH` in the same change. The
badge and footer read `deck_metadata.version` and `schema_version` from
whatever file loaded.

What the page does:

- Search matches name, arcana, suit, element, astrology, `short_description`,
  and upright and reversed keywords and descriptions. Input is debounced 160ms.
- Filters: All, Major Arcana, Wands, Cups, Swords, Pentacles.
- Sort: deck order (file order) or A–Z by name.
- **Draw a random card** opens the detail modal for one card in the *filtered*
  list, using `Math.random`.
- The modal shows number, name, arcana or suit, element, astrology,
  `short_description`, and upright and reversed keywords and descriptions.
  Arrow keys and the on-screen arrows move within the filtered list. Escape
  or a click on the backdrop closes it.
- It does not show tags, life domains, positional text, or elemental weight.

`prefers-reduced-motion: reduce` skips the twinkling canvas and the card-grid
stagger. The HTML comment `pages-branch-verify` in `explorer/index.html` is a
Pages deploy marker. The script does not read it.

## How branches consume Core

1. Core publishes a tagged release (currently `v1.6.1`) containing the dataset files.
2. Each branch pins a Core version in a `core.version` file and documents the
   dependency in its own `CORE.md`.
3. When Core ships a new version, each branch upgrades deliberately.

No branch edits card data locally. Changes land here first.

## Updating the dataset

1. Add the new `tarot_data_vX.Y.json` under `data/`.
2. Keep the previous version in place as a backward-compatibility fixture.
3. Record the change in CHANGELOG.md.
4. Tag a release so downstream branches can pin it.

## Branches of the platform

| Branch | Repo | What it is |
| --- | --- | --- |
| Core | mal494/divine-insight-core | this repo: dataset, schema, platform plans |
| Web | mal494/divine-insight-web | browser reading site with Stripe readings and tips |
| Mobile | mal494/divine-insight-mobile | Android app |
| Studio | mal494/divine-insight-studio | Unity app, data model and scoring engine |
| Academy | `academy/` here | learn to read tarot: lessons, practice, journal |
| Shop | `shop/` here | decks, merch, digital goods |

Arcana Path (mal494/tarot_game) is a sister brand, not a branch.
