# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from collections import OrderedDict
import functools
import re
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import pkg_resources

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.resourcemanager_v3.services.tag_bindings import pagers
from google.cloud.resourcemanager_v3.types import tag_bindings

from .client import TagBindingsClient
from .transports.base import DEFAULT_CLIENT_INFO, TagBindingsTransport
from .transports.grpc_asyncio import TagBindingsGrpcAsyncIOTransport


class TagBindingsAsyncClient:
    """Allow users to create and manage TagBindings between
    TagValues and different cloud resources throughout the GCP
    resource hierarchy.
    """

    _client: TagBindingsClient

    DEFAULT_ENDPOINT = TagBindingsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TagBindingsClient.DEFAULT_MTLS_ENDPOINT

    tag_binding_path = staticmethod(TagBindingsClient.tag_binding_path)
    parse_tag_binding_path = staticmethod(TagBindingsClient.parse_tag_binding_path)
    common_billing_account_path = staticmethod(
        TagBindingsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TagBindingsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TagBindingsClient.common_folder_path)
    parse_common_folder_path = staticmethod(TagBindingsClient.parse_common_folder_path)
    common_organization_path = staticmethod(TagBindingsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        TagBindingsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TagBindingsClient.common_project_path)
    parse_common_project_path = staticmethod(
        TagBindingsClient.parse_common_project_path
    )
    common_location_path = staticmethod(TagBindingsClient.common_location_path)
    parse_common_location_path = staticmethod(
        TagBindingsClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TagBindingsAsyncClient: The constructed client.
        """
        return TagBindingsClient.from_service_account_info.__func__(TagBindingsAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TagBindingsAsyncClient: The constructed client.
        """
        return TagBindingsClient.from_service_account_file.__func__(TagBindingsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return TagBindingsClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> TagBindingsTransport:
        """Returns the transport used by the client instance.

        Returns:
            TagBindingsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TagBindingsClient).get_transport_class, type(TagBindingsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TagBindingsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the tag bindings client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TagBindingsTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = TagBindingsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_tag_bindings(
        self,
        request: Union[tag_bindings.ListTagBindingsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTagBindingsAsyncPager:
        r"""Lists the TagBindings for the given cloud resource, as specified
        with ``parent``.

        NOTE: The ``parent`` field is expected to be a full resource
        name:
        https://cloud.google.com/apis/design/resource_names#full_resource_name

        .. code-block:: python

            from google.cloud import resourcemanager_v3

            async def sample_list_tag_bindings():
                # Create a client
                client = resourcemanager_v3.TagBindingsAsyncClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.ListTagBindingsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tag_bindings(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.ListTagBindingsRequest, dict]):
                The request object. The request message to list all
                TagBindings for a parent.
            parent (:class:`str`):
                Required. The full resource name of a
                resource for which you want to list
                existing TagBindings. E.g.
                "//cloudresourcemanager.googleapis.com/projects/123"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.resourcemanager_v3.services.tag_bindings.pagers.ListTagBindingsAsyncPager:
                The ListTagBindings response.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = tag_bindings.ListTagBindingsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_tag_bindings,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListTagBindingsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_tag_binding(
        self,
        request: Union[tag_bindings.CreateTagBindingRequest, dict] = None,
        *,
        tag_binding: tag_bindings.TagBinding = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a TagBinding between a TagValue and a cloud
        resource (currently project, folder, or organization).

        .. code-block:: python

            from google.cloud import resourcemanager_v3

            async def sample_create_tag_binding():
                # Create a client
                client = resourcemanager_v3.TagBindingsAsyncClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.CreateTagBindingRequest(
                )

                # Make the request
                operation = client.create_tag_binding(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.CreateTagBindingRequest, dict]):
                The request object. The request message to create a
                TagBinding.
            tag_binding (:class:`google.cloud.resourcemanager_v3.types.TagBinding`):
                Required. The TagBinding to be
                created.

                This corresponds to the ``tag_binding`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.resourcemanager_v3.types.TagBinding` A TagBinding represents a connection between a TagValue and a cloud
                   resource (currently project, folder, or
                   organization). Once a TagBinding is created, the
                   TagValue is applied to all the descendants of the
                   cloud resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([tag_binding])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = tag_bindings.CreateTagBindingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if tag_binding is not None:
            request.tag_binding = tag_binding

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_tag_binding,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            tag_bindings.TagBinding,
            metadata_type=tag_bindings.CreateTagBindingMetadata,
        )

        # Done; return the response.
        return response

    async def delete_tag_binding(
        self,
        request: Union[tag_bindings.DeleteTagBindingRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a TagBinding.

        .. code-block:: python

            from google.cloud import resourcemanager_v3

            async def sample_delete_tag_binding():
                # Create a client
                client = resourcemanager_v3.TagBindingsAsyncClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.DeleteTagBindingRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_tag_binding(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.DeleteTagBindingRequest, dict]):
                The request object. The request message to delete a
                TagBinding.
            name (:class:`str`):
                Required. The name of the TagBinding. This is a String
                of the form: ``tagBindings/{id}`` (e.g.
                ``tagBindings/%2F%2Fcloudresourcemanager.googleapis.com%2Fprojects%2F123/tagValues/456``).

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = tag_bindings.DeleteTagBindingRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_tag_binding,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=tag_bindings.DeleteTagBindingMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-resourcemanager",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TagBindingsAsyncClient",)
