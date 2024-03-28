Title: Why isn't the UK in DST yet?!
Date: 2024-03-28
Tags: language:python, topic:dst
Summary: British Summer Time is due to start this weekend. However, for some
    reason, it's three weeks after the usual USA switch over, rather than the
    usual two. Why is this? And when will it happen again?

> Warning: I particularly hate Daylight Savings Time (DST), so this post is
> tainted with negativity. However, I work hard to prepare myself and family
> for the biannual time change, so this post explores how I set my mental model
> up for the clocks going forwards in the UK.

It's 28th March as I write this from the UK.

The UK _should_ have moved to DST according to my mental model. This should
have happened last weekend.

I even did some family sleep time prepping last weekend. I even [wrongly tooted
about it](https://fosstodon.org/@underlap/112145880071901460) and [then
corrected myself](https://fosstodon.org/@jamescooke/112145934698147675).

All of this has happened because my mental model about DST in the UK is
**WRONG** 🤦.

## 🇺🇸 USA and 🇨🇦 Canada

Canada is a country that I like - some of our friends and family live there and
I've visited multiple times. I also like the USA - I've worked for USA
companies and have visited multiple times.

All this means (I think) I'm well connected to what timezone the USA and Canada
are on any particular day. So when they move to DST (which happens before the
UK and Europe's change), we get a brief couple of weeks where: 

* We get more overlap with family and friends in Canada because their summer
  time is closer by 1 hour to GMT.
* As an NHL ice hockey follower, most games start at midnight UK time, but for
  this period, games start an hour earlier.

Let's call this period the "1 hour closer overlap".

## 🧠 Mental model

My mental model is based off this "1 hour closer overlap". In my head this
overlap lasts two weeks - I don't know why - I've just programmed that as a
"fact".

Therefore, my mental model for:

> When does the UK apply DST and switch from GMT?

Is...

> Two weeks after North America changes to DST.

**This can be WRONG** (sometimes).

This year, 2024, is one of those wrong years.

## ⚠️ The problem

I didn't realise how ingrained this two week duration of overlap was in me, so
let's check facts and find out if I need an upgrade.

### First fact

UK's biannual switch to DST happens on [the last Sunday in
March](https://en.wikipedia.org/wiki/British_Summer_Time):

> \[In the UK\] BST begins at 01:00 GMT every year on the last Sunday of March

### Second fact

North America's biannual switch to DST happens on [the second Sunday in
March](https://en.wikipedia.org/wiki/Daylight_saving_time_in_the_United_States)

> In the U.S., daylight saving time starts on the second Sunday in March

### 🚨 Calendar Siren! 🚨

For any months of March where the last Sunday happens in the fifth week of
March, the "1 hour closer overlap" will be three weeks long, not two.

## 📅 Checking future overlaps

In order to have a look at what the 'normal' overlap looks like, I'm going to
brute force the calculation of how many days the "1 hour closer overlap" lasts
for each year from 2014 to 2033 inclusive.

I'm going to use Python with the `rrule()` from
[dateutil](https://dateutil.readthedocs.io/en/stable/rrule.html) and stuff the
data inside a [Pandas
DataFrame](https://pandas.pydata.org/pandas-docs/stable/index.html).

```py
In [1]: import datetime

In [2]: import pandas as pd

In [3]: from dateutil.rrule import rrule, YEARLY, SU

In [4]: # Build UK and USA start dates using rrule
   ...: dst_df = pd.DataFrame(data={
   ...:     'UK DST Start': rrule(
   ...:         YEARLY,
   ...:         dtstart=datetime.date(2014, 1, 1),
   ...:         count=20,
   ...:         bymonth=3,
   ...:         byweekday=SU(-1)),  # Last Sunday of the month
   ...:     'USA DST Start': rrule(
   ...:         YEARLY,
   ...:         dtstart=datetime.date(2014, 1, 1),
   ...:         count=20,
   ...:         bymonth=3,
   ...:         byweekday=SU(2)),  # Second Sunday of the month
   ...:     }
   ...: )

In [5]: dst_df['Weeks overlap'] = dst_df['UK DST Start'] - dst_df['USA DST Start']

In [6]: dst_df[' '] = dst_df.apply(lambda r: "👈 You are here" if r['UK DST Start'].year == 2024 else '',
   ...:  axis='columns')

In [7]: dst_df
Out[7]:
   UK DST Start USA DST Start Weeks overlap
0    2014-03-30    2014-03-09       21 days
1    2015-03-29    2015-03-08       21 days
2    2016-03-27    2016-03-13       14 days
3    2017-03-26    2017-03-12       14 days
4    2018-03-25    2018-03-11       14 days
5    2019-03-31    2019-03-10       21 days
6    2020-03-29    2020-03-08       21 days
7    2021-03-28    2021-03-14       14 days
8    2022-03-27    2022-03-13       14 days
9    2023-03-26    2023-03-12       14 days
10   2024-03-31    2024-03-10       21 days  👈 You are here
11   2025-03-30    2025-03-09       21 days
12   2026-03-29    2026-03-08       21 days
13   2027-03-28    2027-03-14       14 days
14   2028-03-26    2028-03-12       14 days
15   2029-03-25    2029-03-11       14 days
16   2030-03-31    2030-03-10       21 days
17   2031-03-30    2031-03-09       21 days
18   2032-03-28    2032-03-14       14 days
19   2033-03-27    2033-03-13       14 days
```

Wow - so there are many more 3 week overlaps than I thought!

## 👀 Review

Looking back, only two of the last eight years have had a three week "1 hour
closer overlap".

Let's be honest, I'm not sure how I missed the three week overlap in 2019.

But for the 2020 one, although I _was_ working for a US company, we were in
COVID lock-down _and_ `child[0]` was only a few weeks old so I was on parental
leave.

However, looking forward, 2024 marks the start of a 3 year run of three week
overlaps!

## 🧠 A new mental model

So my conclusion is that my previous mental model was pretty poor. It's time
for a new one. Here we go:

> When March starts on a Friday, Saturday or Sunday then there will be 3 weeks
> of "1 hour closer overlap" with North America, otherwise it's 2.

Let's confirm that by averaging the twenty years in the DataFrame above:

```py
# Add a 'first' column which contains the first day of March for each year
In [23]: dst_df['first'] = dst_df.apply(
    ...:     lambda r: datetime.date(r['UK DST Start'].year, 3, 1).strftime('%a'),
    ...:     axis='columns',
    ...: )

In [24]: dst_df.groupby('first')['Weeks overlap'].mean()
Out[24]:
first
Fri   21 days
Mon   14 days
Sat   21 days
Sun   21 days
Thu   14 days
Tue   14 days
Wed   14 days
Name: Weeks overlap, dtype: timedelta64[ns]
```

That looks right - so that's my new mental model sorted.

Now I just need to remember to check on what NHL ice hockey games will be
happening between 9th and 30th March 2025 when the schedule is published -
that's going to be three weeks of "easier to watch" matches! 😊
