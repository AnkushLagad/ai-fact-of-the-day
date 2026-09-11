# AI Fact of the Day

A beginner-friendly first AWS deploy: an AWS Lambda function with a public
Function URL that calls Amazon Bedrock (Nova Lite) to generate a fresh,
interesting fact every time someone visits, and returns it as a simple
styled HTML page.

## AWS services used

- **AWS Lambda** - runs the handler code and exposes it via a public
  Function URL, with no separate API Gateway or web server needed.
- **Amazon Bedrock (Nova Lite)** - generates the fact text live on every
  request via a direct `invoke_model` call.

## Deploying it yourself

```bash
zip function.zip lambda_function.py

aws lambda create-function \
  --function-name ai-fact-of-the-day \
  --runtime python3.12 \
  --role <your-lambda-execution-role-arn> \
  --handler lambda_function.handler \
  --zip-file fileb://function.zip \
  --timeout 15 \
  --region us-west-2

aws lambda create-function-url-config \
  --function-name ai-fact-of-the-day \
  --auth-type NONE \
  --region us-west-2

aws lambda add-permission \
  --function-name ai-fact-of-the-day \
  --statement-id FunctionURLAllowPublicAccess \
  --action lambda:InvokeFunctionUrl \
  --principal "*" \
  --function-url-auth-type NONE \
  --region us-west-2
```

The execution role needs `bedrock:InvokeModel` permission for
`amazon.nova-lite-v1:0` in `us-west-2`.
