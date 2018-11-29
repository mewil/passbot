# PassBot

How to use PassBot:
-  Get Docker: `curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh`
-  Enable the Google Calendar API and follow along with the [Python Quickstart](https://developers.google.com/calendar/quickstart/python)
-  Following the above guide will create the necessary `credentials.json` and `token.json` files which need only be generated once
-  Create a file called `.env` with the following environment variables:
```
CALENDAR_ID
N2YO_API_KEY
SATELLITE_ID
LATITUDE
LONGITUDE
```
- Run `docker build -t passbot . && docker run --env-file .env -P -d passbot` to build the docker container and run it in the background
