from fastapi import APIRouter


user_router = APIRouter()


@user_router.post("/user/signup/")
async def signup():
    return {"message": "Welcome home"}

# Skipping this for now, just delete the token for signout
# @user_router.post("/user/signup/")
# async def signout(req: ScrapeRequest):
#     return {"message": "Welcome home"}


@user_router.post("/user/login/")
async def login():
    return {"message": "Welcome home"}
