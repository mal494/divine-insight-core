# Card artwork

The Rider-Waite-Smith deck (Pamela Colman Smith, 1909) is public domain and is
the platform's artwork source. The images themselves are not committed here yet;
they live in Drive under `rider-waite/` in three sizes:

```
full/    high-res JPG, ~3 MB per card - print and Shop products
720px/   ~300 KB per card - web and app faces
gif/     animated variants
```

Plus two deck backs: `Cover` and `Cover_Rare`.

## manifest.json

The art filenames do not match Core slugs: majors are `00_Fool`, minors are
`Wands01` through `Pents14`, and Pentacles is abbreviated `Pents`. `manifest.json`
maps every Core slug to its artwork basename, so a branch never hardcodes that
naming:

```json
"the-fool": "00_Fool",
"ace-of-pentacles": "Pents01",
"king-of-swords": "Swords14"
```

All 78 slugs map to a unique file, verified against the dataset.

## Using it

Web expects `/public/cards/<slug>.webp`. The conversion step is: take `720px/<basename>.jpg`
from the manifest, convert to WebP, write it out named by slug. That replaces the
glyph placeholders the site currently renders for most cards.

Shop's printable deck and guidebook PDF should pull from `full/` instead.

## Attribution

Artist: Pamela Colman Smith (1878-1951). Designer: Arthur Edward Waite.
Publisher: Rider & Company, 1909. Public domain; source Wikimedia Commons.
Credit Smith by name wherever the art is shown or sold - she was uncredited
and underpaid in her lifetime, and it costs nothing to do right by her.
