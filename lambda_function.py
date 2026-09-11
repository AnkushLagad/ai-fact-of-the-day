import json
import random
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")
MODEL_ID = "amazon.nova-lite-v1:0"

CATEGORIES = [
    "space and astronomy",
    "the ocean and marine life",
    "ancient history",
    "computer science and technology history",
    "animals and biology",
    "language and etymology",
    "food and cooking science",
    "mathematics",
]


def generate_fact():
    category = random.choice(CATEGORIES)
    prompt = (
        f"Share one genuinely interesting, true, and verifiable fact about "
        f"{category}. Write it as a single engaging paragraph, 2-3 sentences, "
        f"in a friendly and slightly enthusiastic tone. Do not use markdown "
        f"formatting, headers, or bullet points - just plain, well-written "
        f"prose. Do not start with generic phrases like 'Did you know' - "
        f"just state the fact directly and engagingly."
    )
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 250, "temperature": 0.9},
        }),
    )
    result = json.loads(response["body"].read())
    fact_text = result["output"]["message"]["content"][0]["text"]
    return fact_text, category


def build_html_page(fact_text, category):
    safe_fact = fact_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_category = category.title()
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Fact of the Day</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
    background: linear-gradient(135deg, #232F3E, #37475A); color: #ffffff;
    min-height: 100vh; margin: 0; display: flex; align-items: center;
    justify-content: center; padding: 24px; }
  .card { max-width: 640px; background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 16px;
    padding: 36px 32px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
  .label { display: inline-block; background: #FF9900; color: #232F3E;
    font-weight: bold; font-size: 0.8em; padding: 4px 12px; border-radius: 999px;
    margin-bottom: 18px; text-transform: uppercase; letter-spacing: 0.5px; }
  h1 { margin: 0 0 20px 0; font-size: 1.6em; }
  p.fact { font-size: 1.15em; line-height: 1.7; margin: 0 0 24px 0; }
  .refresh-hint { font-size: 0.85em; color: #cccccc;
    border-top: 1px solid rgba(255, 255, 255, 0.15); padding-top: 16px; }
  .refresh-hint a { color: #FF9900; text-decoration: none; font-weight: bold; }
</style>
</head>
<body>
  <div class="card">
    <span class="label">CATEGORY_PLACEHOLDER</span>
    <h1>AI Fact of the Day</h1>
    <p class="fact">FACT_PLACEHOLDER</p>
    <div class="refresh-hint">
      Generated live by Amazon Bedrock (Nova Lite).
      <a href="/">Refresh for a new fact &rarr;</a>
    </div>
  </div>
</body>
</html>"""
    html = html.replace("CATEGORY_PLACEHOLDER", safe_category)
    html = html.replace("FACT_PLACEHOLDER", safe_fact)
    return html


def handler(event, context):
    try:
        fact_text, category = generate_fact()
        html = build_html_page(fact_text, category)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": html,
        }
    except Exception as e:
        error_html = "<html><body style='font-family: sans-serif; padding: 40px;'><h2>Something went wrong generating today's fact</h2><p>Please try refreshing the page. (Error: " + str(e) + ")</p></body></html>"
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": error_html,
        }
