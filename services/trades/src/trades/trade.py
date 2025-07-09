from datetime import datetime, timezone

from pydantic import BaseModel


class Trade(BaseModel):
    product_id: str
    price: float
    quantity: float
    timestamp: str
    timestamp_ms: int

    def to_dict(self) -> dict:
        return self.model_dump()

    @staticmethod
    def convert_timestamp_to_iso_format(timestamp_sec: int) -> str:
        """
        Convert a timestamp in seconds to a string in ISO format

        Args:
            timestamp_sec (int): The timestamp in seconds

        Returns:
            str: The timestamp in ISO format

        Example:
            convert_timestamp_to_datetime(1609459200)
            '2021-01-01T00:00:00Z'
        """
        dt = datetime.fromtimestamp(timestamp_sec, tz=timezone.utc)
        return dt.isoformat().replace('+00:00', 'Z')

    @staticmethod
    def iso_format_to_timestamp(iso_format: str) -> int:
        """
        Convert a timestamp in ISO format to a timestamp in seconds

        Args:
            iso_format (str): The timestamp in ISO format

        Returns:
            int: The timestamp in seconds

        Example:
            iso_format_to_timestamp('2021-01-01T00:00:00Z')
            1609459200
        """
        dt = datetime.fromisoformat(iso_format)
        return int(dt.timestamp())

    @classmethod
    def from_kraken_rest_api_response(
        cls,
        product_id: str,
        price: float,
        quantity: float,
        timestamp_sec: int
    ) -> 'Trade':
        """
        Create a Trade object from the response of the Kraken REST API  
        """
        return cls(
            product_id=product_id,
            price=price,
            quantity=quantity,
            timestamp=cls.convert_timestamp_to_iso_format(timestamp_sec),
            timestamp_ms=int(timestamp_sec * 1000)
        )

    @classmethod
    def from_kraken_websocket_response(
        cls,
        product_id: str,
        price: float,
        quantity: float,
        timestamp: str
    ) -> 'Trade':
        """
        Create a Trade object from the response of the Kraken Websocket API
        """
        return cls(
            product_id=product_id,
            price=price,
            quantity=quantity,
            timestamp=timestamp,
            timestamp_ms=cls.iso_format_to_timestamp(timestamp)
        )
