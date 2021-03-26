from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def meetlinks():
    creds = None
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

    # Call the Calendar API
    now_ = datetime.datetime.utcnow()
    now = now_.isoformat() + 'Z' # 'Z' indicates UTC time (7am IST to 9om IST => 2 am to 13pm UTC)
    day_start = datetime.datetime(now_.year, now_.month, now_.day, 2, 0, 0).isoformat() + 'Z'
    day_end = datetime.datetime(now_.year, now_.month, now_.day, 13, 0, 0).isoformat() + 'Z'
   
    events_result = service.events().list(calendarId='primary', timeMin = day_start, timeMax = day_end, singleEvents=True,
                                        orderBy='startTime', maxResults = 10).execute()
    events = events_result.get('items', [])
    print("==============================================")
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')
        if start is None or end is None:
            continue
        start_time = str(datetime.datetime.fromisoformat(start).time()).replace("+05:30","")
        end_time = str(datetime.datetime.fromisoformat(end).time()).replace("+05:30","")

        try:
            print(start_time, end_time, event['summary'],"\t\t", event['location'])
        except KeyError:
            print(start_time,end_time, event['summary'], "\t\t", "no meet link")
    print(("=============================================="))
    with open('meet.txt', 'w') as fh:
        for event in events:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            if start is None or end is None:
                continue
            start = str(start).replace("+05:30","")
            end = str(end).replace("+05:30","")
            try:
                fh.write(f"{str(start)}\t{str(end)}\t{event['summary']}\t\t{event['location']}\n")
            except KeyError:
                fh.write(f"{str(start)}\t{str(end)}\t{event['summary']}\t\tNo meet info\n")
    fh.close()
