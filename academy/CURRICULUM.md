# Curriculum

Four modules, each building on the one before it. Every lesson pulls its card
facts from Core, so a dataset update improves the lessons automatically.

## Module 1 - Foundations

Goal: a learner can pick up any card and say something true about it without
looking it up.

1. What a tarot deck is - 22 Majors, 56 Minors, why the split matters
2. The four suits - Wands/Fire, Cups/Water, Swords/Air, Pentacles/Earth
3. Numerology - Ace through Ten as a sequence, not fourteen separate facts
4. The court cards - Page, Knight, Queen, King as postures rather than people
5. The Major Arcana as an arc - the Fool's journey, 0 through 21
6. Reversals - using Core's `reversed` meanings without treating them as "bad"

Core fields used: `arcana`, `suit`, `element`, `number`, `meanings.upright`,
`meanings.reversed`.

## Module 2 - Spreads

Goal: a learner can run a reading end to end and explain why each position says
what it says.

1. One card - the daily draw
2. Three cards - past, present, future, and the other three-card framings
3. The five-card Extended spread used on Web
4. Celtic Cross - ten positions, read in pairs
5. Designing a spread - choosing positions that actually ask different questions

Core fields used: `positional_text`, `positional_weights`.

## Module 3 - Practice

Goal: the learner reads first, then compares.

The loop:

1. Academy draws a card into a named position
2. The learner writes their own read in a text box
3. Core's `positional_text` for that card and position is revealed alongside it
4. The learner tags what they missed - imagery, element, number, domain

Nothing is scored as right or wrong. The comparison is the lesson.

Later: run the Studio scoring engine over a learner's full spread to show which
cards carried the most weight and why.

## Module 4 - Journal

Goal: a learner builds a personal record and sees their own patterns.

- Save any reading with the question, the cards, and their own notes
- Revisit a past reading and add what actually happened
- Surface patterns - which cards recur, which life domains dominate
- Shared account with Web and Mobile, so a reading taken anywhere lands here

Core fields used: `life_domains`, `tags`.

## Open questions

- Free in full, or Foundations free and the rest paid?
- Does Academy ship inside the Web app or as its own site at learn.?
- Do journal entries sync from day one, or does Academy start standalone?
