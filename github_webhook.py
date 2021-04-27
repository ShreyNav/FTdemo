import json
from lib.slackapi import SlackAPI
from lib.secrets import get_secret_or_environment
from lib.github import Github

def handler(event, context):
  github_secret = get_secret_or_environment('GITHUB_WEBHOOK_SECRET')
  slack_api_token = get_secret_or_environment('SLACK_API_TOKEN')

  github = Github(secret=github_secret)
  slack = SlackAPI(api_token=slack_api_token)

  slack_messages = github.handle(event)
  for message in slack_messages:
    slack.send_message('bot-playground', attachments=message)

  return {
    "statusCode": 200,
    "body": f"ok: sent {len(slack_messages)} messages"
  }
