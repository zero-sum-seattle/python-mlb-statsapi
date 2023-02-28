import sys
import os
import datetime
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# get from environment variables
ISSUE_URL           = os.environ.get("ISSUE_URL")
ISSUE_USER          = os.environ.get("ISSUE_USER")
ISSUE_USER_IMAGE    = os.environ.get("ISSUE_USER_IMAGE")
ISSUE_NUMBER        = os.environ.get("ISSUE_NUMBER")
ISSUE_TITLE         = os.environ.get("ISSUE_TITLE")
ISSUE_TIME          = int(datetime.datetime.timestamp(datetime.datetime.strptime(os.environ.get("ISSUE_TIME"), "%Y-%m-%dT%H:%M:%SZ")))
ISSUE_BODY          = os.environ.get("ISSUE_BODY")
ISSUE_REPO          = os.environ.get("ISSUE_REPO")
ISSUE_REPO_URL      = os.environ.get("ISSUE_REPO_URL")

def reportpullrequesturl(channel, slacktoken, msg):

    # WebClient instantiates a client that can call API methods
    client = WebClient(token=slacktoken)

    # ID of channel you want to post message to
    channel_id = channel

    try:
        # Call the conversations.list method using the WebClient
        client.chat_postMessage(
            channel=channel_id,
            text = f'New Issue Created',
            blocks= [                                            
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": f'{ISSUE_USER_IMAGE}',
                            "alt_text": "user logo"  
                        },                      
                        {
                            "type": "mrkdwn",
                            "text": f'{ISSUE_USER} opened new issue *<{ISSUE_URL}|#{ISSUE_NUMBER}> \n{ISSUE_URL}'
                        }
                    ]
                },           
                {
                    "type": "divider"
                }                              
            ],
            attachments= [
                {
                    "color": "#3ca553",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f'*<{ISSUE_URL}|#{ISSUE_NUMBER} {ISSUE_TITLE}>* \n{msg}'
                            }
                        },                        
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "image",
                                    "image_url": 'https://slack-imgs.com/?c=1&o1=wi32.he32.si&url=https%3A%2F%2Fslack.github.com%2Fstatic%2Fimg%2Ffavicon-neutral.png',
                                    "alt_text": "github logo"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f'<{ISSUE_REPO_URL}|{ISSUE_REPO}> _|_ <!date^{ISSUE_TIME}^' + '{date_pretty} at {time}|' + f'{ISSUE_TIME}> _|_ Added by cronbot'
                                }
                            ]
                        }
                    ]
                }                
            ]
        )        

    except SlackApiError as e:
        print(f"Error: {e}")        


def format_pr_template() -> str:
    msg = []

    for line in ISSUE_BODY.splitlines():        
        if line[:4] == "### ":
            line = '*' + line[4:] + '*'
        msg.append(line)
    
    return "\n".join(msg)

def main(args):
    message = format_pr_template()
    reportpullrequesturl(args[1], args[2], message)

if __name__ == '__main__':
    main(sys.argv)