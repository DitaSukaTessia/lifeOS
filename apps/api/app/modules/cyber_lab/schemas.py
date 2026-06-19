from pydantic import BaseModel


class ToolInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str  # "recon" | "web" | "network"


class ScanResult(BaseModel):
    tool: str
    target: str
    output: str
    duration_ms: int


class CVEItem(BaseModel):
    id: str
    description: str
    severity: str  # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    score: float
    published: str
