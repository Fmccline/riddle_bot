# Silly Bot

## About
Silly Bot is a Twitch chat bot meant to increase chat interaction for streamers.

## Setup

### Docker
Install docker. Pull the silly_bot image. Run the image.
### Without Docker
Make sure python3 is installed.
Open up a command prompt and run the following commands:

`pip install --upgrade pip`

`pip install -r requirements.txt`

## Commands
### !riddle 
Responds with the question for a riddle. After a set amount of time, it will respond with an answer. Only one riddle at a time will be given in a specific chat.

### !fact
Responds with a random fact.

## Running Silly Bot
If you installed Docker, run the image. If you're just using python run:  `python silly_bot.py`

