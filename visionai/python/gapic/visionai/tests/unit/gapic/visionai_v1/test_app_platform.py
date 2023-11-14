# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.location import locations_pb2
from visionai.python.gapic.visionai.visionai_v1.services.app_platform import AppPlatformAsyncClient
from visionai.python.gapic.visionai.visionai_v1.services.app_platform import AppPlatformClient
from visionai.python.gapic.visionai.visionai_v1.services.app_platform import pagers
from visionai.python.gapic.visionai.visionai_v1.services.app_platform import transports
from visionai.python.gapic.visionai.visionai_v1.types import annotations
from visionai.python.gapic.visionai.visionai_v1.types import common
from visionai.python.gapic.visionai.visionai_v1.types import platform
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2 # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return "foo.googleapis.com" if ("localhost" in client.DEFAULT_ENDPOINT) else client.DEFAULT_ENDPOINT


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert AppPlatformClient._get_default_mtls_endpoint(None) is None
    assert AppPlatformClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert AppPlatformClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert AppPlatformClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert AppPlatformClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert AppPlatformClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (AppPlatformClient, "grpc"),
    (AppPlatformAsyncClient, "grpc_asyncio"),
    (AppPlatformClient, "rest"),
])
def test_app_platform_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'visionai.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://visionai.googleapis.com'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.AppPlatformGrpcTransport, "grpc"),
    (transports.AppPlatformGrpcAsyncIOTransport, "grpc_asyncio"),
    (transports.AppPlatformRestTransport, "rest"),
])
def test_app_platform_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (AppPlatformClient, "grpc"),
    (AppPlatformAsyncClient, "grpc_asyncio"),
    (AppPlatformClient, "rest"),
])
def test_app_platform_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'visionai.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://visionai.googleapis.com'
        )


def test_app_platform_client_get_transport_class():
    transport = AppPlatformClient.get_transport_class()
    available_transports = [
        transports.AppPlatformGrpcTransport,
        transports.AppPlatformRestTransport,
    ]
    assert transport in available_transports

    transport = AppPlatformClient.get_transport_class("grpc")
    assert transport == transports.AppPlatformGrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (AppPlatformClient, transports.AppPlatformGrpcTransport, "grpc"),
    (AppPlatformAsyncClient, transports.AppPlatformGrpcAsyncIOTransport, "grpc_asyncio"),
    (AppPlatformClient, transports.AppPlatformRestTransport, "rest"),
])
@mock.patch.object(AppPlatformClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AppPlatformClient))
@mock.patch.object(AppPlatformAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AppPlatformAsyncClient))
def test_app_platform_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AppPlatformClient, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AppPlatformClient, 'get_transport_class') as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(api_audience="https://language.googleapis.com")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com"
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,use_client_cert_env", [
    (AppPlatformClient, transports.AppPlatformGrpcTransport, "grpc", "true"),
    (AppPlatformAsyncClient, transports.AppPlatformGrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (AppPlatformClient, transports.AppPlatformGrpcTransport, "grpc", "false"),
    (AppPlatformAsyncClient, transports.AppPlatformGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    (AppPlatformClient, transports.AppPlatformRestTransport, "rest", "true"),
    (AppPlatformClient, transports.AppPlatformRestTransport, "rest", "false"),
])
@mock.patch.object(AppPlatformClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AppPlatformClient))
@mock.patch.object(AppPlatformAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AppPlatformAsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_app_platform_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        options = client_options.ClientOptions(client_cert_source=client_cert_source_callback)
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
                with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=client_cert_source_callback):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch("google.auth.transport.mtls.has_default_client_cert_source", return_value=False):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [
    AppPlatformClient, AppPlatformAsyncClient
])
@mock.patch.object(AppPlatformClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AppPlatformClient))
@mock.patch.object(AppPlatformAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AppPlatformAsyncClient))
def test_app_platform_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=False):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
            with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_client_cert_source):
                api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (AppPlatformClient, transports.AppPlatformGrpcTransport, "grpc"),
    (AppPlatformAsyncClient, transports.AppPlatformGrpcAsyncIOTransport, "grpc_asyncio"),
    (AppPlatformClient, transports.AppPlatformRestTransport, "rest"),
])
def test_app_platform_client_client_options_scopes(client_class, transport_class, transport_name):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (AppPlatformClient, transports.AppPlatformGrpcTransport, "grpc", grpc_helpers),
    (AppPlatformAsyncClient, transports.AppPlatformGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
    (AppPlatformClient, transports.AppPlatformRestTransport, "rest", None),
])
def test_app_platform_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

def test_app_platform_client_client_options_from_dict():
    with mock.patch('visionai.python.gapic.visionai.visionai_v1.services.app_platform.transports.AppPlatformGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = AppPlatformClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (AppPlatformClient, transports.AppPlatformGrpcTransport, "grpc", grpc_helpers),
    (AppPlatformAsyncClient, transports.AppPlatformGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_app_platform_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "visionai.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=None,
            default_host="visionai.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  platform.ListApplicationsRequest,
  dict,
])
def test_list_applications(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListApplicationsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListApplicationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApplicationsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_applications_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        client.list_applications()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListApplicationsRequest()

@pytest.mark.asyncio
async def test_list_applications_async(transport: str = 'grpc_asyncio', request_type=platform.ListApplicationsRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.ListApplicationsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListApplicationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApplicationsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_applications_async_from_dict():
    await test_list_applications_async(request_type=dict)


def test_list_applications_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListApplicationsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        call.return_value = platform.ListApplicationsResponse()
        client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_applications_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListApplicationsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListApplicationsResponse())
        await client.list_applications(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_applications_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListApplicationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_applications(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_applications_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_applications(
            platform.ListApplicationsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_applications_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListApplicationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListApplicationsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_applications(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_applications_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_applications(
            platform.ListApplicationsRequest(),
            parent='parent_value',
        )


def test_list_applications_pager(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                    platform.Application(),
                ],
                next_page_token='abc',
            ),
            platform.ListApplicationsResponse(
                applications=[],
                next_page_token='def',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                ],
                next_page_token='ghi',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_applications(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Application)
                   for i in results)
def test_list_applications_pages(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                    platform.Application(),
                ],
                next_page_token='abc',
            ),
            platform.ListApplicationsResponse(
                applications=[],
                next_page_token='def',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                ],
                next_page_token='ghi',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_applications(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_applications_async_pager():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                    platform.Application(),
                ],
                next_page_token='abc',
            ),
            platform.ListApplicationsResponse(
                applications=[],
                next_page_token='def',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                ],
                next_page_token='ghi',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_applications(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, platform.Application)
                for i in responses)


@pytest.mark.asyncio
async def test_list_applications_async_pages():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_applications),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                    platform.Application(),
                ],
                next_page_token='abc',
            ),
            platform.ListApplicationsResponse(
                applications=[],
                next_page_token='def',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                ],
                next_page_token='ghi',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_applications(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  platform.GetApplicationRequest,
  dict,
])
def test_get_application(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Application(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
            state=platform.Application.State.CREATED,
            billing_mode=platform.Application.BillingMode.PAYG,
        )
        response = client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Application)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.state == platform.Application.State.CREATED
    assert response.billing_mode == platform.Application.BillingMode.PAYG


def test_get_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_application),
            '__call__') as call:
        client.get_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetApplicationRequest()

@pytest.mark.asyncio
async def test_get_application_async(transport: str = 'grpc_asyncio', request_type=platform.GetApplicationRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.Application(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
            state=platform.Application.State.CREATED,
            billing_mode=platform.Application.BillingMode.PAYG,
        ))
        response = await client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Application)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.state == platform.Application.State.CREATED
    assert response.billing_mode == platform.Application.BillingMode.PAYG


@pytest.mark.asyncio
async def test_get_application_async_from_dict():
    await test_get_application_async(request_type=dict)


def test_get_application_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_application),
            '__call__') as call:
        call.return_value = platform.Application()
        client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_application_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_application),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Application())
        await client.get_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_application_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Application()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_application_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_application(
            platform.GetApplicationRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_application_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Application()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Application())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_application_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_application(
            platform.GetApplicationRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.CreateApplicationRequest,
  dict,
])
def test_create_application(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application),
            '__call__') as call:
        client.create_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateApplicationRequest()

