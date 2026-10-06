# Changelog

## v1.6 - 2026-10-06

Folds the useful parts of the older Divine Insight Dictionary 2.0 (from `mal494/tarot_game`)
into Core so Arcana Path can consume Core like every other branch.

- `data/tarot_data_v1.6.json` - deck 4.6, schema 1.6. Adds `deck_metadata.changelog_1_6`.
- Astrology fixed on 20 cards. All 16 court cards held their element pair (e.g. `Air/Fire`)
  in `astrology`. Wands, Swords and Pentacles courts are restored from the Dictionary; the Cups
  courts use Golden Dawn attributions (Page: Water Signs, Knight: Pisces, Queen: Cancer,
  King: Scorpio). The four Aces now list their three signs instead of `<Element> Signs`.
- Tags merged with the Dictionary tag lists: 87 tags added across 50 cards, lowercased,
  de-duplicated, ASCII hyphens. No existing tag removed.
- New card field `short_description`: a one-line summary for lists and tooltips. 74 from the
  Dictionary; the four Cups court cards are newly written.
- `data/tarot_data_v1.5.json` is retained as a backward-compatibility fixture. Readers that
  ignore unknown fields load v1.6 unchanged.

## v1.5 - 2026-10-05

Initial Core release. The 78-card dataset is split out of `mal494/divine-insight-unity`
and becomes the single source of truth for every Divine Insight branch.

- `data/tarot_data_v1.5.json` - deck 4.5, schema 1.5. Adds `deck_metadata.changelog_1_5`;
  card fields unchanged from 1.4. Original position text written for all 78 cards.
- `data/tarot_data_v1.4.json` - deck 4.4, schema 1.4. Retained as a backward-compatibility
  fixture so readers can prove older datasets still load.
