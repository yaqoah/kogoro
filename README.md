# 🎯 Kogorō

A bot that predicts football matches outcome and gives wide-ranging statistics in Telegram.
#
![Kogoro Demo](github/kogoroGIF.gif)
## Features:
- Predictions: 
  1) Expected outcome(win/draw/lose)
  2) Winner and probability of winning
  3) Total goals
  4) Anticipated attacking and defending potency. 
- League Statistics: All inclusive Stats.
- Team Statistics: 
  1) Form 
  2) (win/draw/lose) Ratios
  3) (most/least) Productive minutes and their statistics
  4) (win/lose) Streaks. 
  5) (highest/lowest) Goal streaks
  6) Clean Sheets
- Player Statistics: shots, passes, defending, dribbling cards and foul play statistics.

Kogoro leverages "FOOTBALL-API" which primarily relies upon the poisson-distribution algorithm among others to produce the predictions.

# Configuration:
If you want to run the bot locally, you will need a number of variables before preparing to launch.

```
> RapidApi host and key values. (from Rapid-API: Football-API)
> Bot token. (from BotFather in Telegram)
> Telegram api and hash.  (from Telegram)
> Call URL of Football-API. (from Rapid-API: Football API)
> Some custom f-string messages and others (bot/__init__.py)
```