@pytest.mark.asyncio
async def test_create_application_async(transport: str = 'grpc_asyncio', request_type=platform.CreateApplicationRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_application_async_from_dict():
    await test_create_application_async(request_type=dict)


def test_create_application_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateApplicationRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_application_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateApplicationRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_application_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_application(
            parent='parent_value',
            application=platform.Application(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].application
        mock_val = platform.Application(name='name_value')
        assert arg == mock_val


def test_create_application_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_application(
            platform.CreateApplicationRequest(),
            parent='parent_value',
            application=platform.Application(name='name_value'),
        )

@pytest.mark.asyncio
async def test_create_application_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_application(
            parent='parent_value',
            application=platform.Application(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].application
        mock_val = platform.Application(name='name_value')
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_application_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_application(
            platform.CreateApplicationRequest(),
            parent='parent_value',
            application=platform.Application(name='name_value'),
        )


@pytest.mark.parametrize("request_type", [
  platform.UpdateApplicationRequest,
  dict,
])
def test_update_application(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application),
            '__call__') as call:
        client.update_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationRequest()

@pytest.mark.asyncio
async def test_update_application_async(transport: str = 'grpc_asyncio', request_type=platform.UpdateApplicationRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_application_async_from_dict():
    await test_update_application_async(request_type=dict)


def test_update_application_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateApplicationRequest()

    request.application.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'application.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_application_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateApplicationRequest()

    request.application.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'application.name=name_value',
    ) in kw['metadata']


def test_update_application_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_application(
            application=platform.Application(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].application
        mock_val = platform.Application(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_application_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_application(
            platform.UpdateApplicationRequest(),
            application=platform.Application(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_application_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_application(
            application=platform.Application(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].application
        mock_val = platform.Application(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_application_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_application(
            platform.UpdateApplicationRequest(),
            application=platform.Application(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  platform.DeleteApplicationRequest,
  dict,
])
def test_delete_application(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application),
            '__call__') as call:
        client.delete_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteApplicationRequest()

@pytest.mark.asyncio
async def test_delete_application_async(transport: str = 'grpc_asyncio', request_type=platform.DeleteApplicationRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_application_async_from_dict():
    await test_delete_application_async(request_type=dict)


def test_delete_application_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_application_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_application_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_application_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_application(
            platform.DeleteApplicationRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_application_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_application_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_application(
            platform.DeleteApplicationRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.DeployApplicationRequest,
  dict,
])
def test_deploy_application(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.deploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.deploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeployApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_deploy_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.deploy_application),
            '__call__') as call:
        client.deploy_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeployApplicationRequest()

@pytest.mark.asyncio
async def test_deploy_application_async(transport: str = 'grpc_asyncio', request_type=platform.DeployApplicationRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.deploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.deploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeployApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_deploy_application_async_from_dict():
    await test_deploy_application_async(request_type=dict)


def test_deploy_application_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeployApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.deploy_application),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.deploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_deploy_application_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeployApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.deploy_application),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.deploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_deploy_application_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.deploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.deploy_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_deploy_application_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.deploy_application(
            platform.DeployApplicationRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_deploy_application_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.deploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.deploy_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_deploy_application_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.deploy_application(
            platform.DeployApplicationRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.UndeployApplicationRequest,
  dict,
])
def test_undeploy_application(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undeploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.undeploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UndeployApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undeploy_application_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undeploy_application),
            '__call__') as call:
        client.undeploy_application()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UndeployApplicationRequest()

@pytest.mark.asyncio
async def test_undeploy_application_async(transport: str = 'grpc_asyncio', request_type=platform.UndeployApplicationRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undeploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.undeploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UndeployApplicationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undeploy_application_async_from_dict():
    await test_undeploy_application_async(request_type=dict)


def test_undeploy_application_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UndeployApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undeploy_application),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.undeploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_undeploy_application_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UndeployApplicationRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undeploy_application),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.undeploy_application(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_undeploy_application_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undeploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undeploy_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_undeploy_application_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undeploy_application(
            platform.UndeployApplicationRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_undeploy_application_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.undeploy_application),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undeploy_application(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_undeploy_application_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undeploy_application(
            platform.UndeployApplicationRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.AddApplicationStreamInputRequest,
  dict,
])
def test_add_application_stream_input(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.add_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.add_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.AddApplicationStreamInputRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_add_application_stream_input_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.add_application_stream_input),
            '__call__') as call:
        client.add_application_stream_input()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.AddApplicationStreamInputRequest()

@pytest.mark.asyncio
async def test_add_application_stream_input_async(transport: str = 'grpc_asyncio', request_type=platform.AddApplicationStreamInputRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.add_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.add_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.AddApplicationStreamInputRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_add_application_stream_input_async_from_dict():
    await test_add_application_stream_input_async(request_type=dict)


def test_add_application_stream_input_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.AddApplicationStreamInputRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.add_application_stream_input),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.add_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_add_application_stream_input_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.AddApplicationStreamInputRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.add_application_stream_input),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.add_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_add_application_stream_input_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.add_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.add_application_stream_input(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_add_application_stream_input_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_application_stream_input(
            platform.AddApplicationStreamInputRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_add_application_stream_input_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.add_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.add_application_stream_input(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_add_application_stream_input_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.add_application_stream_input(
            platform.AddApplicationStreamInputRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.RemoveApplicationStreamInputRequest,
  dict,
])
def test_remove_application_stream_input(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.remove_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.remove_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.RemoveApplicationStreamInputRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_remove_application_stream_input_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.remove_application_stream_input),
            '__call__') as call:
        client.remove_application_stream_input()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.RemoveApplicationStreamInputRequest()

@pytest.mark.asyncio
async def test_remove_application_stream_input_async(transport: str = 'grpc_asyncio', request_type=platform.RemoveApplicationStreamInputRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.remove_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.remove_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.RemoveApplicationStreamInputRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_remove_application_stream_input_async_from_dict():
    await test_remove_application_stream_input_async(request_type=dict)


def test_remove_application_stream_input_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.RemoveApplicationStreamInputRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.remove_application_stream_input),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.remove_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_remove_application_stream_input_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.RemoveApplicationStreamInputRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.remove_application_stream_input),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.remove_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_remove_application_stream_input_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.remove_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.remove_application_stream_input(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_remove_application_stream_input_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_application_stream_input(
            platform.RemoveApplicationStreamInputRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_remove_application_stream_input_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.remove_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.remove_application_stream_input(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_remove_application_stream_input_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.remove_application_stream_input(
            platform.RemoveApplicationStreamInputRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.UpdateApplicationStreamInputRequest,
  dict,
])
def test_update_application_stream_input(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationStreamInputRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_application_stream_input_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_stream_input),
            '__call__') as call:
        client.update_application_stream_input()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationStreamInputRequest()

@pytest.mark.asyncio
async def test_update_application_stream_input_async(transport: str = 'grpc_asyncio', request_type=platform.UpdateApplicationStreamInputRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationStreamInputRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_application_stream_input_async_from_dict():
    await test_update_application_stream_input_async(request_type=dict)


def test_update_application_stream_input_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateApplicationStreamInputRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_stream_input),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_application_stream_input_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateApplicationStreamInputRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_stream_input),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_application_stream_input(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_update_application_stream_input_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_application_stream_input(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_update_application_stream_input_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_application_stream_input(
            platform.UpdateApplicationStreamInputRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_update_application_stream_input_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_stream_input),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_application_stream_input(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_application_stream_input_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_application_stream_input(
            platform.UpdateApplicationStreamInputRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.ListInstancesRequest,
  dict,
])
def test_list_instances(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListInstancesResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstancesPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_instances_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        client.list_instances()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListInstancesRequest()

@pytest.mark.asyncio
async def test_list_instances_async(transport: str = 'grpc_asyncio', request_type=platform.ListInstancesRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.ListInstancesResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstancesAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_instances_async_from_dict():
    await test_list_instances_async(request_type=dict)


def test_list_instances_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListInstancesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        call.return_value = platform.ListInstancesResponse()
        client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_instances_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListInstancesRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListInstancesResponse())
        await client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_instances_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListInstancesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_instances(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_instances_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_instances(
            platform.ListInstancesRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_instances_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListInstancesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListInstancesResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_instances(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_instances_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_instances(
            platform.ListInstancesRequest(),
            parent='parent_value',
        )


def test_list_instances_pager(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                    platform.Instance(),
                ],
                next_page_token='abc',
            ),
            platform.ListInstancesResponse(
                instances=[],
                next_page_token='def',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                ],
                next_page_token='ghi',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_instances(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Instance)
                   for i in results)
def test_list_instances_pages(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                    platform.Instance(),
                ],
                next_page_token='abc',
            ),
            platform.ListInstancesResponse(
                instances=[],
                next_page_token='def',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                ],
                next_page_token='ghi',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_instances(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_instances_async_pager():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                    platform.Instance(),
                ],
                next_page_token='abc',
            ),
            platform.ListInstancesResponse(
                instances=[],
                next_page_token='def',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                ],
                next_page_token='ghi',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_instances(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, platform.Instance)
                for i in responses)


@pytest.mark.asyncio
async def test_list_instances_async_pages():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_instances),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                    platform.Instance(),
                ],
                next_page_token='abc',
            ),
            platform.ListInstancesResponse(
                instances=[],
                next_page_token='def',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                ],
                next_page_token='ghi',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_instances(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  platform.GetInstanceRequest,
  dict,
])
def test_get_instance(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_instance),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Instance(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
            instance_type=platform.Instance.InstanceType.STREAMING_PREDICTION,
            state=platform.Instance.State.CREATING,
        )
        response = client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Instance)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.instance_type == platform.Instance.InstanceType.STREAMING_PREDICTION
    assert response.state == platform.Instance.State.CREATING


def test_get_instance_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_instance),
            '__call__') as call:
        client.get_instance()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetInstanceRequest()

@pytest.mark.asyncio
async def test_get_instance_async(transport: str = 'grpc_asyncio', request_type=platform.GetInstanceRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_instance),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.Instance(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
            instance_type=platform.Instance.InstanceType.STREAMING_PREDICTION,
            state=platform.Instance.State.CREATING,
        ))
        response = await client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetInstanceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Instance)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.instance_type == platform.Instance.InstanceType.STREAMING_PREDICTION
    assert response.state == platform.Instance.State.CREATING


@pytest.mark.asyncio
async def test_get_instance_async_from_dict():
    await test_get_instance_async(request_type=dict)


def test_get_instance_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetInstanceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_instance),
            '__call__') as call:
        call.return_value = platform.Instance()
        client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_instance_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetInstanceRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_instance),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Instance())
        await client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_instance_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_instance),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Instance()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_instance(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_instance_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_instance(
            platform.GetInstanceRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_instance_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_instance),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Instance()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Instance())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_instance(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_instance_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_instance(
            platform.GetInstanceRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.CreateApplicationInstancesRequest,
  dict,
])
def test_create_application_instances(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateApplicationInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_application_instances_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application_instances),
            '__call__') as call:
        client.create_application_instances()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateApplicationInstancesRequest()

@pytest.mark.asyncio
async def test_create_application_instances_async(transport: str = 'grpc_asyncio', request_type=platform.CreateApplicationInstancesRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateApplicationInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_application_instances_async_from_dict():
    await test_create_application_instances_async(request_type=dict)


def test_create_application_instances_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateApplicationInstancesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application_instances),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_application_instances_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateApplicationInstancesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application_instances),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_create_application_instances_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_application_instances(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_create_application_instances_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_application_instances(
            platform.CreateApplicationInstancesRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_create_application_instances_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_application_instances(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_application_instances_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_application_instances(
            platform.CreateApplicationInstancesRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.DeleteApplicationInstancesRequest,
  dict,
])
def test_delete_application_instances(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteApplicationInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_application_instances_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application_instances),
            '__call__') as call:
        client.delete_application_instances()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteApplicationInstancesRequest()

@pytest.mark.asyncio
async def test_delete_application_instances_async(transport: str = 'grpc_asyncio', request_type=platform.DeleteApplicationInstancesRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteApplicationInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_application_instances_async_from_dict():
    await test_delete_application_instances_async(request_type=dict)


def test_delete_application_instances_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteApplicationInstancesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application_instances),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_application_instances_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteApplicationInstancesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application_instances),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_application_instances_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_application_instances(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_application_instances_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_application_instances(
            platform.DeleteApplicationInstancesRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_application_instances_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_application_instances(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_application_instances_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_application_instances(
            platform.DeleteApplicationInstancesRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.UpdateApplicationInstancesRequest,
  dict,
])
def test_update_application_instances(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_application_instances_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_instances),
            '__call__') as call:
        client.update_application_instances()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationInstancesRequest()

@pytest.mark.asyncio
async def test_update_application_instances_async(transport: str = 'grpc_asyncio', request_type=platform.UpdateApplicationInstancesRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateApplicationInstancesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_application_instances_async_from_dict():
    await test_update_application_instances_async(request_type=dict)


def test_update_application_instances_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateApplicationInstancesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_instances),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_application_instances_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateApplicationInstancesRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_instances),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_application_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_update_application_instances_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_application_instances(
            name='name_value',
            application_instances=[platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].application_instances
        mock_val = [platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))]
        assert arg == mock_val


def test_update_application_instances_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_application_instances(
            platform.UpdateApplicationInstancesRequest(),
            name='name_value',
            application_instances=[platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))],
        )

@pytest.mark.asyncio
async def test_update_application_instances_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_application_instances),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_application_instances(
            name='name_value',
            application_instances=[platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].application_instances
        mock_val = [platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))]
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_application_instances_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_application_instances(
            platform.UpdateApplicationInstancesRequest(),
            name='name_value',
            application_instances=[platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))],
        )


@pytest.mark.parametrize("request_type", [
  platform.ListDraftsRequest,
  dict,
])
def test_list_drafts(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListDraftsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_drafts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListDraftsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDraftsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_drafts_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        client.list_drafts()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListDraftsRequest()

@pytest.mark.asyncio
async def test_list_drafts_async(transport: str = 'grpc_asyncio', request_type=platform.ListDraftsRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.ListDraftsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_drafts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListDraftsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDraftsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_drafts_async_from_dict():
    await test_list_drafts_async(request_type=dict)


def test_list_drafts_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListDraftsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        call.return_value = platform.ListDraftsResponse()
        client.list_drafts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_drafts_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListDraftsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListDraftsResponse())
        await client.list_drafts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_drafts_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListDraftsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_drafts(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_drafts_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_drafts(
            platform.ListDraftsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_drafts_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListDraftsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListDraftsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_drafts(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_drafts_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_drafts(
            platform.ListDraftsRequest(),
            parent='parent_value',
        )


def test_list_drafts_pager(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                    platform.Draft(),
                ],
                next_page_token='abc',
            ),
            platform.ListDraftsResponse(
                drafts=[],
                next_page_token='def',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                ],
                next_page_token='ghi',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_drafts(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Draft)
                   for i in results)
def test_list_drafts_pages(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                    platform.Draft(),
                ],
                next_page_token='abc',
            ),
            platform.ListDraftsResponse(
                drafts=[],
                next_page_token='def',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                ],
                next_page_token='ghi',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_drafts(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_drafts_async_pager():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                    platform.Draft(),
                ],
                next_page_token='abc',
            ),
            platform.ListDraftsResponse(
                drafts=[],
                next_page_token='def',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                ],
                next_page_token='ghi',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_drafts(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, platform.Draft)
                for i in responses)


