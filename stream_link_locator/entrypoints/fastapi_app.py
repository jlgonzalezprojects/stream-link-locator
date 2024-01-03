from fastapi import FastAPI

from stream_link_locator.presentation.rest import channels

app = FastAPI()
app.include_router(channels.router)
