from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Ping/healthcheck")
def ping():
    return {"status": "ok"}
