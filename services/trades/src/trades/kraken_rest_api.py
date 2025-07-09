import json
import time

import requests
from loguru import logger
from pydantic import BaseModel
from trade import Trade
from websocket import create_connection


class KrakenRestAPI:
    URL = 'https://api.kraken.com/0/public/Trades'

    def __init__(
        self,
        product_ids: str,
        last_n_days: int
    ):
        self.product_ids = product_ids
        self.last_n_days = last_n_days
        self._is_done = False
        self.since_timestamp_ns = int(
            time.time_ns() - last_n_days * 24 * 60 * 60 * 1000000000
        )

    def get_trades(self) -> list[Trade]:
        """
        Sends a GET request to the Kraken API to get the trades for the given pair
        and since the given timestamp

        Returns:
            list[Trade]: List of trades for the given pair and since the given timestamp
        """
        headers = {'Accept': 'application/json'}

        for product_id in self.product_ids:
            params = {
                'pair': product_id,
                'since': self.since_timestamp_ns
            }
            try:
                response = requests.request(
                    'GET', self.URL, headers=headers, params=params)

            except requests.exceptions.SSLError as e:
                logger.error(f"The Kraken API is not reachable. Error: {e}")
                time.sleep(10)
                return []

            try:
                data = json.loads(response.text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse response as json: {e}")
                return []

            try:
                trades = data['result'][product_id]
            except KeyError as e:
                logger.error(
                    f"Failed to get trades for product_id {product_id}: {e}")
                return []

            # Transform the trades data into a list of Trade objects
            trades = [
                Trade.from_kraken_rest_api_response(
                    product_id=product_id,
                    price=trade[0],
                    quantity=trade[1],
                    timestamp_sec=trade[2],
                )
                for trade in trades
            ]

            self.since_timestamp_ns = int(float(data['result']['last']))

            if self.since_timestamp_ns > int(time.time_ns() - 10000000000):
                self._is_done = True

            return trades

    def is_done(self) -> bool:
        return self._is_done
