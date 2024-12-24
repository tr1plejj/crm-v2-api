from fastapi.encoders import jsonable_encoder
from redis import Redis


class RedisTools:

    redis_conn = Redis()  # host='redis', port=6379

    @classmethod
    def set_product(cls, product_id: int, product_obj: dict):
        with cls.redis_conn as r:
            r.hset(
                name=f'product:{product_id}',
                mapping=jsonable_encoder(product_obj)
            )
            r.expire(f'product:{product_id}', 60)


    @classmethod
    def get_product(cls, product_id: int):
        with cls.redis_conn as r:
            data = r.hgetall(f'product:{product_id}')
            decoded_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}
            return decoded_data

    @classmethod
    def set_order(cls, order_id: int, order_obj: dict):
        with cls.redis_conn as r:
            r.hset(
                name=f'order:{order_id}',
                mapping=jsonable_encoder(order_obj)
            )
            r.expire(f'order:{order_id}', 60)

    @classmethod
    def get_order(cls, order_id: int):
        with cls.redis_conn as r:
            data = r.hgetall(f'order:{order_id}')
            decoded_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}
            return decoded_data