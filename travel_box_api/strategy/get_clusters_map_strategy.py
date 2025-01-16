#!/bin/python3
from travel_box_api.strategy.strategy import Strategy

from travel_box_api.utils.get_map_service import get_map


class GetClusterMapStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "012"

    def process(self):
        return get_map()
