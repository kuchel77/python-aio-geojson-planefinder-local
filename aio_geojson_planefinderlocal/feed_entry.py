"""Flight Air Map feed entry."""
from datetime import datetime

import logging
import pytz

from aio_geojson_client.feed_entry import FeedEntry

_LOGGER = logging.getLogger(__name__)

class PlanefinderLocalFeedEntry(FeedEntry):
    """Flight Air Map Incidents feed entry."""

    def __init__(self, home_coordinates, feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)
    @property
    def title(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties("flightno")

    @property
    def external_id(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties("id")

    @property
    def call_sign(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties("call_sign")

    @property
    def flight_num(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties("flightno")

    @property
    def aircraft_registration(self) -> str:
        """Return the y of this entry."""
        return self._search_in_properties("reg")

    @property
    def aircraft_hex(self) -> str:
        """Return the y of this entry."""
        return self._search_in_properties("id")

    @property
    def aircraft_type(self) -> str:
        """Return the location of this entry."""
        return self._search_in_properties("type")

    @property
    def departure_airport(self) -> str:
        """Return the y of this entry."""
        return self._search_in_properties("airport_dep")

    @property
    def arrival_airport(self) -> str:
        """Return the location of this entry."""
        arrival_airport = self._search_in_properties("airport_final")
        return arrival_airport
    
    @property
    def altitude(self) -> str:
        """Return the location of this entry."""
        if self._search_in_properties("altitude") is not None:
            altitude = self._search_in_properties("altitude")
        else:
            altitude = None
        return altitude
    
    @property
    def selected_altitude(self) -> str:
        """Return the location of this entry."""
        if self._search_in_properties("altitude") is not None:
            selected_altitude = self._search_in_properties("selected_altitude")
        else:
            selected_altitude = None
        return selected_altitude

    @property
    def squawk(self) -> str:
        """Return the location of this entry."""
        squawk = self._search_in_properties("squawk")
        return squawk
   
    @property
    def heading(self) -> str:
        """Return the location of this entry."""
        heading = self._search_in_properties("heading")
        if heading is not None:
            return heading
        return None
    
    @property
    def speed(self) -> str:
        """Return the location of this entry."""
        speed = self._search_in_properties("speed")
        if speed is not None:
            return speed
        return None

    @property
    def ground_speed(self) -> str:
        """Return the location of this entry."""
        ground_speed = self._search_in_properties("ground_speed")
        if ground_speed is not None:
            return ground_speed
        return None

    @property
    def true_air_speed(self) -> str:
        """Return the location of this entry."""
        true_air_speed = self._search_in_properties("true_air_speed")
        if true_air_speed is not None:
            return true_air_speed
        return None

    @property
    def indicated_air_speed(self) -> str:
        """Return the location of this entry."""
        indicated_air_speed = self._search_in_properties("indicated_air_speed")
        if indicated_air_speed is not None:
            return indicated_air_speed
        return None

    @property
    def wind_speed(self) -> str:
        """Return the location of this entry."""
        wind_speed = self._search_in_properties("wind_speed")
        if wind_speed is not None:
            return wind_speed
        return None

    @property
    def wind_direction(self) -> str:
        """Return the location of this entry."""
        wind_direction = self._search_in_properties("wind_direction")
        if wind_direction is not None:
            return wind_direction
        return None

    @property
    def route(self) -> str:
        """Return the location of this entry."""
        route = self._search_in_properties("route")
        if route is not None:
            return route
        return None

    @property
    def publication_date(self) -> datetime:
        """Return the publication date of this entry."""
        last_update = self._search_in_properties("pos_update_time")
        if last_update is not None:
            publication_date = datetime.fromtimestamp(int(last_update), tz=pytz.utc)
            return publication_date 
        return None
