import asyncio

from aioheleket import HeleketClient, RequestConfig


async def main() -> None:
    """
    EN:
    Demonstrating the creation of a ``HeleketClient`` with HTTP request settings via a ``RequestConfig`` object.

    ``RequestConfig`` parameters (passed to the client's ``config`` parameter):

    ``timeout_s`` (float): total request timeout in seconds (default 20.0)
    ``max_retries`` (int): number of retry attempts for network errors (default 2)
    ``retry_backoff_s`` (float): base delay before retrying (exponential backoff; default 0.25)
    ``connector_limit`` (int): maximum total number of connections in the pool (default 100)
    ``connector_limit_per_host`` (int): maximum number of connections per single host (default 50)
    ``ttl_dns_cache`` (int): time-to-live for DNS cache entries in seconds (default 300)

    In the example below, ``max_retries=4`` and ``connector_limit=80`` are overridden.


    RU:
    Демонстрация создания клиента ``HeleketClient`` с настройками обработки HTTP-запросов через объект ``RequestConfig``.

    Параметры ``RequestConfig`` (передаются в параметр ``config`` клиента):

    ``timeout_s`` (float): общий таймаут запроса в секундах (по умолчанию 20.0)
    ``max_retries`` (int): количество повторных попыток при сетевых ошибках (по умолчанию 2)
    ``retry_backoff_s`` (float): базовая задержка перед повторной попыткой (экспоненциальный рост; по умолчанию 0.25)
    ``connector_limit`` (int): максимальное общее количество соединений в пуле (по умолчанию 100)
    ``connector_limit_per_host`` (int): максимальное количество соединений на один хост (по умолчанию 50)
    ``ttl_dns_cache`` (int): время жизни записей DNS‑кэша в секундах (по умолчанию 300)

    В примере ниже переопределены значения ``max_retries=4`` и ``connector_limit=80``.
    """
    client = HeleketClient(
        merchant_id="<id>",
        payment_api_key="<key>",
        config=RequestConfig(
            max_retries=4,
            connector_limit=80
        )
    )
    ...

    await client.close_session()


if __name__ == "__main__":
    asyncio.run(main())
