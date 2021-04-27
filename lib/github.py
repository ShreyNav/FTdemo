""" Management of github things. """
import os
import json
import hmac
from urllib.parse import parse_qs
from hashlib import sha1

# pylint: disable=R0903
class Github():
  """ Handles Github webhooks. """

  def __init__(self, secret=None):
    if secret is None:
      secret = os.environ['GITHUB_WEBHOOK_SECRET']
    self.secret = secret.encode('utf-8')

  def _github_signature(self, event):
    header = event["headers"]["X-Hub-Signature"]
    return header[len('sha1='):]

  def _validate_signature(self, event):
    body = event["body"].encode('utf-8')
    signature = self._github_signature(event)

    mac = hmac.new(self.secret, msg=body, digestmod=sha1)
    if not hmac.compare_digest(mac.hexdigest(), signature):
      raise ValueError("invalid signature!")

  def handle(self, event):
    """ Handles an APIG event containing a webhook. """

    self._validate_signature(event)

    event_type = event["headers"]["X-GitHub-Event"]
    if event_type != 'gollum':
      raise ValueError(f"Can't handle event type {event_type}")

    payload = parse_qs(event["body"])["payload"][0]
    gh_event = json.loads(payload)
    pages = gh_event["pages"]
    sender = gh_event["sender"]["login"]

    messages = []
    for page in pages:

      messages.append(
        [
          {
            "color": "#36a64f",
            "author_name": f"{sender} just {page['action']} this wiki page!",
            "title": page['title'],
            "title_link": page['html_url'],
            "footer": "sent by id-bot"
          }
        ]
      )

    return messages
