"""
RevOps AI - FastAPI Main Application
Multi-Agent B2B Sales Intelligence Platform
"""
import os
import sys
from dotenv import load_dotenv

# Load .env FIRST before any other imports
load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from routers.agents import router as agents_router
from routers.dashboard import router as dashboard_router
from websocket.manager import ws_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    print("🚀 RevOps AI Platform Starting...")
    print("📊 Mock CRM data loaded")
    print("🤖 AI Agents ready")
    print("🔌 WebSocket server active")

    # Check Gemini API status
    llm_provider = os.getenv("LLM_PROVIDER", "mock")
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if llm_provider == "gemini" and api_key:
        print(f"✨ Gemini AI: ACTIVE (key: ...{api_key[-8:]})")
    elif llm_provider == "gemini":
        print("⚠️  Gemini AI: KEY NOT SET — falling back to templates")
    else:
        print(f"📋 LLM Provider: {llm_provider} (template mode)")

    yield
    print("👋 RevOps AI Platform shutting down...")


app = FastAPI(
    title="RevOps AI Platform",
    description="AI-powered multi-agent system for B2B sales pipeline acceleration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents_router)
app.include_router(dashboard_router)


# WebSocket endpoint
@app.websocket("/ws/agent-status")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time agent status updates"""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for messages
            data = await websocket.receive_text()
            # Echo back or handle client messages
            await ws_manager.send_message(websocket, {
                "type": "ack",
                "message": f"Received: {data}"
            })
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "RevOps AI Platform",
        "version": "1.0.0",
        "agents": ["prospect", "deal_risk", "churn", "competitive"],
        "websocket": f"{len(ws_manager.active_connections)} active connections"
    }


@app.get("/")
async def root():
    return {
        "name": "RevOps AI Platform",
        "version": "1.0.0",
        "description": "AI-powered multi-agent B2B sales intelligence",
        "endpoints": {
            "dashboard": "/api/dashboard",
            "prospect_agent": "POST /api/prospect",
            "deal_risk_agent": "POST /api/deal-risk",
            "churn_agent": "POST /api/churn",
            "competitive_agent": "POST /api/competitive",
            "agent_runs": "/api/agent-runs",
            "leads": "/api/leads",
            "deals": "/api/deals",
            "accounts": "/api/accounts",
            "websocket": "ws://localhost:8000/ws/agent-status"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
