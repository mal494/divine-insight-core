# Divine Insight Core

The canonical 78-card tarot dataset and schema notes shared by every Divine Insight branch.

Core is the trunk of the platform. Web, Mobile and Studio all consume a versioned
release of this repo rather than keeping their own copy of the card data. This
repo is public so those branches can fetch a release at build time without a token.
Core currently ships datasets, schema conventions, and planning docs; it does not
yet include standalone validation tooling.

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
academy/
  CURRICULUM.md          # Academy lesson plan
shop/
  CATALOG.md             # Shop product plan
CHANGELOG.md             # dataset and schema release notes
```

Academy and Shop live here as plans until either has running code of its own.

### Serving the explorer locally

The explorer reads `../data/tarot_data_v1.6.1.json`, so serve the repo root over HTTP:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173/explorer/`.

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
3. Record the change in CHANGELOG.md.
4. Tag a release so downstream branches can pin it.

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

TBD (pending Michael's decision).
