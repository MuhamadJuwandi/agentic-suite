# SecureRedact - Serverless PII Redaction API

A specialized, zero-cost API for redacting PII (Personally Identifiable Information) from text, designed for AI Agents. Built with FastAPI, Presidio, and SpaCy, optimized for Vercel Serverless Functions.

## Features
- **Zero Cost**: Runs on Vercel Hobby Tier.
- **Hybrid Detection**: Combines RegEx (for speed) and NLP (for context).
- **Stateless**: No data storage, fully privacy-compliant.

## Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Server**:
   ```bash
   uvicorn api.index:app --reload
   ```

3. **Test API**:
   Open `http://localhost:8000/docs` to see the Swagger UI.

## Deployment

1. Push this repo to GitHub.
2. Import project into Vercel.
3. Vercel will automatically detect `vercel.json` and deploy.

## API Usage

**POST** `/api/redact`

```json
{
  "text": "My phone number is 08123456789 and my name is Budi.",
  "anonymize": true
}
```
