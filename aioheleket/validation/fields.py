from typing import Annotated
from pydantic import Field, TypeAdapter, HttpUrl

OrderID128 = Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_-]+$")]
OrderID100 = Annotated[str, Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")]
HttpUrl255 = Annotated[HttpUrl, Field(min_length=6, max_length=255)]

order_id128_adapter = TypeAdapter(OrderID128)
order_id100_adapter = TypeAdapter(OrderID100)
http_url_adapter = TypeAdapter(HttpUrl255)
