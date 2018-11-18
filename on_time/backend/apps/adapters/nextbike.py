import requests

from lxml import etree

from .exceptions import SdkRequestError


class NextBikeSdk:
    API_BASE_URL = 'https://nextbike.net/maps/nextbike-live.xml'

    def bikes(self):
        response = requests.get(self.API_BASE_URL, params={'domains': 'vp'})
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise SdkRequestError()
        return self._extract_stations(response.content)

    def _extract_stations(self, xml_data):
        root = etree.fromstring(xml_data)
        return [station.attrib for station in root.cssselect('place')]
