import html
import json
import logging
import os
import random

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = os.environ.get("AWS_REGION", "us-west-2")
MODEL_ID = os.environ.get("MODEL_ID", "amazon.nova-lite-v1:0")
bedrock = boto3.client("bedrock-runtime", region_name=REGION)

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
    fact_text = result["output"]["message"]["content"][0]["text"].strip()
    return fact_text, category


def build_html_page(fact_text, category):
    safe_fact = html.escape(fact_text, quote=True)
    safe_category = html.escape(category.title(), quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#10141d">
  <meta name="description" content="A fresh, AI-generated fact to brighten your day.">
  <title>AI Fact of the Day</title>
  <style>
    :root {{
      color-scheme: dark;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #f5f2ea;
      background: #10141d;
      font-synthesis: none;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
      --muted: #a4a9b5;
      --accent: #f4b45f;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      min-height: 100vh;
      margin: 0;
      overflow-x: hidden;
      background:
        radial-gradient(ellipse at 82% 23%, rgba(118, 83, 50, 0.22), transparent 34%),
        radial-gradient(ellipse at 14% 94%, rgba(54, 75, 93, 0.24), transparent 42%),
        #10141d;
    }}

    .page {{
      position: relative;
      display: flex;
      min-height: 100vh;
      flex-direction: column;
      align-items: center;
      padding: 30px 24px 20px;
      isolation: isolate;
    }}

    .page::before, .page::after {{
      position: fixed;
      z-index: -1;
      width: 240px;
      height: 240px;
      border: 1px solid rgba(244, 180, 95, 0.13);
      border-radius: 50%;
      content: "";
      pointer-events: none;
    }}

    .page::before {{
      top: 16%;
      right: max(5vw, calc((100vw - 1180px) / 2));
      box-shadow: 0 0 90px rgba(244, 180, 95, 0.09), inset 0 0 70px rgba(244, 180, 95, 0.05);
    }}

    .page::after {{
      top: calc(16% + 28px);
      right: max(calc(5vw - 34px), calc((100vw - 1180px) / 2 - 34px));
      width: 308px;
      height: 178px;
      transform: rotate(-24deg);
    }}

    header, main, footer {{ width: min(100%, 1020px); }}

    header {{
      display: flex;
      align-items: center;
      gap: 11px;
      color: #ddd8cb;
      font-size: 0.76rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}

    .brand-mark {{
      display: grid;
      width: 36px;
      height: 36px;
      place-items: center;
      border: 1px solid rgba(244, 180, 95, 0.38);
      border-radius: 12px;
      color: var(--accent);
      font-size: 1.2rem;
    }}

    main {{
      display: grid;
      flex: 1;
      align-content: center;
      justify-items: start;
      padding: 72px 0 86px;
    }}

    .intro {{ max-width: 650px; }}

    .eyebrow {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin: 0 0 18px;
      color: var(--accent);
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
    }}

    .eyebrow::before {{
      width: 24px;
      height: 1px;
      background: currentColor;
      content: "";
    }}

    h1 {{
      max-width: 620px;
      margin: 0 0 16px;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(3rem, 7vw, 5.8rem);
      font-weight: 500;
      letter-spacing: -0.055em;
      line-height: 1.02;
    }}

    h1 span {{ color: var(--accent); font-style: italic; }}

    .subtitle {{
      max-width: 480px;
      margin: 0 0 36px;
      color: var(--muted);
      font-size: 1rem;
      line-height: 1.7;
    }}

    .fact-card {{
      width: min(100%, 700px);
      padding: clamp(24px, 5vw, 42px);
      border: 1px solid rgba(245, 242, 234, 0.12);
      border-radius: 22px;
      background: linear-gradient(135deg, rgba(34, 40, 51, 0.92), rgba(25, 30, 40, 0.86));
      box-shadow: 0 28px 90px rgba(0, 0, 0, 0.28), inset 0 1px rgba(255, 255, 255, 0.04);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }}

    .card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 32px;
    }}

    .section-label {{
      color: #dfd9cb;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.13em;
      text-transform: uppercase;
    }}

    .category {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      max-width: 65%;
      padding: 8px 12px;
      border: 1px solid rgba(244, 180, 95, 0.23);
      border-radius: 999px;
      background: rgba(244, 180, 95, 0.08);
      color: #f4c783;
      font-size: 0.72rem;
      line-height: 1.35;
      text-align: right;
    }}

    .category::before {{
      flex: 0 0 auto;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 10px rgba(244, 180, 95, 0.7);
      content: "";
    }}

    .fact {{
      margin: 0;
      color: #f4f0e7;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(1.2rem, 2.5vw, 1.55rem);
      line-height: 1.75;
      overflow-wrap: anywhere;
      white-space: pre-wrap;
    }}

    .card-bottom {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      margin-top: 32px;
      padding-top: 22px;
      border-top: 1px solid rgba(245, 242, 234, 0.11);
    }}

    .source-note {{
      max-width: 360px;
      margin: 0;
      color: var(--muted);
      font-size: 0.76rem;
      line-height: 1.55;
    }}

    .actions {{ display: flex; flex: 0 0 auto; gap: 10px; }}

    .button {{
      display: inline-flex;
      min-height: 42px;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 0 15px;
      border: 1px solid rgba(245, 242, 234, 0.18);
      border-radius: 10px;
      color: #f2eee6;
      font: inherit;
      font-size: 0.8rem;
      font-weight: 600;
      text-decoration: none;
      transition: transform 160ms ease, background-color 160ms ease, border-color 160ms ease;
    }}

    .button:hover {{ transform: translateY(-2px); }}
    .button:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 3px; }}
    .button-copy {{ background: rgba(255, 255, 255, 0.035); cursor: pointer; }}
    .button-copy:hover {{ background: rgba(255, 255, 255, 0.09); }}

    .button-new {{
      border-color: var(--accent);
      background: var(--accent);
      color: #20170e;
    }}

    .button-new:hover {{ background: #ffc779; }}
    .button svg {{ width: 15px; height: 15px; }}
    .copy-status {{ min-height: 1.2em; margin: 12px 0 0; color: #f4c783; font-size: 0.78rem; }}

    footer {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      color: #818794;
      font-size: 0.72rem;
      line-height: 1.5;
    }}

    footer span:last-child {{ text-align: right; }}

    @media (max-width: 600px) {{
      .page {{ padding: 20px 18px 16px; }}
      main {{ padding: 60px 0; }}
      .subtitle {{ margin-bottom: 26px; }}
      .fact-card {{ border-radius: 18px; }}
      .card-top {{ align-items: flex-start; flex-direction: column; margin-bottom: 25px; }}
      .category {{ max-width: 100%; text-align: left; }}
      .card-bottom {{ align-items: stretch; flex-direction: column; }}
      .actions {{ display: grid; grid-template-columns: 1fr 1fr; }}
      footer {{ flex-direction: column; gap: 6px; }}
      footer span:last-child {{ text-align: left; }}
      .page::before {{ top: 20%; right: -110px; }}
      .page::after {{ top: calc(20% + 28px); right: -144px; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{
        scroll-behavior: auto !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <span class="brand-mark" aria-hidden="true">i</span>
      <span>A little knowledge, every day</span>
    </header>

    <main>
      <section class="intro" aria-labelledby="page-title">
        <p class="eyebrow">Curiosity, delivered</p>
        <h1 id="page-title">The world is full of <span>surprises.</span></h1>
        <p class="subtitle">Take a minute to discover something unexpected. Here's a fresh fact, picked just for you.</p>
      </section>

      <article class="fact-card" aria-labelledby="fact-heading">
        <div class="card-top">
          <span class="section-label" id="fact-heading">Your fact</span>
          <span class="category">{safe_category}</span>
        </div>
        <p class="fact" id="fact-text">{safe_fact}</p>
        <div class="card-bottom">
          <p class="source-note">AI can make mistakes. Treat this as a starting point and check a trusted source for important facts.</p>
          <div class="actions">
            <button class="button button-copy" id="copy-fact" type="button" aria-label="Copy this fact">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <rect x="8" y="8" width="12" height="12" rx="2"></rect>
                <path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"></path>
              </svg>
              Copy
            </button>
            <a class="button button-new" href="/" aria-label="Generate another fact">
              Another fact <span aria-hidden="true">&rarr;</span>
            </a>
          </div>
        </div>
        <p class="copy-status" id="copy-status" role="status" aria-live="polite"></p>
      </article>
    </main>

    <footer>
      <span>Made to make curiosity a daily habit.</span>
      <span>Generated with Amazon Bedrock Nova Lite.</span>
    </footer>
  </div>

  <script>
    const copyButton = document.getElementById("copy-fact");
    const factText = document.getElementById("fact-text").textContent;
    const copyStatus = document.getElementById("copy-status");

    copyButton.addEventListener("click", async () => {{
      try {{
        await navigator.clipboard.writeText(factText);
        copyStatus.textContent = "Fact copied to your clipboard.";
      }} catch (error) {{
        console.error("Could not copy the fact to the clipboard.", error);
        copyStatus.textContent = "Copying is unavailable in this browser. You can select and copy the fact instead.";
      }}
    }});
  </script>
</body>
</html>"""


def handler(_event, _context):
    try:
        fact_text, category = generate_fact()
        page = build_html_page(fact_text, category)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Cache-Control": "no-store",
            },
            "body": page,
        }
    except Exception:
        logger.exception("Unable to generate the fact page.")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Cache-Control": "no-store",
            },
            "body": """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Fact unavailable</title></head>
<body style="margin:0;padding:48px 24px;background:#10141d;color:#f5f2ea;font:16px/1.6 system-ui,sans-serif">
  <main style="max-width:620px;margin:10vh auto">
    <p style="color:#f4b45f;font-size:.75rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase">A little pause</p>
    <h1 style="font-family:Georgia,serif;font-size:2.5rem">We couldn't find a fact right now.</h1>
    <p style="color:#a4a9b5">Please try again in a moment. If the problem continues, the site owner can check the Lambda logs.</p>
    <a style="color:#f4b45f" href="/">Try again</a>
  </main>
</body>
</html>""",
        }
