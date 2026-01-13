# Webhook Receiver Service (FastAPI)

A secure webhook receiver that validates signatures, stores payloads,
and prevents duplicate events using idempotency.

## Features
- POST /webhook endpoint
- Shared secret validation (X-Signature header)
- SQLite / PostgreSQL support
- Idempotent event handling
- Clean JSON responses

## Setup

### 1. Clone Repo
```bash
git clone <https://github.com/DeveloperAyaz7382/webhook-receiver.git>
cd webhook-receiver
