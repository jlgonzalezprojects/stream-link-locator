from typing import Optional, List

from fastapi import APIRouter, Security
from pydantic import BaseModel

from stream_link_locator.bootstrap import bootstrap
from stream_link_locator.domain.commands import LoadChannels
from stream_link_locator.presentation.security import get_api_key

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
    dependencies=[Security(get_api_key)],
    responses={404: {"description": "Not found"}},
)


class LoadChannelsPayload(BaseModel):
    source: Optional[str] = None


class ChannelType(BaseModel):
    id: int
    name: str
    url: str


bus = bootstrap()


@router.post("/load", status_code=201)
async def load_channels(
    payload: LoadChannelsPayload,
):
    """Load channels"""
    bus.handle(LoadChannels(source=payload.source))
    return {"message": f"Channels loaded from {payload.source}"}


@router.get("/")
async def get_channels() -> List[ChannelType]:
    """Get channels"""
    with bus.uow:
        channels = bus.uow.channels.get_all()
        return [
            ChannelType(id=channel.id, name=channel.name, url=channel.url)
            for channel in channels
        ]
