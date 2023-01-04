"""Flight Air Map feed."""
import logging
from typing import Optional

from aio_geojson_client.feed import GeoJsonFeed
from aiohttp import ClientSession
import requests
import json
from json import JSONDecodeError
import geojson
from geojson import Feature, FeatureCollection

from .feed_entry import PlanefinderLocalFeedEntry
#from aio_geojson_planefinderlocal.feed_entry import PlanefinderLocalFeedEntry

UPDATE_OK = "OK"
UPDATE_OK_NO_DATA = "OK_NO_DATA"
UPDATE_ERROR = "ERROR"

_LOGGER = logging.getLogger(__name__)


class PlanefinderLocalFeed(GeoJsonFeed):
    """Flight Air Map feed."""

    def __init__(self,
                 websession: ClientSession,
                 coordinates,
                 url,
                 filter_radius=None):
        """Initialise this service."""
        super().__init__(websession,                         
                         coordinates,
                         url=url,
                         filter_radius=filter_radius)

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(home={}, url={}, radius={})>'.format(
            self.__class__.__name__, self._home_coordinates, self._url,
            self._filter_radius)

    def _new_entry(self, home_coordinates, feature, global_data):
        """Generate a new entry."""
        return PlanefinderLocalFeedEntry(home_coordinates, feature)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        filtered_entries = super()._filter_entries(entries)
        return filtered_entries

    def _extract_last_timestamp(self, feed_entries):
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(filter(
                None, [entry.publication_date for entry in feed_entries]),
                           reverse=True)
            if len(dates) > 0:
                return dates[0]
        return None

    def _extract_from_feed(self, feed) -> Optional:
        """Extract global metadata from feed."""
        return None

    async def _update_internal(
        self, filter_function):
        """Update from external source and return filtered entries."""
        status, data = await self._fetch()
        if status == UPDATE_OK:
            if data:
                """Tranform json to GEOJson"""
                output = {}
                output['type'] = 'FeatureCollection'
                output['minimal'] = 'true'
                output['sqt'] = '0'

                features = []

                for k,v in data.items():
                    if k == 'aircraft':
                        for x in v:
                            if 'lat' in v[x] and 'lon' in v[x]:
                                print(x)
                                feature = {}
                                feature['type'] = 'Feature'
                                feature['id'] = x
                                
                                geometry = {}
                                geometry['type'] = 'Point'
                                coordinates = []
                                coordinates.append(v[x]['lon'])
                                coordinates.append(v[x]['lat'])
                                geometry['coordinates'] = coordinates

                                feature['geometry'] = geometry
                                properties = {}
                                for prop in v[x]:
                                    properties[prop] = v[x][prop]
                                    if prop == 'route':
                                        properties['airport_dep'] = v[x][prop].split('-')[0]
                                        properties['airport_final'] = v[x][prop].split('-')[-1]
                                properties['id'] = x
                                feature['properties'] = properties
                                features.append(feature)

                output['features'] = features
                data = geojson.loads(json.dumps(output))
            if data:
                entries = []
                global_data = self._extract_from_feed(data)
                # Extract data from feed entries.
                if type(data) is Feature:
                    entries.append(
                        self._new_entry(self._home_coordinates, data, global_data)
                    )
                elif type(data) is FeatureCollection:
                    for feature in data.features:
                        entries.append(
                            self._new_entry(
                                self._home_coordinates, feature, global_data
                            )
                        )
                else:
                    _LOGGER.warning(f"Unsupported GeoJSON object found: {type(data)}")
                filtered_entries = filter_function(entries)
                self._last_timestamp = self._extract_last_timestamp(filtered_entries)
                return UPDATE_OK, filtered_entries
            else:
                # Should not happen.
                return UPDATE_OK, None
        elif status == UPDATE_OK_NO_DATA:
            # Happens for example if the server returns 304
            return UPDATE_OK_NO_DATA, None
        else:
            # Error happened while fetching the feed.
            self._last_timestamp = None
            return UPDATE_ERROR, None