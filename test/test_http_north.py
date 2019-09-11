# -*- coding: utf-8 -*-

# FLEDGE_BEGIN
# See: http://fledge.readthedocs.io/
# FLEDGE_END

from unittest.mock import patch
from aiohttp import web
from aiohttp.test_utils import unused_port
import pytest

from python.fledge.plugins.north.http_north import http_north
from python.fledge.plugins.north.http_north.http_north import HttpNorthPlugin

__author__ = "Ashish Jabble"
__copyright__ = "Copyright (c) 2017 OSIsoft, LLC"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"


_HOST = '127.0.0.1'
_PORT = unused_port()
_URL = 'http://{}:{}/sensor-reading'.format(_HOST, _PORT)
_HTTPS_URL = 'https://{}:{}/sensor-reading'.format(_HOST, _PORT)


class FakeServer:

    def __init__(self, *, loop):
        self.loop = loop
        self.app = web.Application(loop=loop)
        self.app.router.add_routes([
            web.post('/sensor-reading', self.receive_payload)
        ])
        self.handler = None
        self.server = None

    async def start(self, secure=False):
        self.handler = self.app.make_handler()
        ssl_ctx = None
        if secure:
            ssl_ctx = None  # TODO: set the ssl context with self signed certificates
        self.server = await self.loop.create_server(self.handler, _HOST, _PORT, ssl=ssl_ctx)

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()
        await self.app.shutdown()
        await self.handler.shutdown()
        await self.app.cleanup()

    async def receive_payload(self, request):
        body = await request.json()
        return web.json_response(body)


def test_plugin_contract():
    assert callable(getattr(http_north, 'plugin_info'))
    assert callable(getattr(http_north, 'plugin_init'))
    assert callable(getattr(http_north, 'plugin_send'))
    assert callable(getattr(http_north, 'plugin_shutdown'))
    assert callable(getattr(http_north, 'plugin_reconfigure'))


def test_plugin_info():
    assert http_north.plugin_info() == {
        'name': 'http',
        'version': '1.5.0',
        'type': 'north',
        'interface': '1.0',
        'config': http_north._DEFAULT_CONFIG
    }


def test_plugin_init():
    assert http_north.plugin_init(http_north._DEFAULT_CONFIG) == http_north._DEFAULT_CONFIG


@pytest.mark.asyncio
async def test_send_payload(event_loop):
    fake_server = FakeServer(loop=event_loop)
    await fake_server.start()

    payloads = [{'id': 1, 'asset_code': 'fogbench/temperature', 'read_key': '31e5ccbb-3e45-4038-95e9-7920834d0852', 'user_ts': '2018-02-26 12:12:54.171949+00', 'reading': {'ambient': 7, 'object': 28}}, {'id': 46, 'asset_code': 'fogbench/luxometer', 'read_key': '9b5beb10-5d87-4cd9-803e-02df7942139d', 'user_ts': '2018-02-27 11:46:57.368753+00', 'reading': {'lux': 92748.668}}]
    http_north.http_north = HttpNorthPlugin()
    http_north.http_north.event_loop = event_loop
    http_north.config = http_north._DEFAULT_CONFIG
    http_north.config['url']['value'] = _URL
    http_north.config['verifySSL']['value'] = "false"
    num_count = await http_north.http_north._send_payloads(payloads)
    assert 2 == num_count

    await fake_server.stop()


@pytest.mark.skip
async def test_send_bad_payload():
    pass


@pytest.mark.skip
async def test_send_payload_server_error():
    pass


@pytest.mark.asyncio
async def test_plugin_send(loop):

    async def mock_coro():
        return 2

    payload = [{'asset_code': 'fogbench/temperature', 'reading': {'ambient': 7, 'object': 28}, 'id': 14,
                'read_key': '31e5ccbb-3e45-4038-95e9-7920834d0852', 'user_ts': '2018-02-26 12:12:54.171949+00'},
               {'asset_code': 'fogbench/wall clock', 'reading': {'tick': 'tock'}, 'id': 20,
                'read_key': '277a6ac9-4351-4807-8cfd-a709d6c346cd', 'user_ts': '2018-02-26 12:12:54.172166+00'}]

    http_north.http_north = HttpNorthPlugin()
    http_north.http_north.event_loop = loop
    http_north.config = http_north._DEFAULT_CONFIG
    with patch.object(http_north.http_north, '_send_payloads', return_value=mock_coro()) as patch_send_payload:
        is_data_sent, new_last_object_id, num_sent = await http_north.plugin_send(data=http_north.config, payload=payload, stream_id=3)
        assert (True, 20, 2) == (is_data_sent, new_last_object_id, num_sent)


@pytest.mark.skip
def test_plugin_shutdown():
    pass
