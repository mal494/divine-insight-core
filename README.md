# Divine Insight Core

The canonical 78-card tarot dataset and schema shared by every Divine Insight branch.

Core is the trunk of the platform. Web, Mobile, Studio, and Academy all consume a
versioned release of this repo rather than keeping their own copy of the card data.

## What's here

```
data/
  tarot_data_v1.5.json   # current dataset (deck 4.5, schema 1.5)
  tarot_data_v1.4.json   # previous dataset, kept as a backward-compatibility fixture
```

## Schema

Schema 1.5 adds `deck_metadata.changelog_1_5`. Card fields are unchanged from 1.4,
so v1.4 files still load against a 1.5 reader.

Each card carries: key, number, slug, name, arcana, suit, element, keywords,
upright and reversed meanings, `elemental_weight`, `positional_weights`,
`positional_text`, `tags`, and `life_domains`.

## How branches consume Core

1. Core publishes a tagged release (for example `v1.5`) containing the dataset files.
2. Each branch pins a Core version and vendors or fetches that release.
3. When Core ships a new version, each branch upgrades deliberately.

No branch edits card data locally. Changes land here first.

## Updating the dataset

1. Add the new `tarot_data_vX.Y.json` under `data/`.
2. Keep the previous version in place as a backward-compatibility fixture.
3. Record the change in CHANGELOG.md.
4. Tag a release so downstream branches can pin it.

## Branches of the platform

| Branch | What it is |
| --- | --- |
| Core | this repo: dataset, schema, validation |
| Web | browser reading site with Stripe readings and tips |
| Mobile | Android app |
| Studio | Unity app, data model and scoring engine |
| Shop | decks, merch, digital goods |
| Academy | learn to read tarot: lessons, practice, journal |
