from time import sleep
from os import environ
from requests import get
from datetime import datetime, timezone
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPE = 'https://www.googleapis.com/auth/calendar.events'

CALENDAR_ID = environ['CALENDAR_ID']
SATELLITE_ID = environ['SATELLITE_ID']
N2YO_API_KEY = environ['N2YO_API_KEY']
LATITUDE = environ['LATITUDE']
LONGITUDE = environ['LONGITUDE']

def main():
    service = init()
    while True:
        run(service)
        hours = 12
        sleep(hours * 60 * 60)


def init():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPE)
        creds = tools.run_flow(flow, store)
    return build('calendar', 'v3', http=creds.authorize(Http()))


def overlap(passes, search):
    for p in passes:
        if local_time(p['endUTC']).timestamp() > search[0] and local_time(p['startUTC']).timestamp() < search[1]:
            return True
    return False

def local_time(string):
    return datetime.utcfromtimestamp(int(string)).replace(tzinfo=timezone.utc).astimezone(tz=None)


def unix_time_from_iso(string):
    return datetime.fromisoformat(string).timestamp()


def run(service):
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                        maxResults=50, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    url = 'https://www.n2yo.com/rest/v1/satellite/radiopasses/' + SATELLITE_ID + '/' + LATITUDE+ '/' + LONGITUDE + '/0/2/0/&apiKey=' + N2YO_API_KEY
    response = get(url)
    passes = response.json()['passes']
    satellite_id = response.json()['info']['satid']
    satellite_name = response.json()['info']['satname']

    for event in events:
        start = event['start'].get('dateTime')
        start_unix_time = unix_time_from_iso(start)
        end = event['end'].get('dateTime')
        end_unix_time = unix_time_from_iso(end)
        if overlap(passes, (start_unix_time, end_unix_time)):
            service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
    
    for p in passes:
        event = {
            'summary': satellite_name + ' Pass',
            'description': satellite_id,
            'start': {
                'dateTime': local_time(p['startUTC']).isoformat(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': local_time(p['endUTC']).isoformat(),
                'timeZone': 'America/New_York',
            }
        }
        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

if __name__ == '__main__':
    main()
