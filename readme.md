# Meetup bot
I keep missing the meetup because the schedule is too odd for my calendar app. (Every last Thursday of the month, wat?)
This is the overengineered solution. It will remind everyone in #general one day in advance, and ten minutes in advance of every meetup. It doesn't currently take into account any changes to the normal schedule.

## Setup / Run (linux)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```