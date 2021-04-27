# pylint: disable=C0111
import os
import pytest
from lib.github import Github

def test_init_uses_secret_parameter_if_provided():
  os.environ['GITHUB_WEBHOOK_SECRET'] = 'envsekrit'
  sut = Github(secret='sekrit')
  assert sut.secret == b'sekrit'

def test_init_uses_environment():
  os.environ['GITHUB_WEBHOOK_SECRET'] = 'envsekrit'
  sut = Github()
  assert sut.secret == b'envsekrit'

def test_handler_validates_github_signature(github_event_apig):
  sut = Github(secret='stEnteRAntIADG')
  sut.handle(github_event_apig)

def test_handler_raises_exception_for_invalid_signature(github_event_apig):
  sut = Github(secret='i-am-invalid')
  with pytest.raises(ValueError, match='invalid signature'):
    sut.handle(github_event_apig)

def test_handler_raises_exception_for_unhandled_event_type(github_event_apig):
  sut = Github(secret='stEnteRAntIADG')
  github_event_apig["headers"]["X-GitHub-Event"] = 'some-strange-event'
  with pytest.raises(ValueError, match="Can't handle event type some-strange-event"):
    sut.handle(github_event_apig)

def test_handler_returns_list_of_messages(github_event_apig):
  sut = Github(secret='stEnteRAntIADG')
  messages = sut.handle(github_event_apig)
  assert isinstance(messages, list)
  assert len(messages) == 1

  attachment = messages[0][0]
  assert attachment["author_name"] == 'jonnangle just edited this wiki page!'
  assert attachment["title"] == 'Home'
  assert attachment["title_link"] == 'https://github.com/Financial-Times/id-tech-test/wiki/Home'
