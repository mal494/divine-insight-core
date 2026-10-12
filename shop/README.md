# Divine Insight Shop

Decks, merch, and digital goods for the Divine Insight platform.

Shop is where the brand turns physical. It sells the things a reader wants after
a reading: a printed deck, a guidebook, art prints, and digital downloads.

## Core alignment

Shop is planned inside the Core repo right now, so it reads directly from this
repo's versioned dataset files under `data/` (currently `v1.6.1`; see `CHANGELOG.md`).
There is no separate vendored Shop copy of Core data yet.

Product copy for anything card-shaped - a printed deck, a single-card print, a
guidebook - reads card names, numbers, suits and meanings from Core rather than
retyping them. See CORE.md.

## Catalog

See CATALOG.md for the planned lineup and how each product maps to Core.

## Payments

Web already runs Stripe for readings and tips (`mal494/divine-insight-web`).
Shop should reuse the same Stripe account and the same customer
records, so a buyer and a reader are one person on the platform, not two.

## Status

Scaffold. No storefront code yet.
