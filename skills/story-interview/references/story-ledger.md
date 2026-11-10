# Story ledger and notes format

One file per story and date. Quote the author's words; paraphrase only in the
restated ledger, where each step cites the quotation it rests on.

```
# <story>: story notes (<date>)

Medium and audience: <talk 30 min; listeners know …; should keep …>

## The line (author's words)
1. "<quote>"
2. "<quote>"

## Ledger
| # | Question / step | Answer | Why it matters | Resting on |
|---|---|---|---|---|

## Decisions
- Resolved: <challenge> -> <what settled it>
- Cut: <item> — <reason>
- Kept despite challenge: <item> — <author's reason>

## Open questions (author decides whether to answer)
- <challenge, quoted passage, what would resolve it>

## Parked
- <challenge> — <why deferred>, return when <condition>

## To verify / materials to prepare
- <claim> — <source to check>; <example or figure needed>
```

## Fictional example

Talk, 20 minutes, audience of graph theorists who know spectra but not the
author's new invariant.

Author's line: "Ranking vertices by cycle structure gives a total preorder
that spectral ranking misses." Challenges raised in order:

1. *Concretize*: "'Misses' — name two graphs the spectral ranking ties that
   yours separates." Author supplies a pair; ledger step 3 gets the example.
2. *Gap*: "From 'cycle structure' to 'preorder' you skip why comparability is
   transitive." Author states a lemma; marked *to verify*.
3. *Cut*: "The general definition of weighted hypergraph is not used after
   slide 4." Author cuts it and keeps the graph case.
4. *Significance*: parked; the author wants to think about which application
   the audience cares about.

The notes end with the four items: one resolved, one verified later, one cut,
one parked.
