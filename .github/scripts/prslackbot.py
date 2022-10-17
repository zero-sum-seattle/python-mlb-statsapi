import sys
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def reportpullrequesturl(slack_webclient_token, slack_channel_id, url):

    # WebClient instantiates a client that can call API methods
    client = WebClient(token=slack_webclient_token)

    # ID of channel you want to post message to
    channel_id = slack_channel_id

    try:
        # Call the conversations.list method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            blocks= [               
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'<{url}>'
                    }
                }
            ]
        )        

    except SlackApiError as e:
        print(f"Error: {e}")        


def main(args):
    reportpullrequesturl(args[1], args[2], args[2])

if __name__ == '__main__':
    main(sys.argv)