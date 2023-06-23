import os
from pydantic import BaseSettings, SecretStr


current_dir = os.path.dirname(__file__)


# class Config(BaseSettings):
#     BOT_TOKEN: SecretStr
#     API_TOKEN: SecretStr
#     MONGO_USERNAME: SecretStr
#     MONGO_PASSWORD: SecretStr
#     MONGO_CLUSTER: SecretStr
#     CURRENT_SCHEMA_VERSION: int
#
#     class Config:
#         env_file = os.path.abspath(os.path.join(current_dir, '.env'))
#         env_file_encoding = 'utf-8'
#
#
# config = Config()