@pytest.mark.asyncio
async def test_list_drafts_async_pages():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_drafts),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                    platform.Draft(),
                ],
                next_page_token='abc',
            ),
            platform.ListDraftsResponse(
                drafts=[],
                next_page_token='def',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                ],
                next_page_token='ghi',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_drafts(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  platform.GetDraftRequest,
  dict,
])
def test_get_draft(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Draft(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
        )
        response = client.get_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Draft)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'


def test_get_draft_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_draft),
            '__call__') as call:
        client.get_draft()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetDraftRequest()

@pytest.mark.asyncio
async def test_get_draft_async(transport: str = 'grpc_asyncio', request_type=platform.GetDraftRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.Draft(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
        ))
        response = await client.get_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Draft)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'


@pytest.mark.asyncio
async def test_get_draft_async_from_dict():
    await test_get_draft_async(request_type=dict)


def test_get_draft_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetDraftRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_draft),
            '__call__') as call:
        call.return_value = platform.Draft()
        client.get_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_draft_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetDraftRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_draft),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Draft())
        await client.get_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_draft_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Draft()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_draft(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_draft_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_draft(
            platform.GetDraftRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_draft_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Draft()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Draft())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_draft(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_draft_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_draft(
            platform.GetDraftRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.CreateDraftRequest,
  dict,
])
def test_create_draft(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_draft_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_draft),
            '__call__') as call:
        client.create_draft()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateDraftRequest()

@pytest.mark.asyncio
async def test_create_draft_async(transport: str = 'grpc_asyncio', request_type=platform.CreateDraftRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_draft_async_from_dict():
    await test_create_draft_async(request_type=dict)


def test_create_draft_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateDraftRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_draft),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_draft_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateDraftRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_draft),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_draft_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_draft(
            parent='parent_value',
            draft=platform.Draft(name='name_value'),
            draft_id='draft_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].draft
        mock_val = platform.Draft(name='name_value')
        assert arg == mock_val
        arg = args[0].draft_id
        mock_val = 'draft_id_value'
        assert arg == mock_val


def test_create_draft_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_draft(
            platform.CreateDraftRequest(),
            parent='parent_value',
            draft=platform.Draft(name='name_value'),
            draft_id='draft_id_value',
        )

@pytest.mark.asyncio
async def test_create_draft_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_draft(
            parent='parent_value',
            draft=platform.Draft(name='name_value'),
            draft_id='draft_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].draft
        mock_val = platform.Draft(name='name_value')
        assert arg == mock_val
        arg = args[0].draft_id
        mock_val = 'draft_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_draft_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_draft(
            platform.CreateDraftRequest(),
            parent='parent_value',
            draft=platform.Draft(name='name_value'),
            draft_id='draft_id_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.UpdateDraftRequest,
  dict,
])
def test_update_draft(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_draft_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_draft),
            '__call__') as call:
        client.update_draft()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateDraftRequest()

@pytest.mark.asyncio
async def test_update_draft_async(transport: str = 'grpc_asyncio', request_type=platform.UpdateDraftRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_draft_async_from_dict():
    await test_update_draft_async(request_type=dict)


def test_update_draft_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateDraftRequest()

    request.draft.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_draft),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'draft.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_draft_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateDraftRequest()

    request.draft.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_draft),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'draft.name=name_value',
    ) in kw['metadata']


def test_update_draft_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_draft(
            draft=platform.Draft(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].draft
        mock_val = platform.Draft(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_draft_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_draft(
            platform.UpdateDraftRequest(),
            draft=platform.Draft(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_draft_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_draft(
            draft=platform.Draft(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].draft
        mock_val = platform.Draft(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_draft_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_draft(
            platform.UpdateDraftRequest(),
            draft=platform.Draft(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  platform.DeleteDraftRequest,
  dict,
])
def test_delete_draft(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_draft_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_draft),
            '__call__') as call:
        client.delete_draft()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteDraftRequest()

@pytest.mark.asyncio
async def test_delete_draft_async(transport: str = 'grpc_asyncio', request_type=platform.DeleteDraftRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteDraftRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_draft_async_from_dict():
    await test_delete_draft_async(request_type=dict)


def test_delete_draft_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteDraftRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_draft),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_draft_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteDraftRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_draft),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_draft(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_draft_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_draft(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_draft_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_draft(
            platform.DeleteDraftRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_draft_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_draft),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_draft(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_draft_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_draft(
            platform.DeleteDraftRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.ListProcessorsRequest,
  dict,
])
def test_list_processors(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListProcessorsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListProcessorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProcessorsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_processors_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        client.list_processors()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListProcessorsRequest()

@pytest.mark.asyncio
async def test_list_processors_async(transport: str = 'grpc_asyncio', request_type=platform.ListProcessorsRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.ListProcessorsResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListProcessorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProcessorsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_processors_async_from_dict():
    await test_list_processors_async(request_type=dict)


def test_list_processors_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListProcessorsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        call.return_value = platform.ListProcessorsResponse()
        client.list_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_processors_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListProcessorsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListProcessorsResponse())
        await client.list_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_processors_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListProcessorsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_processors(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_processors_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_processors(
            platform.ListProcessorsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_processors_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListProcessorsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListProcessorsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_processors(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_processors_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_processors(
            platform.ListProcessorsRequest(),
            parent='parent_value',
        )


def test_list_processors_pager(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                    platform.Processor(),
                ],
                next_page_token='abc',
            ),
            platform.ListProcessorsResponse(
                processors=[],
                next_page_token='def',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                ],
                next_page_token='ghi',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_processors(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Processor)
                   for i in results)
def test_list_processors_pages(transport_name: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                    platform.Processor(),
                ],
                next_page_token='abc',
            ),
            platform.ListProcessorsResponse(
                processors=[],
                next_page_token='def',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                ],
                next_page_token='ghi',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_processors(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_processors_async_pager():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                    platform.Processor(),
                ],
                next_page_token='abc',
            ),
            platform.ListProcessorsResponse(
                processors=[],
                next_page_token='def',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                ],
                next_page_token='ghi',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_processors(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, platform.Processor)
                for i in responses)


@pytest.mark.asyncio
async def test_list_processors_async_pages():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_processors),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                    platform.Processor(),
                ],
                next_page_token='abc',
            ),
            platform.ListProcessorsResponse(
                processors=[],
                next_page_token='def',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                ],
                next_page_token='ghi',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in ( # pragma: no branch
            await client.list_processors(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  platform.ListPrebuiltProcessorsRequest,
  dict,
])
def test_list_prebuilt_processors(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_prebuilt_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListPrebuiltProcessorsResponse(
        )
        response = client.list_prebuilt_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListPrebuiltProcessorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.ListPrebuiltProcessorsResponse)


def test_list_prebuilt_processors_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_prebuilt_processors),
            '__call__') as call:
        client.list_prebuilt_processors()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListPrebuiltProcessorsRequest()

@pytest.mark.asyncio
async def test_list_prebuilt_processors_async(transport: str = 'grpc_asyncio', request_type=platform.ListPrebuiltProcessorsRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_prebuilt_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.ListPrebuiltProcessorsResponse(
        ))
        response = await client.list_prebuilt_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.ListPrebuiltProcessorsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.ListPrebuiltProcessorsResponse)


@pytest.mark.asyncio
async def test_list_prebuilt_processors_async_from_dict():
    await test_list_prebuilt_processors_async(request_type=dict)


def test_list_prebuilt_processors_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListPrebuiltProcessorsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_prebuilt_processors),
            '__call__') as call:
        call.return_value = platform.ListPrebuiltProcessorsResponse()
        client.list_prebuilt_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_prebuilt_processors_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.ListPrebuiltProcessorsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_prebuilt_processors),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListPrebuiltProcessorsResponse())
        await client.list_prebuilt_processors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_prebuilt_processors_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_prebuilt_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListPrebuiltProcessorsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_prebuilt_processors(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_prebuilt_processors_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_prebuilt_processors(
            platform.ListPrebuiltProcessorsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_prebuilt_processors_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_prebuilt_processors),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.ListPrebuiltProcessorsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.ListPrebuiltProcessorsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_prebuilt_processors(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_prebuilt_processors_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_prebuilt_processors(
            platform.ListPrebuiltProcessorsRequest(),
            parent='parent_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.GetProcessorRequest,
  dict,
])
def test_get_processor(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Processor(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
            processor_type=platform.Processor.ProcessorType.PRETRAINED,
            model_type=platform.ModelType.IMAGE_CLASSIFICATION,
            state=platform.Processor.ProcessorState.CREATING,
            configuration_typeurl='configuration_typeurl_value',
            supported_annotation_types=[annotations.StreamAnnotationType.STREAM_ANNOTATION_TYPE_ACTIVE_ZONE],
            compatible_deployment_environment=[platform.DeploymentEnvironment.DEPLOYMENT_ENVIRONMENT_CLOUD],
            supports_post_processing=True,
            supported_instance_types=[platform.Instance.InstanceType.STREAMING_PREDICTION],
        )
        response = client.get_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Processor)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.processor_type == platform.Processor.ProcessorType.PRETRAINED
    assert response.model_type == platform.ModelType.IMAGE_CLASSIFICATION
    assert response.state == platform.Processor.ProcessorState.CREATING
    assert response.configuration_typeurl == 'configuration_typeurl_value'
    assert response.supported_annotation_types == [annotations.StreamAnnotationType.STREAM_ANNOTATION_TYPE_ACTIVE_ZONE]
    assert response.compatible_deployment_environment == [platform.DeploymentEnvironment.DEPLOYMENT_ENVIRONMENT_CLOUD]
    assert response.supports_post_processing is True
    assert response.supported_instance_types == [platform.Instance.InstanceType.STREAMING_PREDICTION]


def test_get_processor_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_processor),
            '__call__') as call:
        client.get_processor()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetProcessorRequest()

@pytest.mark.asyncio
async def test_get_processor_async(transport: str = 'grpc_asyncio', request_type=platform.GetProcessorRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(platform.Processor(
            name='name_value',
            display_name='display_name_value',
            description='description_value',
            processor_type=platform.Processor.ProcessorType.PRETRAINED,
            model_type=platform.ModelType.IMAGE_CLASSIFICATION,
            state=platform.Processor.ProcessorState.CREATING,
            configuration_typeurl='configuration_typeurl_value',
            supported_annotation_types=[annotations.StreamAnnotationType.STREAM_ANNOTATION_TYPE_ACTIVE_ZONE],
            compatible_deployment_environment=[platform.DeploymentEnvironment.DEPLOYMENT_ENVIRONMENT_CLOUD],
            supports_post_processing=True,
            supported_instance_types=[platform.Instance.InstanceType.STREAMING_PREDICTION],
        ))
        response = await client.get_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.GetProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Processor)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.processor_type == platform.Processor.ProcessorType.PRETRAINED
    assert response.model_type == platform.ModelType.IMAGE_CLASSIFICATION
    assert response.state == platform.Processor.ProcessorState.CREATING
    assert response.configuration_typeurl == 'configuration_typeurl_value'
    assert response.supported_annotation_types == [annotations.StreamAnnotationType.STREAM_ANNOTATION_TYPE_ACTIVE_ZONE]
    assert response.compatible_deployment_environment == [platform.DeploymentEnvironment.DEPLOYMENT_ENVIRONMENT_CLOUD]
    assert response.supports_post_processing is True
    assert response.supported_instance_types == [platform.Instance.InstanceType.STREAMING_PREDICTION]


