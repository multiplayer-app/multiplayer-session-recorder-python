import os

MULTIPLAYER_OTEL_DEFAULT_TRACES_EXPORTER_HTTP_URL = 'https://api.multiplayer.app/v1/traces'

MULTIPLAYER_OTEL_DEFAULT_LOGS_EXPORTER_HTTP_URL = 'https://api.multiplayer.app/v1/logs'

MULTIPLAYER_OTEL_DEFAULT_TRACES_EXPORTER_GRPC_URL = 'https://api.multiplayer.app:4317/v1/traces'

MULTIPLAYER_OTEL_DEFAULT_LOGS_EXPORTER_GRPC_URL = 'https://api.multiplayer.app:4317/v1/logs'

MULTIPLAYER_TRACE_DOC_PREFIX = 'd0cd0c'

MULTIPLAYER_TRACE_DEBUG_PREFIX = 'debdeb'

MULTIPLAYER_TRACE_CONTINUOUS_DEBUG_PREFIX = 'cdbcdb'

MULTIPLAYER_OTLP_KEY = os.environ.get("MULTIPLAYER_OTLP_KEY")

MULTIPLAYER_TRACE_DEBUG_SESSION_SHORT_ID_LENGTH = 8

MULTIPLAYER_BASE_API_URL = os.environ.get("MULTIPLAYER_BASE_API_URL") or 'https://api.multiplayer.app'

MASK_PLACEHOLDER = '***MASKED***'

ATTR_MULTIPLAYER_WORKSPACE_ID = 'multiplayer.workspace.id'

ATTR_MULTIPLAYER_PROJECT_ID = 'multiplayer.project.id'

ATTR_MULTIPLAYER_PLATFORM_ID = 'multiplayer.platform.id'

ATTR_MULTIPLAYER_CONTINUOUS_DEBUG_AUTO_SAVE = 'multiplayer.debugger.save'

ATTR_MULTIPLAYER_PLATFORM_NAME = 'multiplayer.platform.name'

ATTR_MULTIPLAYER_CLIENT_ID = 'multiplayer.client.id'

ATTR_MULTIPLAYER_INTEGRATION_ID = 'multiplayer.integration.id'

ATTR_MULTIPLAYER_SESSION_ID = 'multiplayer.session.id'

ATTR_MULTIPLAYER_HTTP_REQUEST_BODY = 'multiplayer.http.request.body'

ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY = 'multiplayer.http.response.body'

ATTR_MULTIPLAYER_HTTP_REQUEST_HEADERS = 'multiplayer.http.request.headers'

ATTR_MULTIPLAYER_HTTP_RESPONSE_HEADERS = 'multiplayer.http.response.headers'

ATTR_MULTIPLAYER_HTTP_RESPONSE_BODY_ENCODING = 'multiplayer.http.response.body.encoding'

ATTR_MULTIPLAYER_RPC_REQUEST_MESSAGE = 'multiplayer.rpc.request.message'

ATTR_MULTIPLAYER_RPC_REQUEST_MESSAGE_ENCODING = 'multiplayer.rpc.request.message.encoding'

ATTR_MULTIPLAYER_RPC_RESPONSE_MESSAGE = 'multiplayer.rpc.response.message'

ATTR_MULTIPLAYER_GRPC_REQUEST_MESSAGE = 'multiplayer.rpc.grpc.request.message'

ATTR_MULTIPLAYER_GRPC_REQUEST_MESSAGE_ENCODING = 'multiplayer.rpc.request.message.encoding'

ATTR_MULTIPLAYER_GRPC_RESPONSE_MESSAGE = 'multiplayer.rpc.grpc.response.message'

ATTR_MULTIPLAYER_MESSAGING_MESSAGE_BODY = 'multiplayer.messaging.message.body'

ATTR_MULTIPLAYER_MESSAGING_MESSAGE_BODY_ENCODING = 'multiplayer.messaging.message.body.encoding'
