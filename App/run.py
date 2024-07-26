from fastapi import FastAPI
import models
from database import engine
from router import user, post, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Home
@app.get('/', tags="Base Entry Point")
async def root():
    return {"msg" : "go to /docs to see whole info"}

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
