from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer

import pytest

from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken

from taxi.routing import application

TEST_CHANNEL_LAYERS = {
  'default': {
    'BACKEND': 'channels.layers.InMemoryChannelLayer',
  },
}



@database_sync_to_async
def create_user(username, password):
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    access = AccessToken.for_user(user)
    return user, access

@pytest.mark.asyncio
# we need to add the below to be able to access the database
@pytest.mark.django_db(transaction=True) # new
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        # making settings to use default django in mermory instead of redis
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        # call the created user which returns access token
        _, access = await create_user('test.user@example.com', 'pAssw0rd')
        communicator = WebsocketCommunicator(
            application=application,
            # path='/taxi/' # without token
            path=f'/taxi/?token={access}' # with token
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

    # test connection fail without a valid token
    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is False
