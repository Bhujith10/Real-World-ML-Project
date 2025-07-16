# Create an Application instance with Kafka configs

from kraken_rest_api import KrakenRestAPI
from kraken_websocket_api import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application
from trade import Trade
from trades.config import config


def run(
    kafka_broker_address: str,
    kafka_topic_name: str,
    kraken_api: KrakenWebsocketAPI | KrakenRestAPI,
):
    """
    Produces a stream of trades to a Kafka topic.

    This function will take care of:

    1. Fetching events from the external API
    2. Serializing the event using the defined Topic
    3. Producing the message into the Kafka topic

    :param kafka_broker_address: The Kafka broker address
    :param kafka_topic_name: The name of the Kafka topic to produce to
    :param kraken_api: An instance of the Kraken API (either websocket or rest)
    """

    app = Application(
        broker_address=kafka_broker_address,
    )

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        while not kraken_api.is_done():
            # 1. Fetch the event from the external API
            events: list[Trade] = kraken_api.get_trades()
            # event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}

            for event in events:
                # 2. Serialize an event using the defined Topic
                message = topic.serialize(
                    key=event.product_id,
                    value=event.to_dict()
                )

                # 3. Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    key=message.key
                )

                # logger.info(f'Produced message to topic {topic.name}')
                logger.info(f'Trade {event.to_dict()} pushed to Kafa')

            # breakpoint()


if __name__ == '__main__':

    if config.live_or_historical == "live":
        api = KrakenWebsocketAPI(product_ids=config.product_ids)
    elif config.live_or_historical == "historical":
        api = KrakenRestAPI(product_ids=config.product_ids,
                            last_n_days=config.last_n_days)

    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        kraken_api=api,
    )

    # When running locally the kafka_broker_address should be localhost:9092

    # run(
    #     kafka_broker_address="localhost:9092",
    #     kafka_topic_name="tra
    # des",
    #     kraken_api=api,
    # )

    # kafka-e11b-kafka-bootstrap.kafka.svc.cluster.local:9092
