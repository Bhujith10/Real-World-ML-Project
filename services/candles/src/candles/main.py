from loguru import logger
from quixstreams import Application


def run(
    # kafka parameters
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    # candles parameters
    candle_sec: int,
):
    """
    Transforms a stream of input trades into a stream of output candles.

    In 3 steps:
    - Ingests trade from the `kafka_input_topic`
    - Aggregates trades into candles
    - Produces candles to the `kafka_output_topic`

    Args:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic name
        kafka_output_topic (str): Kafka output topic name
        candle_sec (int): Candle duration in seconds

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
    )

    # input topic
    trades_topic = app.topic(kafka_input_topic, value_deserializer='json')
    # output topic
    candles_topic = app.topic(kafka_output_topic, value_serializer='json')

    # Step 1. Ingest trades from the input kafka topic
    # Create a Streaming DataFrame connected to the input Kafka topic
    sdf = app.dataframe(topic=trades_topic)

    # Step 2. Aggregate trades into candles
    # TODO: at the moment I am just printing it, to make sure this thing works.
    sdf = sdf.update(lambda message: logger.info(f'Input:  {message}'))

    # Step 3. Produce the candles to the output kafka topic
    sdf = sdf.to_topic(candles_topic)

    # Starts the streaming app
    app.run()


if __name__ == '__main__':
    run(
        kafka_broker_address='localhost:31234',
        kafka_input_topic='trades',
        kafka_output_topic='candles',
        candle_sec=60,
    )
