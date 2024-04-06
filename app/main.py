from fastapi import Depends, FastAPI

from .db.models import user
from .db.main import engine
from .router.v1 import usersRoute, authRoute, tokenRoute

app = FastAPI(

)
user.Base.metadata.create_all(bind=engine)

app.include_router(tokenRoute.router)
app.include_router(authRoute.router)
app.include_router(usersRoute.router)


@app.get("/", tags=["Main"])
async def read_root():
    return {"Hello": "World"}
