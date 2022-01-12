# id-tech-test

Serverless function to help with managing admin processes for the Infrastructure Delivery team.
`github_webhook` listens for events from Github when someone creates or edits a Wiki page, and posts a message in Slack with the details.

## Prerequisites

To run the app and tests locally:

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

You'll need to set up a Slack app to enable you to access the Slack API.

Install serverless and jq to deploy the lambdas via serverless:

```sh
npm install serverless --save
npm install serverless-crypt
brew install jq
```

## Secrets management

Secrets are managed using the [serverless-crypt](https://github.com/marcy-terui/serverless-crypt) plugin. This plugin relies on KMS, so you should set an environment variable `AWS_KMS_KEYID` to point to the ARN of the key that you'd like to use for this.

Two secrets are required:

- `GITHUB_WEBHOOK_SECRET`: a shared secret to allow us to validate Wiki webhook events from Github.
- `SLACK_API_TOKEN`: a Slack OAuth access token for accessing general Slack API functions. It needs `chat:write:bot` permissions in order to send messages.

 If you need to update a secret, here's how to do it:

```sh
$ serverless encrypt -n SLACK_API_TOKEN -t MYTOKEN --save
Serverless: Name of the secret: SLACK_API_TOKEN
Serverless: Encrypt the text: MYTOKEN
Serverless: Cipher text: AQICAHic00ID678OlOQtYRLGpzuTi3LFsNTMS0joyQ+3nNiHIAEklBkRpM2A+cUbmYPIX2hgAAAArzCBrAYJKoZIhvcNAQcGoIGeMIGbAgEAMIGVBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEED
CdH3PvUKM/Y75zFZgIBEIBoxCF5fu4r2ZqoT0Ga6+7fCm/WiC3e4B0W9Nmx8rurX8XzDUvzaIW3ZD3cv+Sn458+gAut5RMhiKC23Ioynz+YSoaRw9H0UY+qGaIXxbSBXcyHaUvaZ+eolCWaESsJ/8KOlOhAW9VA2do=
Serverless: Successfully saved the secret that named "SLACK_API_TOKEN"
```

You can (and should!) commit the resulting `.serverless-secret.json` to Git.
## Adding the webhook

You can add a webhook to a Github repository in Settings / Webhooks. This function only understands Wiki events (Github calls these `gollum` events).

# Deployment

To deploy the serverless functions:

```sh
make deploy
```
## Manually Running tests

To run the tests locally:

```sh
make test
```

Or for coverage:

```sh
make test-coverage && open htmlcov/index.html
```

## Contact

Please contact [Infrastructure Delivery](mailto:infrastructure.delivery@ft.com) with any questions or PRs.
