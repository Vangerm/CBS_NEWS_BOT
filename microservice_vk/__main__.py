import asyncio
import logging.config

from microservice_vk.loger.logging_settings import logging_config
from microservice_vk.config_data.config import load_config
from microservice_vk.utils.nats_connect import connect_to_nats
from microservice_vk.utils.start_consumer import start_get_vk_post


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info('Starting microservice')

    # Получаем конфигурационные данные
    config = load_config()

    # Подключаемся к NATS
    nc, js = await connect_to_nats(servers=config.nats.servers)

    try:
        await start_get_vk_post(
            nc=nc,
            js=js,
            subject_consumer=config.delayed_consumer.subject_consumer,
            subject_publisher=config.delayed_consumer.subject_publisher,
            stream=config.delayed_consumer.stream,
            durable_name=config.delayed_consumer.durable_name
            )
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info('Stop microservice')
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем соединение с NATS
        await nc.close()
        logger.info('Connection to NATS closed')


if __name__ == '__main__':
    asyncio.run(main())
