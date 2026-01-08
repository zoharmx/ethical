# Ethica.AI Web Application

Enterprise-Grade Ethical AI Decision System - Modern Web Interface

## Features

- **Interactive Dashboard**: Analyze AI scenarios in real-time
- **10-Module Pipeline**: Comprehensive ethical analysis across 4 layers
- **Multi-Provider AI**: Leverage Gemini, Mistral, and DeepSeek
- **Beautiful UI**: Modern, responsive design with animations
- **Real-time Analysis**: Watch the analysis progress through all modules
- **Detailed Results**: Quantitative metrics and actionable recommendations

## Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS, Shadcn/ui components
- **Animations**: Framer Motion
- **Backend**: FastAPI (Python)
- **AI Framework**: Ethica Framework (multi-provider)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- API Keys for Gemini, Mistral, and DeepSeek

### Installation

1. Clone the repository:
```bash
git clone https://github.com/zoharmx/ethical.git
cd ethical/web-app
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
cd api
pip install -r requirements.txt
cd ..
```

4. Set up environment variables:
```bash
cp .env.example .env.local
```

Edit `.env.local` and add your API keys:
```
GEMINI_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
```

### Development

1. Start the backend API (in one terminal):
```bash
cd api
python main.py
```

2. Start the frontend (in another terminal):
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000)

### Production Build

```bash
npm run build
npm start
```

## Deployment

### Vercel (Recommended for Frontend)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard

### Backend Deployment

The FastAPI backend can be deployed to:
- **Vercel** (serverless)
- **Railway**
- **Render**
- **AWS Lambda**

## Project Structure

```
web-app/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Landing page
│   │   ├── dashboard/
│   │   │   └── page.tsx      # Analysis dashboard
│   │   ├── api/
│   │   │   └── analyze/
│   │   │       └── route.ts  # API route handler
│   │   └── layout.tsx        # Root layout
│   ├── components/
│   │   └── ui/               # Reusable UI components
│   ├── lib/
│   │   └── utils.ts          # Utility functions
│   └── styles/
│       └── globals.css       # Global styles
├── api/
│   ├── main.py               # FastAPI backend
│   └── requirements.txt      # Python dependencies
└── public/                   # Static assets
```

## API Endpoints

### POST /api/analyze

Analyze an AI scenario:

**Request:**
```json
{
  "action": "Deploy AI system...",
  "context": "Company proposes...",
  "stakeholders": ["Users", "Company", "Society"],
  "name": "Scenario Name"
}
```

**Response:**
```json
{
  "scenario_id": "ETH-xxxxx",
  "timestamp": "2025-01-06T...",
  "decision": {
    "approved": true,
    "approval_type": "CONDITIONAL",
    "confidence": 0.98,
    "reasoning": "...",
    "actions": [...],
    "conditions": [...]
  },
  ...
}
```

## Features in Detail

### Strategic Layer
- Purpose validation
- Insight generation
- Multi-perspective context analysis

### Operational Layer
- Opportunity identification
- Risk assessment
- Conflict resolution

### Tactical Layer
- Sustainability evaluation
- Implementation planning

### Execution Layer
- Integration synthesis
- Final decision orchestration

## License

Proprietary - Ethica.AI

## Support

For support, email support@ethica.ai or visit our documentation.
