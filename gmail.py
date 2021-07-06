from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service


def show_threads(service, no_of_mails=100, user_id='me'):
    threads = service.users().threads().list(userId=user_id, maxResults=no_of_mails).execute().get('threads', [])
    mails = []
    for thread in threads:
        tdata = service.users().threads().get(userId=user_id, id=thread['id']).execute()
        nmsgs = len(tdata['messages'])

        msg = tdata['messages'][0]['payload']
        subject = ''
        From = ''
        #Date=''
        for header in msg['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'Date':
                Date= header['value']
            if header['name'] == 'From':
                From = header['value']
                From=From.replace('<','')
                From=From.replace('>', '')

                break
        snippet = tdata['messages'][0]['snippet']
        mails.append({
            'snippet': snippet,
            'subject': subject,
            'from' : From,
            'date' : Date
        })

    return mails


if __name__ == '__main__':

    service = main()
    # mails = show_threads(service)
    # print('---' * 30)
    # print(len(mails))
    # print('---' * 30)
