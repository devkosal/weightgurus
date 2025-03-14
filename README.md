# weightgurus flask app for easy display / motivation

Setup:
1. Run `pip install -r requirements.txt`
2. Create `.env` file e.g.
```
USERS_JSON='[{"username":"johndoe@gmail.com", "password": "p@ssword", "alias": "John"}]'
TIMEZONE=America/New_York
```
3. Run `python src/app.py` (runs in development mode)


# weightgurus (from fork origin)
API Interface for Weight Gurus

This is a simple API interface for Weight Gurus,
it allows you to pull down your entire weight history
and submit new weights.

Weight Gurus doesn't have any documentation for their API,
so this does the best we can with the little information we have.

## Usage

When using stand-alone you need to add your username and password
to the main method, then either use 'get_all'