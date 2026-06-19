from fastapi import APIRouter, Query

from app.modules.cyber_lab.schemas import ScanResult, ToolInfo
from app.modules.cyber_lab.service import get_mock_result, get_tools

router = APIRouter(prefix="/cyber-lab", tags=["cyber-lab"])


@router.get("/tools", response_model=list[ToolInfo])
def tools() -> list[ToolInfo]:
    return get_tools()


@router.get("/results", response_model=ScanResult)
def results(
    tool: str = Query(..., description="Tool ID"),
    target: str = Query(..., description="Target host or URL"),
) -> ScanResult:
    return get_mock_result(tool, target)
