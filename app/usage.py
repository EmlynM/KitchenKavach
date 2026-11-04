from fastapi import APIRouter

router = APIRouter()

usage_data = {
    "requests": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "estimated_cost_usd": 0.0
}


@router.get("/usage")
def get_usage():
    return usage_data