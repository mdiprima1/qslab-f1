# QSLab Unit 1.2 — Additional Exploration Prompts

Paste any one of these into Claude Code after completing the main lab.
All prompts stay within the scope of Unit 1.2.

---

## Prompt A — What the numbers actually mean

"Look at the stats from step 6. Walk me through what each number is
telling me in plain English. Explain the regime changes count, the
time in market percentage, and the spread between the latest close
and the SMA. What would it mean if the spread were much larger?
What if it were negative?"

---

## Prompt B — What changes with a different MA period?

"Without running any new code, explain what would happen to the
buy and cash zones if we used a 50-day SMA instead of 100-day.
Would there be more or fewer regime changes? More or less time
in the market? What is the tradeoff between a shorter and longer
moving average period?"

Note to Claude Code: Conceptual only. No new code. No parameter changes.
Remind the student that testing different periods is covered in a later module.

---

## Prompt C — What this chart cannot tell us

"The regime chart looks convincing in some places and wrong in others.
Walk me through what the chart cannot tell us. What would we need to
know before deciding whether this strategy is worth using? What are
the three biggest things missing from what we built today?"

Note to Claude Code: Reflection question only. No new analysis.
Guide toward: 1) no transaction costs, 2) no statistical validation,
3) no out-of-sample test. Do not introduce concepts beyond Unit 1.2 scope.
