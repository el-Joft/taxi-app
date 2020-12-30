from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer

import pytest

from taxi.routing import application

TEST_CHANNEL_LAYERS = {
  'default': {
    'BACKEND': 'channels.layers.InMemoryChannelLayer',
  },
}

@pytest.mark.asyncio
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        # making settings to use default django in mermory instead of redis
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    # This create a message and send it to itself in an empty room
    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        # we send a message and expect to it to echo a response back to us
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    # test using a channel layer to broadcast messgae to a channel group
