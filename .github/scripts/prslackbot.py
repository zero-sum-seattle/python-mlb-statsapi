import sys
import os
import datetime
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# get from environment variables
SLACK_WEBCLIENT_TOKEN   = os.environ.get("SLACK_WEBCLIENT_TOKEN")
CHANNEL                 = os.environ.get("CHANNEL")
PR_URL                  = os.environ.get("PR_URL")
PR_USER                 = os.environ.get("PR_USER")
PR_USER_IMAGE           = os.environ.get("PR_USER_IMAGE")
PR_NUMBER               = os.environ.get("PR_NUMBER")
PR_TITLE                = os.environ.get("PR_TITLE")
PR_TIME                 = datetime.datetime.timestamp(datetime.datetime.strptime(os.environ.get("PR_TIME"), "%Y-%m-%dT%H:%M:%SZ"))
PR_BODY                 = os.environ.get("PR_BODY")
PR_REPO                 = os.environ.get("PR_REPO")
PR_REPO_URL             = os.environ.get("PR_REPO_URL")
NUM_COMMIT              = os.environ.get("NUM_COMMIT")
HEAD_REPO_NAME          = os.environ.get("HEAD_REPO_NAME")
BASE_REPO_NAME          = os.environ.get("BASE_REPO_NAME")

def reportpullrequesturl(channel, slacktoken):

    # WebClient instantiates a client that can call API methods
    client = WebClient(token=slacktoken)

    # ID of channel you want to post message to
    channel_id = channel

    try:
        # Call the conversations.list method using the WebClient
        client.chat_postMessage(
            channel=channel_id,
            text = f'New pull request by KCNilssen',
            blocks= [                                            
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": f'{PR_USER_IMAGE}',
                            "alt_text": "user logo"  
                        },                      
                        {
                            "type": "mrkdwn",
                            "text": f'{PR_USER} wants to merge {NUM_COMMIT} commits into <{PR_REPO_URL}'+f'/tree/'+'{BASE_REPO_NAME}|{BASE_REPO_NAME}> from <{HEAD_REPO_URL}'+f'/tree/'+'{HEAD_REPO_NAME}|{HEAD_REPO_NAME}> \n{PR_URL}'
                        }
                    ]
                },           
                {
                    "type": "divider"
                }                              
            ],
            attachments= [
                {
                    "color": "#f2c744",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f'*<{PR_URL}|#{PR_NUMBER} {PR_TITLE}>* \n{PR_BODY}'
                            }
                        },                        
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "image",
                                    "image_url": f'{PR_USER_IMAGE}',
                                    "alt_text": "github logo"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f'<{PR_REPO_URL}|{PR_REPO}> _|_ <!date^{PR_TIME}^' + '{date_pretty} at {time}|' + f'{PR_TIME}> _|_ Added by cronbot'
                                }
                            ]
                        }
                    ]
                }                
            ]
        )        

    except SlackApiError as e:
        print(f"Error: {e}")        


def main(args):
    reportpullrequesturl(args[1], args[2])

if __name__ == '__main__':
    main(sys.argv)