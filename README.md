# AI Fact of the Day

A beginner-friendly first AWS deploy: an AWS Lambda function with a public
Function URL that calls Amazon Bedrock (Nova Lite) to generate a fresh,
interesting fact every time someone visits, and returns it as a simple
styled HTML page.

Refresh the page for a new, live-generated fact each time.

## How it works

1. A visitor opens the Function URL in a browser (a GET request arrives).
2. AWS Lambda runs the handler function.
3. The handler calls Amazon Bedrock (Nova Lite) with a prompt asking for a
   short, interesting, verifiable fact from a randomly chosen category.
4. The response is wrapped in a small styled HTML page and returned
   directly as the HTTP response - no separate frontend or server needed.

Every request generates a genuinely new fact live via Bedrock - nothing is
pre-written or cached.

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
