import hashlib
import logging

import elastic_transport
import elasticsearch
from elasticsearch import AsyncElasticsearch

from mangamix.settings import ES_INDEX, ES_HOST, ES_USER, ES_PASSWORD, MMX_SEARCH_SIZE, MMX_ANIMES


class Mangasearch:

    def __init__(self, start_index=-MMX_SEARCH_SIZE):
        self.logger = logging.getLogger(f'{__name__}.{__class__.__name__}')
        self.es = AsyncElasticsearch(hosts=ES_HOST, http_auth=(ES_USER, ES_PASSWORD), retry_on_timeout=True)
        self.num = start_index

    async def get_next_animes(self) -> list[str]:
        if len(MMX_ANIMES) > 0:
            return MMX_ANIMES
        self.logger.info(f'Try to get animes')
        try:
            response = await self.es.search(index=ES_INDEX, size=MMX_SEARCH_SIZE, from_=self.__get_anime_index())
            hits = response.body['hits']['hits']
            self.logger.info(f'Found {len(hits)} animes from ES')
            if len(hits) > 0:
                return Mangasearch.__get_anime_names(hits)
        except (elastic_transport.ConnectionError, elasticsearch.AuthenticationException) as e:
            self.logger.warning(e)
        return []

    async def update_video(self, anime: str, video_url: str):
        upscript = {
            'script': {
                'source': 'if (!ctx._source.containsKey("video")) ctx._source.video = [];'
                          'if (!ctx._source.video.contains(params.value)) ctx._source.video.add(params.value)',
                'params': {
                    'value': video_url
                }
            }
        }
        try:
            anime_id = Mangasearch.hash_name(anime)
            response = await self.es.update(index=ES_INDEX, id=anime_id, body=upscript)
            self.logger.debug(response)
            self.logger.info(f'ES Document for anime "{anime}" (id: "{anime_id}") updated')
        except (elastic_transport.ConnectionError, elasticsearch.AuthenticationException) as e:
            self.logger.warning(e)

    def __get_anime_index(self):
        self.num += MMX_SEARCH_SIZE
        return self.num

    def reset_index(self):
        self.num = -MMX_SEARCH_SIZE
        self.logger.info(f'Index is reset')

    @staticmethod
    def hash_name(name: str):
        return hashlib.sha256(name.encode('utf-8')).hexdigest()

    @staticmethod
    def __get_anime_names(hits):
        return list(map(lambda hit: hit['_source']['name'], hits))
