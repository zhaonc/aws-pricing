# AWS Pricing Navigation

## Introduction

Quickly navigate the spot pricing at Amazong AWS. Refer to AWS pricing pages for [details](https://aws.amazon.com/ec2/spot/pricing/).

## Usage

Run `streamlit run main.py` from `aws-pricing`. By default [streamlit](https://streamlit.io/) will listen on port 8501.

## Deployment

Build and run Docker container with `Dockerfile`. For example

```
docker build -t aws-pricing .
docker run -p 80:8501 aws-pricing
```

Also you may use `docker-compose.yml` as an example. You may need to change the network options `network_mode` to your desired setup.

## Disclaimer

The APIs used in this project can be found on AWS pricing pages. The author of this project is not affiliated with Amazon AWS. Use this software and information at your own risk.