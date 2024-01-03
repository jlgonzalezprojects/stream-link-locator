from typing import List

from bs4 import BeautifulSoup
from torpy.http.requests import tor_requests_session

from stream_link_locator.domain.models import Channel
from stream_link_locator.adapters.parsers.base_parser import BaseParser


class ElCanoParser(BaseParser):
    """ Parse the elcano website. """

    def parse(self) -> List[Channel]:
        """Parse the elcano url and return a list of channels"""
        parsed_channels = []
        with tor_requests_session() as session:
            response = session.get(self.url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, features="html.parser")
            for enlace in soup.find_all("a"):
                channel_link = str(enlace.get("href"))
                channel_name = enlace.text
                if channel_link.startswith("acestream://") and channel_name != "aquí":
                    channel = Channel(name=channel_name, url=channel_link)
                    parsed_channels.append(channel)
            return parsed_channels
