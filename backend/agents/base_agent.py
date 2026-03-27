"""
Base Agent - Shared agent infrastructure
Provides the AI reasoning loop: Collect signals → Analyze → Act → Output
"""
import time
import json
from typing import Dict, Any, List
from datetime import datetime


class BaseAgent:
    """Base class for all AI agents with execution tracking"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.execution_log: List[Dict[str, Any]] = []
        self.start_time: float = 0

    def log_step(self, step: str, details: str, data: Any = None):
        """Log an execution step"""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "details": details,
            "data_summary": str(data)[:200] if data else None,
            "elapsed_ms": int((time.time() - self.start_time) * 1000)
        })

    def start_execution(self):
        """Start tracking execution"""
        self.start_time = time.time()
        self.execution_log = []
        self.log_step("init", f"{self.agent_name} started")

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary"""
        return {
            "agent": self.agent_name,
            "duration_ms": int((time.time() - self.start_time) * 1000),
            "steps": len(self.execution_log),
            "log": self.execution_log
        }

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent - must be overridden"""
        raise NotImplementedError
