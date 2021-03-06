from __future__ import print_function

from datetime import date
from datetime import datetime
import datetime as DT

import pickle
import os.path
from time import time
from xmlrpc.client import DateTime

from googleapiclient.discovery import build
# from google-api-python-client.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of up to 20 events on the user's calendar starting
    1 week ago until today.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
################################################################
    # List all calendars available:
    print('These are all the calendars available to read (calendar name followed by calendar ID)')
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'])
            print(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    print('')
################################################################
    # Call the Calendar API for one week ago through today
    now = datetime.today()
    #print("Current day and time is:")
    #print(now)
    #print(' ')
    oneWeekAgo = now - (DT.timedelta(days=7))

    # Let's get this dateTime into the proper format for Google Calendar API
    # https://stackoverflow.com/questions/66092974/formatting-datetime-in-python-properly-for-google-calendar-api/66099866#66099866
    oneWeekAgo = oneWeekAgo.isoformat() + 'Z' # 'Z' indicates UTC time
    #print("Seven days ago is:")
    #print(oneWeekAgo)

    now = now.isoformat() + 'Z' # 'Z' indicates UTC time

    print('Getting events on primary calendar, starting 1 week ago from today: ')
    events_result = service.events().list(calendarId='primary', timeMin=oneWeekAgo,
                                          timeMax=now, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        #start = event['start'].get('dateTime', event['start'].get('date'))
        #print(start, event['summary'])
        print(event['summary'])

if __name__ == '__main__':
    main()