@pytest.mark.asyncio
async def test_get_processor_async_from_dict():
    await test_get_processor_async(request_type=dict)


def test_get_processor_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetProcessorRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_processor),
            '__call__') as call:
        call.return_value = platform.Processor()
        client.get_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_processor_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.GetProcessorRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_processor),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Processor())
        await client.get_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_processor_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Processor()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_processor(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_processor_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_processor(
            platform.GetProcessorRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_processor_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = platform.Processor()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(platform.Processor())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_processor(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_processor_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_processor(
            platform.GetProcessorRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.CreateProcessorRequest,
  dict,
])
def test_create_processor(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_processor_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_processor),
            '__call__') as call:
        client.create_processor()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateProcessorRequest()

@pytest.mark.asyncio
async def test_create_processor_async(transport: str = 'grpc_asyncio', request_type=platform.CreateProcessorRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.CreateProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_processor_async_from_dict():
    await test_create_processor_async(request_type=dict)


def test_create_processor_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateProcessorRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_processor),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_processor_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.CreateProcessorRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_processor),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_processor_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_processor(
            parent='parent_value',
            processor=platform.Processor(name='name_value'),
            processor_id='processor_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].processor
        mock_val = platform.Processor(name='name_value')
        assert arg == mock_val
        arg = args[0].processor_id
        mock_val = 'processor_id_value'
        assert arg == mock_val


def test_create_processor_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_processor(
            platform.CreateProcessorRequest(),
            parent='parent_value',
            processor=platform.Processor(name='name_value'),
            processor_id='processor_id_value',
        )

@pytest.mark.asyncio
async def test_create_processor_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_processor(
            parent='parent_value',
            processor=platform.Processor(name='name_value'),
            processor_id='processor_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].processor
        mock_val = platform.Processor(name='name_value')
        assert arg == mock_val
        arg = args[0].processor_id
        mock_val = 'processor_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_processor_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_processor(
            platform.CreateProcessorRequest(),
            parent='parent_value',
            processor=platform.Processor(name='name_value'),
            processor_id='processor_id_value',
        )


@pytest.mark.parametrize("request_type", [
  platform.UpdateProcessorRequest,
  dict,
])
def test_update_processor(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_processor_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_processor),
            '__call__') as call:
        client.update_processor()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateProcessorRequest()

@pytest.mark.asyncio
async def test_update_processor_async(transport: str = 'grpc_asyncio', request_type=platform.UpdateProcessorRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.UpdateProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_processor_async_from_dict():
    await test_update_processor_async(request_type=dict)


def test_update_processor_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateProcessorRequest()

    request.processor.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_processor),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'processor.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_processor_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.UpdateProcessorRequest()

    request.processor.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_processor),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'processor.name=name_value',
    ) in kw['metadata']


