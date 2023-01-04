"""Feed Manager for Flight Air Map Incidents feed."""
from aio_geojson_client.feed_manager import FeedManagerBase
from aiohttp import ClientSession
from typing import Optional
from .feed import PlanefinderLocalFeed

class PlanefinderLocalFeedManager(FeedManagerBase):
    """Feed Manager for Flight Air Map feed."""

    def __init__(self,
                 websession: ClientSession,
                 generate_callback,
                 update_callback,
                 remove_callback,
                 coordinates=None,
                 feed_url=None,
                 filter_radius=None):
        """Initialize the Flight Air Map Manager."""
        feed = PlanefinderLocalFeed(
            websession,
            coordinates,
            feed_url,
            filter_radius)
        super().__init__(feed,
                         generate_callback,
                         update_callback,
                         remove_callback)

    def _update_internal(self, status: str, feed_entries):
        """Update the feed and then update connected entities."""

        if status == UPDATE_OK:
            print("here")
            _LOGGER.debug("Data retrieved %s", feed_entries)
            # Keep a copy of all feed entries for future lookups by entities.
            self.feed_entries = {entry.external_id: entry for entry in feed_entries}
            # Record current time of update.
            self._last_update = datetime.now()
            # For entity management the external ids from the feed are used.
            feed_external_ids = set(self.feed_entries)
            remove_external_ids = self._managed_external_ids.difference(
                feed_external_ids
            )
            self._remove_entities(remove_external_ids)
            update_external_ids = self._managed_external_ids.intersection(
                feed_external_ids
            )
            self._update_entities(update_external_ids)
            create_external_ids = feed_external_ids.difference(
                self._managed_external_ids
            )
            self._generate_new_entities(create_external_ids)
        elif status == UPDATE_OK_NO_DATA:
            _LOGGER.debug("Update successful, but no data received from %s", self._feed)
        else:
            _LOGGER.warning(
                "Update not successful, no data received from %s", self._feed
            )
            # Remove all entities.
            self._remove_entities(self._managed_external_ids.copy())
            # Remove all feed entries and managed external ids.
            self.feed_entries.clear()
            self._managed_external_ids.clear()

    def update(self):
        """Update the feed and then update connected entities."""
        status, feed_entries = self._feed.update()
        self._update_internal(status, feed_entries)

    def update_override(self, filter_overrides):
        """Update the feed and then update connected entities."""
        status, feed_entries = self._feed.update_override(
            filter_overrides=filter_overrides
        )
        self._update_internal(status, feed_entries)
