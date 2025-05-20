# End to End RAG Application

![Screenshot (253)](https://github.com/user-attachments/assets/e685176e-084a-4728-8eed-9d5e1d198480)

### Configure AWS

You need to have an AWS account, and AWS CLI set up on your machine.

### Update .env File with AWS Credentials

Create a file named `.env` in `image/`. 

```
AWS_ACCESS_KEY_ID=XXXXX
AWS_SECRET_ACCESS_KEY=XXXXX
AWS_DEFAULT_REGION=us-east-1
TABLE_NAME=YourTableName
```

### Installing Requirements

```sh
pip install -r image/requirements.txt
```

### Building the Vector DB

Put all the PDF source files you want into `image/src/data/source/`. Then go `image` and run:

```sh
# Use "--reset" if you want to overwrite an existing DB.
python populate_database.py --reset
```

### Running the App

```sh
# Execute from image/src directory
cd image/src
python rag_app/query_rag.py "how much does a landing page cost?"
```

Example output:

```text
Answer the question based on the above context: How much does a landing page cost to develop?

Response:  Based on the context provided, the cost for a landing page service offered by Galaxy Design Agency is $4,820. Specifically, under the "Our Services" section, it states "Landing Page for Small Businesses ($4,820)" when describing the landing page service. So the cost listed for a landing page is $4,820.
Sources: ['src/data/source/galaxy-design-client-guide.pdf:1:0', 'src/data/source/galaxy-design-client-guide.pdf:7:0', 'src/data/source/galaxy-design-client-guide.pdf:7:1']
```

### Starting FastAPI Server

```sh
# From image/src directory.
python app_api_handler.py
```

Then go to `http://0.0.0.0:8000/docs` to try it out.

## Using Docker Image

These commands can be run from `image/` directory to build, test, and serve the app locally.

```sh
docker build --platform linux/amd64 -t aws_rag_app .
```

```sh
# Run the container using command `python app_work_handler.main`
docker run --rm -it \
    --entrypoint python \
    --env-file .env \
    aws_rag_app app_work_handler.py
```

## Running Locally as a Server

Assuming you've build the image from the previous step.

```sh
docker run --rm -p 8000:8000 \
    --entrypoint python \
    --env-file .env \
    aws_rag_app app_api_handler.py
```

## Testing Locally

After running the Docker container on localhost, you can access an interactive API page locally to test it: `http://0.0.0.0:8000/docs`.

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/submit_query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query_text": "How much does a landing page for a small business cost?"
}'
```

## Deploy to AWS

I have put all the AWS CDK files into `rag-cdk-infra/`. Go into the folder and install the Node dependencies.

```sh
npm install
```

Then run this command to deploy it (assuming you have AWS CLI already set up, and AWS CDK already bootstrapped). I recommend deploying to `us-east-1` to start with (since all the AI models are there).

```sh
cdk deploy
```
