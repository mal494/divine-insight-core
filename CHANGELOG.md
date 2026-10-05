# Changelog

## v1.5 - 2026-10-05

Initial Core release. The 78-card dataset is split out of `mal494/divine-insight-unity`
and becomes the single source of truth for every Divine Insight branch.

- `data/tarot_data_v1.5.json` - deck 4.5, schema 1.5. Adds `deck_metadata.changelog_1_5`;
  card fields unchanged from 1.4. Original position text written for all 78 cards.
- `data/tarot_data_v1.4.json` - deck 4.4, schema 1.4. Retained as a backward-compatibility
  fixture so readers can prove older datasets still load.
