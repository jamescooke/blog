Title: Missing tiny data breaks pipeline
Date: 2024-02-17
Summary: At work, when our usage and revenue reporting pipelines fail, they
    usually fail because of *tiny* data.

This week, during our monthly reporting run, two major label licensing reports
failed validation. This is unexpected because usually all reports are generated
and validate just fine.

It turned out a row of advertising revenue was missed for the United States
Minor Outlying Islands (UMI).

That missed row was worth just £ 0.0003. 🙀

## 👌 This is tiny tiny data

At work (Mixcloud) we generate usage reports for major labels on a monthly
basis. Those reports total thousand of dollars / pounds / euros.

This missing row was "tiny" by many definitions:

* It was a tiny territory that I have to [look up on
  Wikipedia](https://en.wikipedia.org/wiki/United_States_Minor_Outlying_Islands).
  Turns out the population is about 300 people.
* It was a tiny amount of revenue that would get rounded out of existence at
  payout time. It would literally make zero change to the total payout for the
  month to any label.

We often use a 0.1 % sense check definition of edge cases when working out what
bugs and issues to put effort against, and by every definition, this missing
row was less than 0.1 % of all sorts of monthly factors.

## 🔥 But the pipeline failed

A long time ago, I realised that we needed to validate the reports generated
_before_ they were sent to partners. So we built a post-process validation
system. This checks the generated reports from the client perspective,
providing row-wise, file-wise and batch-wise validation.

One of these checks ensures that advertising revenue is reported in GBP £.
However, because we had a missing row for the United States Minor Outlying
Islands (UMI), the reported advertising-based usage row became USD $ and failed
validation.

Under the hood, this happened because we have a `LEFT JOIN` between revenue and
usage which wasn't populated on the revenue side because the UMI row was
missing.

## 🛑 When there's a validation failure, everything stops

When the generated reports with $ 0 amounts of advertising revenue hit our
validators they fail for the partners whose reports contain enough detail to
see that revenue and currency information. Even though this was just two
partners, when we receive those validation errors in the pipeline, the monthly
production stops.

We keep the generated reports, but work to find out the cause of the error and
assess how many generated reports are tainted.

## 🔧 Fix and regenerate

This time the error was, as discussed, tiny. And the fix was pretty tiny too.
We generated an extra row of revenue for UMI worth £ 0.0001 and spliced it back
into our monthly source data snapshots.

Then we reran all partners that receive reports on Mixcloud's ad-funded usage
and our ops colleagues got our monthly production process back up to speed.

## 🤔 Is this kind of behaviour a "good" thing?

After this incident, I'm left wondering if it's OK that our pipeline is halted
by a missing row worth less than a penny that wouldn't affect monthly payouts.

### This is good

On the "good" side, we could say:

> All the main sources of error are stable, it's just the tiny edge cases that
> are failing.

In addition, these failures are so rare that we often are surprised when things
fail. Plus, it's good that we have the validation in place that finds this
kinds of errors and reports them.

### This is bad

On the other hand, we could say:

> The pipelines are so fragile that a tiny missing piece of revenue allocated
> to a user in a territory can bring down a monthly reporting run.

There also seems some truth in this.

Probably the `LEFT JOIN` in our revenue pipeline that caused the USD row to
appear is not robust enough. And as we've dug more into the error later in the
week, my colleague Tim might have found a scenario that we would never be able
to prevent without strengthening this left join.
