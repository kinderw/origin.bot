import discord
import os
import pickle
import requests

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

client = discord.Client()

#add ytid to playlist
def insert_yturlweb(yturlid):

    credentials = None
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    client_secrets_file = "client_secrets.json"
    api_service_name = "youtube"
    api_version = "v3"

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            flow.run_local_server(port=8080, prompt='consent',
                                authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials, static_discovery=False)
    print('mid call1')
    request = youtube.playlistItems().insert(
        part='snippet',
        body={
            "snippet": {
                "playlistId": "PLOVRtyd9seKLumOZ3u8DWzBhrLcgdIuHw",
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": yturlid
                }
            }
        }  
    )
    response = request.execute()
    print(response)

#add ytid to playlist - test
def insert_yturlid(yturlid):
  print('start call')

  scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

  api_service_name = "youtube"
  api_version = "v3"
  client_secrets_file = "test-lib.json"

  flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
  credentials = flow.run_console()
  
  youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials, static_discovery=False)
  print('mid call1')
  request = youtube.playlistItems().insert(
    part='snippet',
    body={
        "snippet": {
            "playlistId": "PLOVRtyd9seKLumOZ3u8DWzBhrLcgdIuHw",
            "position": 0,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": yturlid
            }
        }
    }  
  )
  print('mid call2')
  response = request.execute()
  print(response)



#build init full list
def build_init():
  print('placeholder')

  
#on_ready
@client.event
async def on_ready():
  print('forming {0.user}'.format(client))


#yt link capture
@client.event
async def on_message(message):
  channel_id = str(message.channel.id)
  channel = message.channel
  
  if message.author == client.user:
    return

  if message.content.startswith('https://www.youtube.com/watch') and channel_id == '860650829101924372':
    yturl = message.content
    r = requests.get(yturl)
    if r.status_code == 200:
      await message.channel.send('yt url captured')
      yturlid = yturl.split('=')[1]
      #yt api function
      insert_yturlweb(yturlid)
    else:
      await message.channel.send('yt url failed capture')
      
    print('')
    print(channel_id)
    print(channel)
    print(yturlid)
    

client.run(os.environ['TOKEN'])