def test_update_processor_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_processor(
            processor=platform.Processor(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].processor
        mock_val = platform.Processor(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_processor_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_processor(
            platform.UpdateProcessorRequest(),
            processor=platform.Processor(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_processor_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_processor(
            processor=platform.Processor(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].processor
        mock_val = platform.Processor(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_processor_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_processor(
            platform.UpdateProcessorRequest(),
            processor=platform.Processor(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  platform.DeleteProcessorRequest,
  dict,
])
def test_delete_processor(request_type, transport: str = 'grpc'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_processor_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_processor),
            '__call__') as call:
        client.delete_processor()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteProcessorRequest()

@pytest.mark.asyncio
async def test_delete_processor_async(transport: str = 'grpc_asyncio', request_type=platform.DeleteProcessorRequest):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == platform.DeleteProcessorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_processor_async_from_dict():
    await test_delete_processor_async(request_type=dict)


def test_delete_processor_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteProcessorRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_processor),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_processor_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = platform.DeleteProcessorRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_processor),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_processor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_processor_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_processor(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_processor_flattened_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_processor(
            platform.DeleteProcessorRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_processor_flattened_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_processor),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_processor(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_processor_flattened_error_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_processor(
            platform.DeleteProcessorRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
    platform.ListApplicationsRequest,
    dict,
])
def test_list_applications_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListApplicationsResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListApplicationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_applications(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListApplicationsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_applications_rest_required_fields(request_type=platform.ListApplicationsRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_applications._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_applications._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.ListApplicationsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.ListApplicationsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_applications(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_applications_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_applications._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_applications_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_list_applications") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_list_applications") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.ListApplicationsRequest.pb(platform.ListApplicationsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.ListApplicationsResponse.to_json(platform.ListApplicationsResponse())

        request = platform.ListApplicationsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.ListApplicationsResponse()

        client.list_applications(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_applications_rest_bad_request(transport: str = 'rest', request_type=platform.ListApplicationsRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_applications(request)


def test_list_applications_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListApplicationsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListApplicationsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_applications(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/applications" % client.transport._host, args[1])


def test_list_applications_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_applications(
            platform.ListApplicationsRequest(),
            parent='parent_value',
        )


def test_list_applications_rest_pager(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                    platform.Application(),
                ],
                next_page_token='abc',
            ),
            platform.ListApplicationsResponse(
                applications=[],
                next_page_token='def',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                ],
                next_page_token='ghi',
            ),
            platform.ListApplicationsResponse(
                applications=[
                    platform.Application(),
                    platform.Application(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(platform.ListApplicationsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_applications(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Application)
                for i in results)

        pages = list(client.list_applications(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    platform.GetApplicationRequest,
    dict,
])
def test_get_application_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Application(
              name='name_value',
              display_name='display_name_value',
              description='description_value',
              state=platform.Application.State.CREATED,
              billing_mode=platform.Application.BillingMode.PAYG,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Application.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_application(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Application)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.state == platform.Application.State.CREATED
    assert response.billing_mode == platform.Application.BillingMode.PAYG


def test_get_application_rest_required_fields(request_type=platform.GetApplicationRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.Application()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.Application.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_application(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_application_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_application._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_application_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_get_application") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_get_application") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.GetApplicationRequest.pb(platform.GetApplicationRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.Application.to_json(platform.Application())

        request = platform.GetApplicationRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.Application()

        client.get_application(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_application_rest_bad_request(transport: str = 'rest', request_type=platform.GetApplicationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_application(request)


def test_get_application_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Application()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Application.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_application(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}" % client.transport._host, args[1])


def test_get_application_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_application(
            platform.GetApplicationRequest(),
            name='name_value',
        )


def test_get_application_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.CreateApplicationRequest,
    dict,
])
def test_create_application_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["application"] = {'name': 'name_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}, 'runtime_info': {'deploy_time': {}, 'global_output_resources': [{'output_resource': 'output_resource_value', 'producer_node': 'producer_node_value', 'key': 'key_value'}], 'monitoring_config': {'enabled': True}, 'deployment_environment': 1}, 'state': 1, 'notification_settings': {'contact_settings': [{'email_contact': {'email_address': 'email_address_value'}, 'pubsub_contact': {'topic': 'topic_value'}}]}, 'billing_mode': 1}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_application(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_application_rest_required_fields(request_type=platform.CreateApplicationRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["application_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "applicationId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "applicationId" in jsonified_request
    assert jsonified_request["applicationId"] == request_init["application_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["applicationId"] = 'application_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_application._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("application_id", "request_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "applicationId" in jsonified_request
    assert jsonified_request["applicationId"] == 'application_id_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_application(request)

            expected_params = [
                (
                    "applicationId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_application_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_application._get_unset_required_fields({})
    assert set(unset_fields) == (set(("applicationId", "requestId", )) & set(("parent", "applicationId", "application", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_application_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_create_application") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_create_application") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.CreateApplicationRequest.pb(platform.CreateApplicationRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.CreateApplicationRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_application(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_application_rest_bad_request(transport: str = 'rest', request_type=platform.CreateApplicationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["application"] = {'name': 'name_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}, 'runtime_info': {'deploy_time': {}, 'global_output_resources': [{'output_resource': 'output_resource_value', 'producer_node': 'producer_node_value', 'key': 'key_value'}], 'monitoring_config': {'enabled': True}, 'deployment_environment': 1}, 'state': 1, 'notification_settings': {'contact_settings': [{'email_contact': {'email_address': 'email_address_value'}, 'pubsub_contact': {'topic': 'topic_value'}}]}, 'billing_mode': 1}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_application(request)


def test_create_application_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            application=platform.Application(name='name_value'),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_application(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/applications" % client.transport._host, args[1])


def test_create_application_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_application(
            platform.CreateApplicationRequest(),
            parent='parent_value',
            application=platform.Application(name='name_value'),
        )


def test_create_application_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.UpdateApplicationRequest,
    dict,
])
def test_update_application_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'application': {'name': 'projects/sample1/locations/sample2/applications/sample3'}}
    request_init["application"] = {'name': 'projects/sample1/locations/sample2/applications/sample3', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}, 'runtime_info': {'deploy_time': {}, 'global_output_resources': [{'output_resource': 'output_resource_value', 'producer_node': 'producer_node_value', 'key': 'key_value'}], 'monitoring_config': {'enabled': True}, 'deployment_environment': 1}, 'state': 1, 'notification_settings': {'contact_settings': [{'email_contact': {'email_address': 'email_address_value'}, 'pubsub_contact': {'topic': 'topic_value'}}]}, 'billing_mode': 1}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_application(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_application_rest_required_fields(request_type=platform.UpdateApplicationRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_application._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id", "update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_application(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_application_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_application._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId", "updateMask", )) & set(("application", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_application_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_update_application") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_update_application") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.UpdateApplicationRequest.pb(platform.UpdateApplicationRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.UpdateApplicationRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_application(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_application_rest_bad_request(transport: str = 'rest', request_type=platform.UpdateApplicationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'application': {'name': 'projects/sample1/locations/sample2/applications/sample3'}}
    request_init["application"] = {'name': 'projects/sample1/locations/sample2/applications/sample3', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}, 'runtime_info': {'deploy_time': {}, 'global_output_resources': [{'output_resource': 'output_resource_value', 'producer_node': 'producer_node_value', 'key': 'key_value'}], 'monitoring_config': {'enabled': True}, 'deployment_environment': 1}, 'state': 1, 'notification_settings': {'contact_settings': [{'email_contact': {'email_address': 'email_address_value'}, 'pubsub_contact': {'topic': 'topic_value'}}]}, 'billing_mode': 1}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_application(request)


def test_update_application_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'application': {'name': 'projects/sample1/locations/sample2/applications/sample3'}}

        # get truthy value for each flattened field
        mock_args = dict(
            application=platform.Application(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_application(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{application.name=projects/*/locations/*/applications/*}" % client.transport._host, args[1])


def test_update_application_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_application(
            platform.UpdateApplicationRequest(),
            application=platform.Application(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_application_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.DeleteApplicationRequest,
    dict,
])
def test_delete_application_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_application(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_application_rest_required_fields(request_type=platform.DeleteApplicationRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_application._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("force", "request_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_application(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_application_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_application._get_unset_required_fields({})
    assert set(unset_fields) == (set(("force", "requestId", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_application_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_delete_application") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_delete_application") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.DeleteApplicationRequest.pb(platform.DeleteApplicationRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.DeleteApplicationRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_application(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_application_rest_bad_request(transport: str = 'rest', request_type=platform.DeleteApplicationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_application(request)


def test_delete_application_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_application(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}" % client.transport._host, args[1])


def test_delete_application_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_application(
            platform.DeleteApplicationRequest(),
            name='name_value',
        )


def test_delete_application_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.DeployApplicationRequest,
    dict,
])
def test_deploy_application_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.deploy_application(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_deploy_application_rest_required_fields(request_type=platform.DeployApplicationRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).deploy_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).deploy_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.deploy_application(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_deploy_application_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.deploy_application._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_deploy_application_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_deploy_application") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_deploy_application") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.DeployApplicationRequest.pb(platform.DeployApplicationRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.DeployApplicationRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.deploy_application(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_deploy_application_rest_bad_request(transport: str = 'rest', request_type=platform.DeployApplicationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.deploy_application(request)


def test_deploy_application_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.deploy_application(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:deploy" % client.transport._host, args[1])


def test_deploy_application_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.deploy_application(
            platform.DeployApplicationRequest(),
            name='name_value',
        )


def test_deploy_application_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.UndeployApplicationRequest,
    dict,
])
def test_undeploy_application_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.undeploy_application(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_undeploy_application_rest_required_fields(request_type=platform.UndeployApplicationRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).undeploy_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).undeploy_application._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.undeploy_application(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_undeploy_application_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.undeploy_application._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_undeploy_application_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_undeploy_application") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_undeploy_application") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.UndeployApplicationRequest.pb(platform.UndeployApplicationRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.UndeployApplicationRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.undeploy_application(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_undeploy_application_rest_bad_request(transport: str = 'rest', request_type=platform.UndeployApplicationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.undeploy_application(request)


def test_undeploy_application_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.undeploy_application(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:undeploy" % client.transport._host, args[1])


def test_undeploy_application_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undeploy_application(
            platform.UndeployApplicationRequest(),
            name='name_value',
        )


def test_undeploy_application_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.AddApplicationStreamInputRequest,
    dict,
])
def test_add_application_stream_input_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.add_application_stream_input(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_add_application_stream_input_rest_required_fields(request_type=platform.AddApplicationStreamInputRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).add_application_stream_input._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).add_application_stream_input._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.add_application_stream_input(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_add_application_stream_input_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.add_application_stream_input._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_add_application_stream_input_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_add_application_stream_input") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_add_application_stream_input") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.AddApplicationStreamInputRequest.pb(platform.AddApplicationStreamInputRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.AddApplicationStreamInputRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.add_application_stream_input(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_add_application_stream_input_rest_bad_request(transport: str = 'rest', request_type=platform.AddApplicationStreamInputRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_application_stream_input(request)


def test_add_application_stream_input_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.add_application_stream_input(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:addStreamInput" % client.transport._host, args[1])


def test_add_application_stream_input_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_application_stream_input(
            platform.AddApplicationStreamInputRequest(),
            name='name_value',
        )


def test_add_application_stream_input_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.RemoveApplicationStreamInputRequest,
    dict,
])
def test_remove_application_stream_input_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.remove_application_stream_input(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_remove_application_stream_input_rest_required_fields(request_type=platform.RemoveApplicationStreamInputRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).remove_application_stream_input._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).remove_application_stream_input._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.remove_application_stream_input(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_remove_application_stream_input_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.remove_application_stream_input._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_remove_application_stream_input_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_remove_application_stream_input") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_remove_application_stream_input") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.RemoveApplicationStreamInputRequest.pb(platform.RemoveApplicationStreamInputRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.RemoveApplicationStreamInputRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.remove_application_stream_input(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_remove_application_stream_input_rest_bad_request(transport: str = 'rest', request_type=platform.RemoveApplicationStreamInputRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.remove_application_stream_input(request)


def test_remove_application_stream_input_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.remove_application_stream_input(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:removeStreamInput" % client.transport._host, args[1])


def test_remove_application_stream_input_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_application_stream_input(
            platform.RemoveApplicationStreamInputRequest(),
            name='name_value',
        )


def test_remove_application_stream_input_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.UpdateApplicationStreamInputRequest,
    dict,
])
def test_update_application_stream_input_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_application_stream_input(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_application_stream_input_rest_required_fields(request_type=platform.UpdateApplicationStreamInputRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_application_stream_input._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_application_stream_input._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_application_stream_input(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_application_stream_input_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_application_stream_input._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_application_stream_input_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_update_application_stream_input") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_update_application_stream_input") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.UpdateApplicationStreamInputRequest.pb(platform.UpdateApplicationStreamInputRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.UpdateApplicationStreamInputRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_application_stream_input(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_application_stream_input_rest_bad_request(transport: str = 'rest', request_type=platform.UpdateApplicationStreamInputRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_application_stream_input(request)


def test_update_application_stream_input_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_application_stream_input(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:updateStreamInput" % client.transport._host, args[1])


def test_update_application_stream_input_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_application_stream_input(
            platform.UpdateApplicationStreamInputRequest(),
            name='name_value',
        )


def test_update_application_stream_input_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.ListInstancesRequest,
    dict,
])
def test_list_instances_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListInstancesResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListInstancesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_instances(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstancesPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_instances_rest_required_fields(request_type=platform.ListInstancesRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_instances._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.ListInstancesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.ListInstancesResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_instances(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_instances_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_instances._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_instances_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_list_instances") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_list_instances") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.ListInstancesRequest.pb(platform.ListInstancesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.ListInstancesResponse.to_json(platform.ListInstancesResponse())

        request = platform.ListInstancesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.ListInstancesResponse()

        client.list_instances(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_instances_rest_bad_request(transport: str = 'rest', request_type=platform.ListInstancesRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_instances(request)


def test_list_instances_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListInstancesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListInstancesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/applications/*}/instances" % client.transport._host, args[1])


def test_list_instances_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_instances(
            platform.ListInstancesRequest(),
            parent='parent_value',
        )


def test_list_instances_rest_pager(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                    platform.Instance(),
                ],
                next_page_token='abc',
            ),
            platform.ListInstancesResponse(
                instances=[],
                next_page_token='def',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                ],
                next_page_token='ghi',
            ),
            platform.ListInstancesResponse(
                instances=[
                    platform.Instance(),
                    platform.Instance(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(platform.ListInstancesResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}

        pager = client.list_instances(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Instance)
                for i in results)

        pages = list(client.list_instances(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    platform.GetInstanceRequest,
    dict,
])
def test_get_instance_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3/instances/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Instance(
              name='name_value',
              display_name='display_name_value',
              description='description_value',
              instance_type=platform.Instance.InstanceType.STREAMING_PREDICTION,
              state=platform.Instance.State.CREATING,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Instance.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_instance(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Instance)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.instance_type == platform.Instance.InstanceType.STREAMING_PREDICTION
    assert response.state == platform.Instance.State.CREATING


def test_get_instance_rest_required_fields(request_type=platform.GetInstanceRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_instance._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.Instance()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.Instance.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_instance(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_instance_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_instance._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_instance_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_get_instance") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_get_instance") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.GetInstanceRequest.pb(platform.GetInstanceRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.Instance.to_json(platform.Instance())

        request = platform.GetInstanceRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.Instance()

        client.get_instance(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_instance_rest_bad_request(transport: str = 'rest', request_type=platform.GetInstanceRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3/instances/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_instance(request)


def test_get_instance_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Instance()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3/instances/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Instance.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_instance(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*/instances/*}" % client.transport._host, args[1])


def test_get_instance_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_instance(
            platform.GetInstanceRequest(),
            name='name_value',
        )


def test_get_instance_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.CreateApplicationInstancesRequest,
    dict,
])
def test_create_application_instances_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_application_instances(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_application_instances_rest_required_fields(request_type=platform.CreateApplicationInstancesRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_application_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_application_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_application_instances(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_application_instances_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_application_instances._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", "applicationInstances", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_application_instances_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_create_application_instances") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_create_application_instances") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.CreateApplicationInstancesRequest.pb(platform.CreateApplicationInstancesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.CreateApplicationInstancesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_application_instances(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_application_instances_rest_bad_request(transport: str = 'rest', request_type=platform.CreateApplicationInstancesRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_application_instances(request)


def test_create_application_instances_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_application_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:createApplicationInstances" % client.transport._host, args[1])


def test_create_application_instances_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_application_instances(
            platform.CreateApplicationInstancesRequest(),
            name='name_value',
        )


def test_create_application_instances_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.DeleteApplicationInstancesRequest,
    dict,
])
def test_delete_application_instances_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_application_instances(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_application_instances_rest_required_fields(request_type=platform.DeleteApplicationInstancesRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["instance_ids"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_application_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'
    jsonified_request["instanceIds"] = 'instance_ids_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_application_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'
    assert "instanceIds" in jsonified_request
    assert jsonified_request["instanceIds"] == 'instance_ids_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_application_instances(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_application_instances_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_application_instances._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", "instanceIds", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_application_instances_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_delete_application_instances") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_delete_application_instances") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.DeleteApplicationInstancesRequest.pb(platform.DeleteApplicationInstancesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.DeleteApplicationInstancesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_application_instances(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_application_instances_rest_bad_request(transport: str = 'rest', request_type=platform.DeleteApplicationInstancesRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_application_instances(request)


def test_delete_application_instances_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_application_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:deleteApplicationInstances" % client.transport._host, args[1])


def test_delete_application_instances_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_application_instances(
            platform.DeleteApplicationInstancesRequest(),
            name='name_value',
        )


def test_delete_application_instances_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.UpdateApplicationInstancesRequest,
    dict,
])
def test_update_application_instances_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_application_instances(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_application_instances_rest_required_fields(request_type=platform.UpdateApplicationInstancesRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_application_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_application_instances._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_application_instances(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_application_instances_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_application_instances._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_application_instances_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_update_application_instances") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_update_application_instances") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.UpdateApplicationInstancesRequest.pb(platform.UpdateApplicationInstancesRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.UpdateApplicationInstancesRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_application_instances(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_application_instances_rest_bad_request(transport: str = 'rest', request_type=platform.UpdateApplicationInstancesRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_application_instances(request)


def test_update_application_instances_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            application_instances=[platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))],
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_application_instances(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*}:updateApplicationInstances" % client.transport._host, args[1])


def test_update_application_instances_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_application_instances(
            platform.UpdateApplicationInstancesRequest(),
            name='name_value',
            application_instances=[platform.UpdateApplicationInstancesRequest.UpdateApplicationInstance(update_mask=field_mask_pb2.FieldMask(paths=['paths_value']))],
        )


def test_update_application_instances_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.ListDraftsRequest,
    dict,
])
def test_list_drafts_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListDraftsResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListDraftsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_drafts(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDraftsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_drafts_rest_required_fields(request_type=platform.ListDraftsRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_drafts._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_drafts._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.ListDraftsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.ListDraftsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_drafts(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_drafts_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_drafts._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_drafts_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_list_drafts") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_list_drafts") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.ListDraftsRequest.pb(platform.ListDraftsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.ListDraftsResponse.to_json(platform.ListDraftsResponse())

        request = platform.ListDraftsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.ListDraftsResponse()

        client.list_drafts(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_drafts_rest_bad_request(transport: str = 'rest', request_type=platform.ListDraftsRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_drafts(request)


def test_list_drafts_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListDraftsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListDraftsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_drafts(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/applications/*}/drafts" % client.transport._host, args[1])


def test_list_drafts_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_drafts(
            platform.ListDraftsRequest(),
            parent='parent_value',
        )


def test_list_drafts_rest_pager(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                    platform.Draft(),
                ],
                next_page_token='abc',
            ),
            platform.ListDraftsResponse(
                drafts=[],
                next_page_token='def',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                ],
                next_page_token='ghi',
            ),
            platform.ListDraftsResponse(
                drafts=[
                    platform.Draft(),
                    platform.Draft(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(platform.ListDraftsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}

        pager = client.list_drafts(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Draft)
                for i in results)

        pages = list(client.list_drafts(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    platform.GetDraftRequest,
    dict,
])
def test_get_draft_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Draft(
              name='name_value',
              display_name='display_name_value',
              description='description_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Draft.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_draft(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Draft)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'


def test_get_draft_rest_required_fields(request_type=platform.GetDraftRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_draft._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_draft._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.Draft()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.Draft.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_draft(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_draft_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_draft._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_draft_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_get_draft") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_get_draft") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.GetDraftRequest.pb(platform.GetDraftRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.Draft.to_json(platform.Draft())

        request = platform.GetDraftRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.Draft()

        client.get_draft(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_draft_rest_bad_request(transport: str = 'rest', request_type=platform.GetDraftRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_draft(request)


def test_get_draft_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Draft()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Draft.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_draft(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*/drafts/*}" % client.transport._host, args[1])


def test_get_draft_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_draft(
            platform.GetDraftRequest(),
            name='name_value',
        )


def test_get_draft_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.CreateDraftRequest,
    dict,
])
def test_create_draft_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}
    request_init["draft"] = {'name': 'name_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'draft_application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_draft(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_draft_rest_required_fields(request_type=platform.CreateDraftRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["draft_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "draftId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_draft._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "draftId" in jsonified_request
    assert jsonified_request["draftId"] == request_init["draft_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["draftId"] = 'draft_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_draft._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("draft_id", "request_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "draftId" in jsonified_request
    assert jsonified_request["draftId"] == 'draft_id_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_draft(request)

            expected_params = [
                (
                    "draftId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_draft_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_draft._get_unset_required_fields({})
    assert set(unset_fields) == (set(("draftId", "requestId", )) & set(("parent", "draftId", "draft", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_draft_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_create_draft") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_create_draft") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.CreateDraftRequest.pb(platform.CreateDraftRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.CreateDraftRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_draft(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_draft_rest_bad_request(transport: str = 'rest', request_type=platform.CreateDraftRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}
    request_init["draft"] = {'name': 'name_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'draft_application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_draft(request)


def test_create_draft_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/applications/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            draft=platform.Draft(name='name_value'),
            draft_id='draft_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_draft(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/applications/*}/drafts" % client.transport._host, args[1])


def test_create_draft_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_draft(
            platform.CreateDraftRequest(),
            parent='parent_value',
            draft=platform.Draft(name='name_value'),
            draft_id='draft_id_value',
        )


def test_create_draft_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.UpdateDraftRequest,
    dict,
])
def test_update_draft_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'draft': {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}}
    request_init["draft"] = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'draft_application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_draft(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_draft_rest_required_fields(request_type=platform.UpdateDraftRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_draft._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_draft._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("allow_missing", "request_id", "update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_draft(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_draft_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_draft._get_unset_required_fields({})
    assert set(unset_fields) == (set(("allowMissing", "requestId", "updateMask", )) & set(("draft", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_draft_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_update_draft") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_update_draft") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.UpdateDraftRequest.pb(platform.UpdateDraftRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.UpdateDraftRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_draft(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_draft_rest_bad_request(transport: str = 'rest', request_type=platform.UpdateDraftRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'draft': {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}}
    request_init["draft"] = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'draft_application_configs': {'nodes': [{'output_all_output_channels_to_stream': True, 'name': 'name_value', 'display_name': 'display_name_value', 'node_config': {'video_stream_input_config': {'streams': ['streams_value1', 'streams_value2'], 'streams_with_annotation': [{'stream': 'stream_value', 'application_annotations': [{'active_zone': {'normalized_vertices': [{'x': 0.12, 'y': 0.121}]}, 'crossing_line': {'normalized_vertices': {}}, 'id': 'id_value', 'display_name': 'display_name_value', 'source_stream': 'source_stream_value', 'type_': 1}], 'node_annotations': [{'node': 'node_value', 'annotations': {}}]}]}, 'ai_enabled_devices_input_config': {}, 'media_warehouse_config': {'corpus': 'corpus_value', 'region': 'region_value', 'ttl': {'seconds': 751, 'nanos': 543}}, 'person_blur_config': {'person_blur_type': 1, 'faces_only': True}, 'occupancy_count_config': {'enable_people_counting': True, 'enable_vehicle_counting': True, 'enable_dwelling_time_tracking': True}, 'person_vehicle_detection_config': {'enable_people_counting': True, 'enable_vehicle_counting': True}, 'vertex_automl_vision_config': {'confidence_threshold': 0.2106, 'max_predictions': 1609}, 'vertex_automl_video_config': {'confidence_threshold': 0.2106, 'blocked_labels': ['blocked_labels_value1', 'blocked_labels_value2'], 'max_predictions': 1609, 'bounding_box_size_limit': 0.2454}, 'vertex_custom_config': {'max_prediction_fps': 1918, 'dedicated_resources': {'machine_spec': {'machine_type': 'machine_type_value', 'accelerator_type': 1, 'accelerator_count': 1805}, 'min_replica_count': 1803, 'max_replica_count': 1805, 'autoscaling_metric_specs': [{'metric_name': 'metric_name_value', 'target': 647}]}, 'post_processing_cloud_function': 'post_processing_cloud_function_value', 'attach_application_metadata': True}, 'general_object_detection_config': {}, 'big_query_config': {'table': 'table_value', 'cloud_function_mapping': {}, 'create_default_table_if_not_exists': True}, 'local_output_config': {'dir_path': 'dir_path_value'}, 'gcs_output_config': {'gcs_path': 'gcs_path_value'}, 'product_recognizer_config': {'retail_endpoint': 'retail_endpoint_value', 'recognition_confidence_threshold': 0.3386}, 'personal_protective_equipment_detection_config': {'enable_face_coverage_detection': True, 'enable_head_coverage_detection': True, 'enable_hands_coverage_detection': True}, 'tag_recognizer_config': {'entity_detection_confidence_threshold': 0.3924, 'tag_parsing_config': {'entity_parsing_configs': [{'entity_class': 'entity_class_value', 'regex': 'regex_value', 'entity_matching_strategy': 1}]}}, 'universal_input_config': {}, 'label_detector_config': {'custom_labels': ['custom_labels_value1', 'custom_labels_value2']}, 'embeddings_extractor_config': {'contextual_texts': ['contextual_texts_value1', 'contextual_texts_value2']}, 'product_detector_config': {'product_detection_confidence_threshold': 0.40240000000000004}, 'post_processing_config': {'post_processing_cloud_function': 'post_processing_cloud_function_value'}, 'experimental_config': {'fields': {}}}, 'processor': 'processor_value', 'parents': [{'parent_node': 'parent_node_value', 'parent_output_channel': 'parent_output_channel_value', 'connected_input_channel': 'connected_input_channel_value'}]}], 'event_delivery_config': {'channel': 'channel_value', 'minimal_delivery_interval': {}}}}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_draft(request)


def test_update_draft_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'draft': {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}}

        # get truthy value for each flattened field
        mock_args = dict(
            draft=platform.Draft(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_draft(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{draft.name=projects/*/locations/*/applications/*/drafts/*}" % client.transport._host, args[1])


def test_update_draft_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_draft(
            platform.UpdateDraftRequest(),
            draft=platform.Draft(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_draft_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.DeleteDraftRequest,
    dict,
])
def test_delete_draft_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_draft(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_draft_rest_required_fields(request_type=platform.DeleteDraftRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_draft._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_draft._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_draft(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_draft_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_draft._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_draft_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_delete_draft") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_delete_draft") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.DeleteDraftRequest.pb(platform.DeleteDraftRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.DeleteDraftRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_draft(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_draft_rest_bad_request(transport: str = 'rest', request_type=platform.DeleteDraftRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_draft(request)


def test_delete_draft_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/applications/sample3/drafts/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_draft(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/applications/*/drafts/*}" % client.transport._host, args[1])


def test_delete_draft_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_draft(
            platform.DeleteDraftRequest(),
            name='name_value',
        )


def test_delete_draft_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.ListProcessorsRequest,
    dict,
])
def test_list_processors_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListProcessorsResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListProcessorsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_processors(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProcessorsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_processors_rest_required_fields(request_type=platform.ListProcessorsRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_processors._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_processors._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.ListProcessorsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.ListProcessorsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_processors(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_processors_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_processors._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_processors_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_list_processors") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_list_processors") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.ListProcessorsRequest.pb(platform.ListProcessorsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.ListProcessorsResponse.to_json(platform.ListProcessorsResponse())

        request = platform.ListProcessorsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.ListProcessorsResponse()

        client.list_processors(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_processors_rest_bad_request(transport: str = 'rest', request_type=platform.ListProcessorsRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_processors(request)


def test_list_processors_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListProcessorsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListProcessorsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_processors(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/processors" % client.transport._host, args[1])


def test_list_processors_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_processors(
            platform.ListProcessorsRequest(),
            parent='parent_value',
        )


def test_list_processors_rest_pager(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                    platform.Processor(),
                ],
                next_page_token='abc',
            ),
            platform.ListProcessorsResponse(
                processors=[],
                next_page_token='def',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                ],
                next_page_token='ghi',
            ),
            platform.ListProcessorsResponse(
                processors=[
                    platform.Processor(),
                    platform.Processor(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(platform.ListProcessorsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_processors(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, platform.Processor)
                for i in results)

        pages = list(client.list_processors(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    platform.ListPrebuiltProcessorsRequest,
    dict,
])
def test_list_prebuilt_processors_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListPrebuiltProcessorsResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListPrebuiltProcessorsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_prebuilt_processors(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.ListPrebuiltProcessorsResponse)


def test_list_prebuilt_processors_rest_required_fields(request_type=platform.ListPrebuiltProcessorsRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_prebuilt_processors._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_prebuilt_processors._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.ListPrebuiltProcessorsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.ListPrebuiltProcessorsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_prebuilt_processors(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_prebuilt_processors_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_prebuilt_processors._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_prebuilt_processors_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_list_prebuilt_processors") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_list_prebuilt_processors") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.ListPrebuiltProcessorsRequest.pb(platform.ListPrebuiltProcessorsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.ListPrebuiltProcessorsResponse.to_json(platform.ListPrebuiltProcessorsResponse())

        request = platform.ListPrebuiltProcessorsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.ListPrebuiltProcessorsResponse()

        client.list_prebuilt_processors(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_prebuilt_processors_rest_bad_request(transport: str = 'rest', request_type=platform.ListPrebuiltProcessorsRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_prebuilt_processors(request)


def test_list_prebuilt_processors_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.ListPrebuiltProcessorsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.ListPrebuiltProcessorsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_prebuilt_processors(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/processors:prebuilt" % client.transport._host, args[1])


def test_list_prebuilt_processors_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_prebuilt_processors(
            platform.ListPrebuiltProcessorsRequest(),
            parent='parent_value',
        )


def test_list_prebuilt_processors_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.GetProcessorRequest,
    dict,
])
def test_get_processor_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/processors/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Processor(
              name='name_value',
              display_name='display_name_value',
              description='description_value',
              processor_type=platform.Processor.ProcessorType.PRETRAINED,
              model_type=platform.ModelType.IMAGE_CLASSIFICATION,
              state=platform.Processor.ProcessorState.CREATING,
              configuration_typeurl='configuration_typeurl_value',
              supported_annotation_types=[annotations.StreamAnnotationType.STREAM_ANNOTATION_TYPE_ACTIVE_ZONE],
              compatible_deployment_environment=[platform.DeploymentEnvironment.DEPLOYMENT_ENVIRONMENT_CLOUD],
              supports_post_processing=True,
              supported_instance_types=[platform.Instance.InstanceType.STREAMING_PREDICTION],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Processor.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_processor(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, platform.Processor)
    assert response.name == 'name_value'
    assert response.display_name == 'display_name_value'
    assert response.description == 'description_value'
    assert response.processor_type == platform.Processor.ProcessorType.PRETRAINED
    assert response.model_type == platform.ModelType.IMAGE_CLASSIFICATION
    assert response.state == platform.Processor.ProcessorState.CREATING
    assert response.configuration_typeurl == 'configuration_typeurl_value'
    assert response.supported_annotation_types == [annotations.StreamAnnotationType.STREAM_ANNOTATION_TYPE_ACTIVE_ZONE]
    assert response.compatible_deployment_environment == [platform.DeploymentEnvironment.DEPLOYMENT_ENVIRONMENT_CLOUD]
    assert response.supports_post_processing is True
    assert response.supported_instance_types == [platform.Instance.InstanceType.STREAMING_PREDICTION]


def test_get_processor_rest_required_fields(request_type=platform.GetProcessorRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_processor._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_processor._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = platform.Processor()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = platform.Processor.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_processor(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_processor_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_processor._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_processor_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_get_processor") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_get_processor") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.GetProcessorRequest.pb(platform.GetProcessorRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = platform.Processor.to_json(platform.Processor())

        request = platform.GetProcessorRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = platform.Processor()

        client.get_processor(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_processor_rest_bad_request(transport: str = 'rest', request_type=platform.GetProcessorRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/processors/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_processor(request)


def test_get_processor_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = platform.Processor()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/processors/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = platform.Processor.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_processor(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/processors/*}" % client.transport._host, args[1])


def test_get_processor_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_processor(
            platform.GetProcessorRequest(),
            name='name_value',
        )


def test_get_processor_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.CreateProcessorRequest,
    dict,
])
def test_create_processor_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["processor"] = {'name': 'name_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'processor_type': 1, 'model_type': 1, 'custom_processor_source_info': {'vertex_model': 'vertex_model_value', 'product_recognizer_artifact': {'retail_product_recognition_index': 'retail_product_recognition_index_value', 'vertex_model': 'vertex_model_value'}, 'source_type': 1, 'additional_info': {}, 'model_schema': {'instances_schema': {'uris': ['uris_value1', 'uris_value2']}, 'parameters_schema': {}, 'predictions_schema': {}}}, 'state': 1, 'processor_io_spec': {'graph_input_channel_specs': [{'name': 'name_value', 'data_type': 1, 'accepted_data_type_uris': ['accepted_data_type_uris_value1', 'accepted_data_type_uris_value2'], 'required': True, 'max_connection_allowed': 2332}], 'graph_output_channel_specs': [{'name': 'name_value', 'data_type': 1, 'data_type_uri': 'data_type_uri_value'}], 'instance_resource_input_binding_specs': [{'config_type_uri': 'config_type_uri_value', 'resource_type_uri': 'resource_type_uri_value', 'name': 'name_value'}], 'instance_resource_output_binding_specs': [{'name': 'name_value', 'resource_type_uri': 'resource_type_uri_value', 'explicit': True}]}, 'configuration_typeurl': 'configuration_typeurl_value', 'supported_annotation_types': [1], 'compatible_deployment_environment': [1], 'supports_post_processing': True, 'supported_instance_types': [1]}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_processor(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_processor_rest_required_fields(request_type=platform.CreateProcessorRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["processor_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "processorId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_processor._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "processorId" in jsonified_request
    assert jsonified_request["processorId"] == request_init["processor_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["processorId"] = 'processor_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_processor._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("processor_id", "request_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "processorId" in jsonified_request
    assert jsonified_request["processorId"] == 'processor_id_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_processor(request)

            expected_params = [
                (
                    "processorId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_processor_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_processor._get_unset_required_fields({})
    assert set(unset_fields) == (set(("processorId", "requestId", )) & set(("parent", "processorId", "processor", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_processor_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_create_processor") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_create_processor") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.CreateProcessorRequest.pb(platform.CreateProcessorRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.CreateProcessorRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_processor(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_processor_rest_bad_request(transport: str = 'rest', request_type=platform.CreateProcessorRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["processor"] = {'name': 'name_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'processor_type': 1, 'model_type': 1, 'custom_processor_source_info': {'vertex_model': 'vertex_model_value', 'product_recognizer_artifact': {'retail_product_recognition_index': 'retail_product_recognition_index_value', 'vertex_model': 'vertex_model_value'}, 'source_type': 1, 'additional_info': {}, 'model_schema': {'instances_schema': {'uris': ['uris_value1', 'uris_value2']}, 'parameters_schema': {}, 'predictions_schema': {}}}, 'state': 1, 'processor_io_spec': {'graph_input_channel_specs': [{'name': 'name_value', 'data_type': 1, 'accepted_data_type_uris': ['accepted_data_type_uris_value1', 'accepted_data_type_uris_value2'], 'required': True, 'max_connection_allowed': 2332}], 'graph_output_channel_specs': [{'name': 'name_value', 'data_type': 1, 'data_type_uri': 'data_type_uri_value'}], 'instance_resource_input_binding_specs': [{'config_type_uri': 'config_type_uri_value', 'resource_type_uri': 'resource_type_uri_value', 'name': 'name_value'}], 'instance_resource_output_binding_specs': [{'name': 'name_value', 'resource_type_uri': 'resource_type_uri_value', 'explicit': True}]}, 'configuration_typeurl': 'configuration_typeurl_value', 'supported_annotation_types': [1], 'compatible_deployment_environment': [1], 'supports_post_processing': True, 'supported_instance_types': [1]}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_processor(request)


def test_create_processor_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            processor=platform.Processor(name='name_value'),
            processor_id='processor_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_processor(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/processors" % client.transport._host, args[1])


def test_create_processor_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_processor(
            platform.CreateProcessorRequest(),
            parent='parent_value',
            processor=platform.Processor(name='name_value'),
            processor_id='processor_id_value',
        )


def test_create_processor_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.UpdateProcessorRequest,
    dict,
])
def test_update_processor_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'processor': {'name': 'projects/sample1/locations/sample2/processors/sample3'}}
    request_init["processor"] = {'name': 'projects/sample1/locations/sample2/processors/sample3', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'processor_type': 1, 'model_type': 1, 'custom_processor_source_info': {'vertex_model': 'vertex_model_value', 'product_recognizer_artifact': {'retail_product_recognition_index': 'retail_product_recognition_index_value', 'vertex_model': 'vertex_model_value'}, 'source_type': 1, 'additional_info': {}, 'model_schema': {'instances_schema': {'uris': ['uris_value1', 'uris_value2']}, 'parameters_schema': {}, 'predictions_schema': {}}}, 'state': 1, 'processor_io_spec': {'graph_input_channel_specs': [{'name': 'name_value', 'data_type': 1, 'accepted_data_type_uris': ['accepted_data_type_uris_value1', 'accepted_data_type_uris_value2'], 'required': True, 'max_connection_allowed': 2332}], 'graph_output_channel_specs': [{'name': 'name_value', 'data_type': 1, 'data_type_uri': 'data_type_uri_value'}], 'instance_resource_input_binding_specs': [{'config_type_uri': 'config_type_uri_value', 'resource_type_uri': 'resource_type_uri_value', 'name': 'name_value'}], 'instance_resource_output_binding_specs': [{'name': 'name_value', 'resource_type_uri': 'resource_type_uri_value', 'explicit': True}]}, 'configuration_typeurl': 'configuration_typeurl_value', 'supported_annotation_types': [1], 'compatible_deployment_environment': [1], 'supports_post_processing': True, 'supported_instance_types': [1]}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_processor(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_processor_rest_required_fields(request_type=platform.UpdateProcessorRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_processor._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_processor._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id", "update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_processor(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_processor_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_processor._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId", "updateMask", )) & set(("processor", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_processor_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_update_processor") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_update_processor") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.UpdateProcessorRequest.pb(platform.UpdateProcessorRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.UpdateProcessorRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_processor(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_processor_rest_bad_request(transport: str = 'rest', request_type=platform.UpdateProcessorRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'processor': {'name': 'projects/sample1/locations/sample2/processors/sample3'}}
    request_init["processor"] = {'name': 'projects/sample1/locations/sample2/processors/sample3', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'labels': {}, 'display_name': 'display_name_value', 'description': 'description_value', 'processor_type': 1, 'model_type': 1, 'custom_processor_source_info': {'vertex_model': 'vertex_model_value', 'product_recognizer_artifact': {'retail_product_recognition_index': 'retail_product_recognition_index_value', 'vertex_model': 'vertex_model_value'}, 'source_type': 1, 'additional_info': {}, 'model_schema': {'instances_schema': {'uris': ['uris_value1', 'uris_value2']}, 'parameters_schema': {}, 'predictions_schema': {}}}, 'state': 1, 'processor_io_spec': {'graph_input_channel_specs': [{'name': 'name_value', 'data_type': 1, 'accepted_data_type_uris': ['accepted_data_type_uris_value1', 'accepted_data_type_uris_value2'], 'required': True, 'max_connection_allowed': 2332}], 'graph_output_channel_specs': [{'name': 'name_value', 'data_type': 1, 'data_type_uri': 'data_type_uri_value'}], 'instance_resource_input_binding_specs': [{'config_type_uri': 'config_type_uri_value', 'resource_type_uri': 'resource_type_uri_value', 'name': 'name_value'}], 'instance_resource_output_binding_specs': [{'name': 'name_value', 'resource_type_uri': 'resource_type_uri_value', 'explicit': True}]}, 'configuration_typeurl': 'configuration_typeurl_value', 'supported_annotation_types': [1], 'compatible_deployment_environment': [1], 'supports_post_processing': True, 'supported_instance_types': [1]}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_processor(request)


def test_update_processor_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'processor': {'name': 'projects/sample1/locations/sample2/processors/sample3'}}

        # get truthy value for each flattened field
        mock_args = dict(
            processor=platform.Processor(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_processor(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{processor.name=projects/*/locations/*/processors/*}" % client.transport._host, args[1])


def test_update_processor_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_processor(
            platform.UpdateProcessorRequest(),
            processor=platform.Processor(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_processor_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    platform.DeleteProcessorRequest,
    dict,
])
def test_delete_processor_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/processors/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_processor(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_processor_rest_required_fields(request_type=platform.DeleteProcessorRequest):
    transport_class = transports.AppPlatformRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_processor._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_processor._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_processor(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_processor_rest_unset_required_fields():
    transport = transports.AppPlatformRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_processor._get_unset_required_fields({})
    assert set(unset_fields) == (set(("requestId", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_processor_rest_interceptors(null_interceptor):
    transport = transports.AppPlatformRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.AppPlatformRestInterceptor(),
        )
    client = AppPlatformClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.AppPlatformRestInterceptor, "post_delete_processor") as post, \
         mock.patch.object(transports.AppPlatformRestInterceptor, "pre_delete_processor") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = platform.DeleteProcessorRequest.pb(platform.DeleteProcessorRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = platform.DeleteProcessorRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_processor(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_processor_rest_bad_request(transport: str = 'rest', request_type=platform.DeleteProcessorRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/processors/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_processor(request)


def test_delete_processor_rest_flattened():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/processors/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_processor(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/processors/*}" % client.transport._host, args[1])


def test_delete_processor_rest_flattened_error(transport: str = 'rest'):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_processor(
            platform.DeleteProcessorRequest(),
            name='name_value',
        )


def test_delete_processor_rest_error():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AppPlatformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AppPlatformClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AppPlatformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AppPlatformClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.AppPlatformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AppPlatformClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = AppPlatformClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AppPlatformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AppPlatformClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AppPlatformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AppPlatformClient(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AppPlatformGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AppPlatformGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.AppPlatformGrpcTransport,
    transports.AppPlatformGrpcAsyncIOTransport,
    transports.AppPlatformRestTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "rest",
])
def test_transport_kind(transport_name):
    transport = AppPlatformClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.AppPlatformGrpcTransport,
    )

def test_app_platform_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AppPlatformTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_app_platform_base_transport():
    # Instantiate the base transport.
    with mock.patch('visionai.python.gapic.visionai.visionai_v1.services.app_platform.transports.AppPlatformTransport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.AppPlatformTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'list_applications',
        'get_application',
        'create_application',
        'update_application',
        'delete_application',
        'deploy_application',
        'undeploy_application',
        'add_application_stream_input',
        'remove_application_stream_input',
        'update_application_stream_input',
        'list_instances',
        'get_instance',
        'create_application_instances',
        'delete_application_instances',
        'update_application_instances',
        'list_drafts',
        'get_draft',
        'create_draft',
        'update_draft',
        'delete_draft',
        'list_processors',
        'list_prebuilt_processors',
        'get_processor',
        'create_processor',
        'update_processor',
        'delete_processor',
        'get_operation',
        'cancel_operation',
        'delete_operation',
        'list_operations',
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_app_platform_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('visionai.python.gapic.visionai.visionai_v1.services.app_platform.transports.AppPlatformTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AppPlatformTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id="octopus",
        )


def test_app_platform_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('visionai.python.gapic.visionai.visionai_v1.services.app_platform.transports.AppPlatformTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AppPlatformTransport()
        adc.assert_called_once()


def test_app_platform_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AppPlatformClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AppPlatformGrpcTransport,
        transports.AppPlatformGrpcAsyncIOTransport,
    ],
)
def test_app_platform_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/cloud-platform',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.AppPlatformGrpcTransport,
        transports.AppPlatformGrpcAsyncIOTransport,
        transports.AppPlatformRestTransport,
    ],
)
def test_app_platform_transport_auth_gdch_credentials(transport_class):
    host = 'https://language.com'
    api_audience_tests = [None, 'https://language2.com']
    api_audience_expect = [host, 'https://language2.com']
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, 'default', autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(return_value=gdch_mock)
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(
                e
            )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.AppPlatformGrpcTransport, grpc_helpers),
        (transports.AppPlatformGrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_app_platform_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(
            quota_project_id="octopus",
            scopes=["1", "2"]
        )

        create_channel.assert_called_with(
            "visionai.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=["1", "2"],
            default_host="visionai.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.AppPlatformGrpcTransport, transports.AppPlatformGrpcAsyncIOTransport])
def test_app_platform_grpc_transport_client_cert_source_for_mtls(
    transport_class
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert,
                private_key=expected_key
            )

def test_app_platform_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel") as mock_configure_mtls_channel:
        transports.AppPlatformRestTransport (
            credentials=cred,
            client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_app_platform_rest_lro_client():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_app_platform_host_no_port(transport_name):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='visionai.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'visionai.googleapis.com:443'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://visionai.googleapis.com'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_app_platform_host_with_port(transport_name):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='visionai.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'visionai.googleapis.com:8000'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://visionai.googleapis.com:8000'
    )

@pytest.mark.parametrize("transport_name", [
    "rest",
])
def test_app_platform_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = AppPlatformClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = AppPlatformClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.list_applications._session
    session2 = client2.transport.list_applications._session
    assert session1 != session2
    session1 = client1.transport.get_application._session
    session2 = client2.transport.get_application._session
    assert session1 != session2
    session1 = client1.transport.create_application._session
    session2 = client2.transport.create_application._session
    assert session1 != session2
    session1 = client1.transport.update_application._session
    session2 = client2.transport.update_application._session
    assert session1 != session2
    session1 = client1.transport.delete_application._session
    session2 = client2.transport.delete_application._session
    assert session1 != session2
    session1 = client1.transport.deploy_application._session
    session2 = client2.transport.deploy_application._session
    assert session1 != session2
    session1 = client1.transport.undeploy_application._session
    session2 = client2.transport.undeploy_application._session
    assert session1 != session2
    session1 = client1.transport.add_application_stream_input._session
    session2 = client2.transport.add_application_stream_input._session
    assert session1 != session2
    session1 = client1.transport.remove_application_stream_input._session
    session2 = client2.transport.remove_application_stream_input._session
    assert session1 != session2
    session1 = client1.transport.update_application_stream_input._session
    session2 = client2.transport.update_application_stream_input._session
    assert session1 != session2
    session1 = client1.transport.list_instances._session
    session2 = client2.transport.list_instances._session
    assert session1 != session2
    session1 = client1.transport.get_instance._session
    session2 = client2.transport.get_instance._session
    assert session1 != session2
    session1 = client1.transport.create_application_instances._session
    session2 = client2.transport.create_application_instances._session
    assert session1 != session2
    session1 = client1.transport.delete_application_instances._session
    session2 = client2.transport.delete_application_instances._session
    assert session1 != session2
    session1 = client1.transport.update_application_instances._session
    session2 = client2.transport.update_application_instances._session
    assert session1 != session2
    session1 = client1.transport.list_drafts._session
    session2 = client2.transport.list_drafts._session
    assert session1 != session2
    session1 = client1.transport.get_draft._session
    session2 = client2.transport.get_draft._session
    assert session1 != session2
    session1 = client1.transport.create_draft._session
    session2 = client2.transport.create_draft._session
    assert session1 != session2
    session1 = client1.transport.update_draft._session
    session2 = client2.transport.update_draft._session
    assert session1 != session2
    session1 = client1.transport.delete_draft._session
    session2 = client2.transport.delete_draft._session
    assert session1 != session2
    session1 = client1.transport.list_processors._session
    session2 = client2.transport.list_processors._session
    assert session1 != session2
    session1 = client1.transport.list_prebuilt_processors._session
    session2 = client2.transport.list_prebuilt_processors._session
    assert session1 != session2
    session1 = client1.transport.get_processor._session
    session2 = client2.transport.get_processor._session
    assert session1 != session2
    session1 = client1.transport.create_processor._session
    session2 = client2.transport.create_processor._session
    assert session1 != session2
    session1 = client1.transport.update_processor._session
    session2 = client2.transport.update_processor._session
    assert session1 != session2
    session1 = client1.transport.delete_processor._session
    session2 = client2.transport.delete_processor._session
    assert session1 != session2
def test_app_platform_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AppPlatformGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_app_platform_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AppPlatformGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.AppPlatformGrpcTransport, transports.AppPlatformGrpcAsyncIOTransport])
def test_app_platform_transport_channel_mtls_with_client_cert_source(
    transport_class
):
    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as grpc_ssl_channel_cred:
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, 'default') as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.AppPlatformGrpcTransport, transports.AppPlatformGrpcAsyncIOTransport])
def test_app_platform_transport_channel_mtls_with_adc(
    transport_class
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_app_platform_grpc_lro_client():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_app_platform_grpc_lro_async_client():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_application_path():
    project = "squid"
    location = "clam"
    application = "whelk"
    expected = "projects/{project}/locations/{location}/applications/{application}".format(project=project, location=location, application=application, )
    actual = AppPlatformClient.application_path(project, location, application)
    assert expected == actual


def test_parse_application_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "application": "nudibranch",
    }
    path = AppPlatformClient.application_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_application_path(path)
    assert expected == actual

def test_draft_path():
    project = "cuttlefish"
    location = "mussel"
    application = "winkle"
    draft = "nautilus"
    expected = "projects/{project}/locations/{location}/applications/{application}/drafts/{draft}".format(project=project, location=location, application=application, draft=draft, )
    actual = AppPlatformClient.draft_path(project, location, application, draft)
    assert expected == actual


def test_parse_draft_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "application": "squid",
        "draft": "clam",
    }
    path = AppPlatformClient.draft_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_draft_path(path)
    assert expected == actual

def test_instance_path():
    project = "whelk"
    location = "octopus"
    application = "oyster"
    instance = "nudibranch"
    expected = "projects/{project}/locations/{location}/applications/{application}/instances/{instance}".format(project=project, location=location, application=application, instance=instance, )
    actual = AppPlatformClient.instance_path(project, location, application, instance)
    assert expected == actual


def test_parse_instance_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "application": "winkle",
        "instance": "nautilus",
    }
    path = AppPlatformClient.instance_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_instance_path(path)
    assert expected == actual

def test_processor_path():
    project = "scallop"
    location = "abalone"
    processor = "squid"
    expected = "projects/{project}/locations/{location}/processors/{processor}".format(project=project, location=location, processor=processor, )
    actual = AppPlatformClient.processor_path(project, location, processor)
    assert expected == actual


def test_parse_processor_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "processor": "octopus",
    }
    path = AppPlatformClient.processor_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_processor_path(path)
    assert expected == actual

def test_stream_path():
    project = "oyster"
    location = "nudibranch"
    cluster = "cuttlefish"
    stream = "mussel"
    expected = "projects/{project}/locations/{location}/clusters/{cluster}/streams/{stream}".format(project=project, location=location, cluster=cluster, stream=stream, )
    actual = AppPlatformClient.stream_path(project, location, cluster, stream)
    assert expected == actual


def test_parse_stream_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "cluster": "scallop",
        "stream": "abalone",
    }
    path = AppPlatformClient.stream_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_stream_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = AppPlatformClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = AppPlatformClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder, )
    actual = AppPlatformClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = AppPlatformClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = AppPlatformClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = AppPlatformClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project, )
    actual = AppPlatformClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = AppPlatformClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = AppPlatformClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = AppPlatformClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AppPlatformClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.AppPlatformTransport, '_prep_wrapped_messages') as prep:
        client = AppPlatformClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.AppPlatformTransport, '_prep_wrapped_messages') as prep:
        transport_class = AppPlatformClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_cancel_operation_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.CancelOperationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2/operations/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.CancelOperationRequest,
    dict,
])
def test_cancel_operation_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2/operations/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = '{}'

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None

def test_delete_operation_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.DeleteOperationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2/operations/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.DeleteOperationRequest,
    dict,
])
def test_delete_operation_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2/operations/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = '{}'

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None

def test_get_operation_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.GetOperationRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2/operations/sample3'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.GetOperationRequest,
    dict,
])
def test_get_operation_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2/operations/sample3'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)

def test_list_operations_rest_bad_request(transport: str = 'rest', request_type=operations_pb2.ListOperationsRequest):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict({'name': 'projects/sample1/locations/sample2'}, request)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)

@pytest.mark.parametrize("request_type", [
    operations_pb2.ListOperationsRequest,
    dict,
])
def test_list_operations_rest(request_type):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {'name': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None
@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc"):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None

def test_delete_operation_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value =  None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_delete_operation_from_dict():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()
@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None
@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc"):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None

def test_cancel_operation_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value =  None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_cancel_operation_from_dict():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()
@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            None
        )
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)
@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc"):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)

def test_get_operation_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_get_operation_from_dict():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()
@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)
@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc"):
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)

def test_list_operations_field_headers():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]
@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=locations",) in kw["metadata"]

def test_list_operations_from_dict():
    client = AppPlatformClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()
@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = AppPlatformAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = AppPlatformClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'rest',
        'grpc',
    ]
    for transport in transports:
        client = AppPlatformClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()

@pytest.mark.parametrize("client_class,transport_class", [
    (AppPlatformClient, transports.AppPlatformGrpcTransport),
    (AppPlatformAsyncClient, transports.AppPlatformGrpcAsyncIOTransport),
])
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
