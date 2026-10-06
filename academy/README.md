# Divine Insight Academy

Learn to read tarot. Lessons, practice spreads, and a reading journal, built on
the same 78-card dataset that powers every other Divine Insight branch.

Academy is the front door of the platform. It brings people in before they want
to pay for a reading, and everything it teaches is grounded in Core data rather
than a separate pile of lesson copy.

## Pinned to Core

```
core.version = v1.5
```

`data/tarot_data_v1.5.json` is a vendored copy of the Core v1.5 release:

https://github.com/mal494/divine-insight-core

Card meanings, keywords, elements, astrology, tags, life domains and position
text all come from Core. See CORE.md for the rules.

## Curriculum

See CURRICULUM.md. Four modules:

1. Foundations - the 78 cards, suits, numerology, reversals
2. Spreads - three-card, Celtic Cross, building your own
3. Practice - draw a card, write your read, compare against Core
4. Journal - saved readings and notes, shared with Web and Mobile

## Why this is cheap to build

Practice mode is the key piece. It reuses Core's `positional_text` and the
Studio scoring engine, so the teaching content is mostly already written. The
work is the lesson framing around it, not a second body of card copy.

## Status

Scaffold. No application code yet.
