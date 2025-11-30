# 🚗 AI Predictive Maintenance System

![Deployment Status](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/🚀%20Production%20Deployment/badge.svg)
![Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/🧪%20Tests/badge.svg)

An intelligent automotive predictive maintenance and fault diagnosis system powered by AI agents.

## ✨ Features

- 📊 Real-time vehicle telemetry analysis
- 🔧 AI-powered fault diagnosis
- 💬 Automated customer engagement
- 📅 Smart scheduling system
- ⭐ Customer feedback management
- 🏭 Manufacturing insights
- 🔒 UEBA security monitoring
- 🚨 Live alert system

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ..
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Development

```bash
# Terminal 1 - Frontend
cd frontend
npm run dev

# Terminal 2 - Backend
python backend_server.py
```

Visit `http://localhost:3000` for the frontend and `http://localhost:5000` for the API.

## 📦 Deployment

### Automated Deployment (Recommended)

1. **Configure GitHub Secrets:**
   Go to `Settings → Secrets and variables → Actions` and add:

   ```
   VERCEL_TOKEN=your_token
   VERCEL_ORG_ID=your_org_id
   VERCEL_PROJECT_ID=your_project_id
   RENDER_DEPLOY_HOOK_URL=your_webhook_url
   OPENAI_API_KEY=your_key
   ELEVENLABS_API_KEY=your_key
   ```
