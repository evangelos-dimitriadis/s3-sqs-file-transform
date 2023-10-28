# S3 client server demo

## How to run the demo

Before running the demo make sure that the AWS credentials' file is located to `$HOME/.aws/credentials`.
If you use another location edit the `docker-compose.yml` volume to point to the correct file. It is possible to use mock-up credentials if you use localstack.

The command to start the demo is:

`docker-compose up`

It is possible to run first in the background `localstack` (`docker-compose up -d localstack`)
and then `bestseller`, but not the opposite.
This will be helpful to easier focus on one's containers logs.

When the server has successfully started you can upload a file to the client's S3 from another console by typing:

`docker exec -it demo python client.py examples/example.xml`

You can add your own examples to this folder. The folder "examples" is mounted to the docker container.

To check the creation of the s3 object visit the URL:

`http://localhost:4566/serverbucket4321`

## Configuration

Using AWS instead of localstack is possible. Inside the `docker-compose.yml` you will need to
comment out the `ENDPOINT_URL` and use all the other fields. Also, when using localstack,
you can use a fake AWS credentials file to pass to the docker.

**Attention**

Both S3 buckets must preexists along with the SQS and the `AWS_PROFILE` must have access to those resources.
The demo will set up the SQS to receive messages from the `CLIENT_BUCKET`.

## Tests

Run tests by running the command:

`docker exec -it demo python -m pytest`
