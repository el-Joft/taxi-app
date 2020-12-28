from channels.routing import ProtocolTypeRouter

# Note: Nothing was passed in because, the it uses HTTP by default
application = ProtocolTypeRouter({})
