# Divine Insight Shop

Decks, merch, and digital goods for the Divine Insight platform.

Shop is where the brand turns physical. It sells the things a reader wants after
a reading: a printed deck, a guidebook, art prints, and digital downloads.

## Pinned to Core

```
core.version = v1.5
```

`data/tarot_data_v1.5.json` is a vendored copy of the Core v1.5 release:

https://github.com/mal494/divine-insight-core

Product copy for anything card-shaped - a printed deck, a single-card print, a
guidebook - reads card names, numbers, suits and meanings from Core rather than
retyping them. See CORE.md.

## Catalog

See CATALOG.md for the planned lineup and how each product maps to Core.

## Payments

Web already runs Stripe for readings and tips (`src/lib/payments.ts` in
mal494/DI). Shop should reuse the same Stripe account and the same customer
records, so a buyer and a reader are one person on the platform, not two.

## Status

Scaffold. No storefront code yet.
