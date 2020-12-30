
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TaxiConsumer(AsyncJsonWebsocketConsumer):
    groups = ['test'] # new
    async def connect(self):
        # this was changed to enable group connection
        # it enables any connection to the TaxiConsumer to enable subscription to the test group
        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )
        await self.accept()

    # The receive_json() function is responsible for processing all messages that come to the server.
    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'echo.message':
            await self.send_json({
                'type': message_type,
                'data': content.get('data'),
            })

    async def echo_message(self, message): # new
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    # async def disconnect(self, code):
    #     await super().disconnect(code)
    async def disconnect(self, code): # changed
        await self.channel_layer.group_discard(
            group='test',
            channel=self.channel_name
        )
        await super().disconnect(code)