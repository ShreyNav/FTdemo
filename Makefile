.PHONY: test test-coverage

slsdep:
	apt install nodejs
	apt install npm
	npm install -g serverless

pydep:
	pip install -r requirements.txt

lint:
	pylint -f colorized lib/ test/

test:
	PYTHONPATH=. pytest -v test/

deploy:
	serverless deploy

test-coverage:
	PYTHONPATH=. pytest -v --cov=lib --cov-report=html --cov-report=term test/ \

create-kms-stack:
	aws cloudformation create-stack --stack-name=idbot-kms \
		--template-body file://cf/kms.yaml \

update-kms-stack:
	aws cloudformation update-stack --stack-name=idbot-kms \
		--template-body file://cf/kms.yaml \

delete-kms-stack:
	aws cloudformation delete-stack --stack-name=idbot-kms

get-kms-arn:
	aws cloudformation describe-stacks --stack-name idbot-kms | jq -r .Stacks[].Outputs[].OutputValue