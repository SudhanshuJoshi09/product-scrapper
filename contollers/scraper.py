from models.requests import ScrapeRequest
from fastapi import APIRouter


scrape_router = APIRouter()


@scrape_router.post("/scrape/")
async def scrape_request(req: ScrapeRequest):
    return {"message": "Welcome home"}


@scrape_router.get("/scrape/{request_id}")
async def get_request_details(request_id: int):
    return {"message": "New request"}
