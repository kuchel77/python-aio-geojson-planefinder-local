""" This is a test of the FlightAirMap feed """
import asyncio
from aiohttp import ClientSession
from aio_geojson_planefinderlocal import PlanefinderLocalFeed
async def main() -> None:
    """ Main function """
    async with ClientSession() as websession:
        # Home Coordinates: Latitude: -33.0, Longitude: 150.0
        # Filter radius: 50 km
        feed = PlanefinderLocalFeed(websession,
                                (-33.0, 150.0),
                                "http://192.168.0.245:30053/ajax/aircraft",
                                filter_radius=2000000)
        status, entries = await feed.update()
        print(status)
        print(entries)
        for entry in entries:
            print(entry.publication_date)
            print(entry.coordinates)
            print(entry.flight_num)
            print(entry.departure_airport,'-',entry.arrival_airport)
asyncio.get_event_loop().run_until_complete(main())
