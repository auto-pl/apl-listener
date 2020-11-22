"""The following is an enumeration of the event types sent.

These events are derived from PS2 API events, but have been stripped
back and merged to simplify the information contained.

"""

import dataclasses
import datetime
from typing import Optional

__all__ = [
    'PlayerBlip',
    'RelativePlayerBlip',
    'OutfitBlip',
    'FacilityCapture',
    'FacilityDefence',
    'FacilityReset'
]


@dataclasses.dataclass(frozen=True)
class PlayerBlip:
    """Player blips allow associating a character with a facility.

    These events are sent for facility captures and defences, and are
    therefore quite reliable - for a short while.

    :param timestamp: UTC timestamp of the event
    :param character_id: Character to position
    :param facility_id: Facility to position the character at
    :param server_id: ID of the server the event took place on
    :param zone_id: ID of the continent of the base

    """

    timestamp: datetime.datetime
    character_id: int
    facility_id: int
    server_id: int
    zone_id: int


@dataclasses.dataclass(frozen=True)
class RelativePlayerBlip:
    """Relative player blips give relative positioning between players.

    This generally happens when players revive or kill each other. For
    kills, mines (both infantry and anti tank) are ignored.

    The order of the characters has no relevance. For consistency, the
    character with the lower character ID will always be character A.

    :param timestamp: UTC timestamp of the event
    :param character_a_id: Player A of the relation
    :param character_b_id: Player B of the relation
    :param server_id: ID of the server the event took place on
    :param zone_id: ID of the continent of the base

    """

    timestamp: datetime.datetime
    character_a_id: int
    character_b_id: int
    server_id: int
    zone_id: int


@dataclasses.dataclass(frozen=True)
class OutfitBlip:
    """An outfit blip is used to position outfits with facilities.

    One outfit blip is sent for every member's player blip, with extra
    blips being sent when an outfit captures a facility in its name.

    :param timestamp: UTC timestamp of the event
    :param outfit_id: Outfit to be blipped
    :param facility_id: Facility to blip the outfit at
    :param server_id: ID of the server the event took place on
    :param zone_id: ID of the continent of the base

    """

    timestamp: datetime.datetime
    outfit_id: int
    facility_id: int
    server_id: int
    zone_id: int


@dataclasses.dataclass(frozen=True)
class FacilityCapture:
    """A facility has been captured by an outfit.

    :param timestamp: UTC timestamp of the event
    :param facility_id: ID of the facility that was captured
    :param duration_held: Time that :attr:`old_faction` held the base for in seconds
    :param new_faction_id: Faction that captured the base
    :param old_faction_id: Faction that lost the base
    :param outfit_id: Capturing outfit, if any
    :param server_id: ID of the server the event took place on
    :param zone_id: ID of the continent of the base

    """

    timestamp: datetime.datetime
    facility_id: int
    duration_held: int
    new_faction_id: int
    old_faction_id: int
    outfit_id: Optional[int]
    server_id: int
    zone_id: int


@dataclasses.dataclass(frozen=True)
class FacilityDefence:
    """A facility has been defended by its current owner.

    :param timestamp: UTC timestamp of the event
    :param facility_id: ID of the facility that was defended
    :param faction_id: Faction that captured the base
    :param server_id: ID of the server the event took place on
    :param zone_id: ID of the continent of the base

    """

    timestamp: datetime.datetime
    facility_id: int
    faction_id: int
    server_id: int
    zone_id: int


@dataclasses.dataclass(frozen=True)
class FacilityReset:
    """A facility has been reset to another owner.

    This occurs after downtime, or if a continent immediately reopens
    after locking due to high population.

    :param timestamp: UTC timestamp of the event
    :param facility_id: ID of the facility that was reset
    :param faction_id: New owner of the facility
    :param server_id: ID of the server the event took place on
    :param zone_id: ID of the continent of the base

    """

    timestamp: datetime.datetime
    facility_id: int
    faction_id: int
    server_id: int
    zone_id: int
