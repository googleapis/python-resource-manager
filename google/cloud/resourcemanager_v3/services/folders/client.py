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
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.resourcemanager_v3.services.folders import pagers
from google.cloud.resourcemanager_v3.types import folders
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import FoldersTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import FoldersGrpcTransport
from .transports.grpc_asyncio import FoldersGrpcAsyncIOTransport


class FoldersClientMeta(type):
    """Metaclass for the Folders client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[FoldersTransport]]
    _transport_registry["grpc"] = FoldersGrpcTransport
    _transport_registry["grpc_asyncio"] = FoldersGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[FoldersTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class FoldersClient(metaclass=FoldersClientMeta):
    """Manages Cloud Platform folder resources.
    Folders can be used to organize the resources under an
    organization and to control the policies applied to groups of
    resources.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "cloudresourcemanager.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
            FoldersClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            FoldersClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> FoldersTransport:
        """Returns the transport used by the client instance.

        Returns:
            FoldersTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_folder_path(path: str) -> Dict[str, str]:
        """Parses a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
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
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, FoldersTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the folders client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, FoldersTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, FoldersTransport):
            # transport is a FoldersTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def get_folder(
        self,
        request: Union[folders.GetFolderRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> folders.Folder:
        r"""Retrieves a folder identified by the supplied resource name.
        Valid folder resource names have the format
        ``folders/{folder_id}`` (for example, ``folders/1234``). The
        caller must have ``resourcemanager.folders.get`` permission on
        the identified folder.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_get_folder():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.GetFolderRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_folder(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.GetFolderRequest, dict]):
                The request object. The GetFolder request message.
            name (str):
                Required. The resource name of the folder to retrieve.
                Must be of the form ``folders/{folder_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.resourcemanager_v3.types.Folder:
                A folder in an organization's
                resource hierarchy, used to organize
                that organization's resources.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.GetFolderRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.GetFolderRequest):
            request = folders.GetFolderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_folder]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_folders(
        self,
        request: Union[folders.ListFoldersRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFoldersPager:
        r"""Lists the folders that are direct descendants of supplied parent
        resource. ``list()`` provides a strongly consistent view of the
        folders underneath the specified parent resource. ``list()``
        returns folders sorted based upon the (ascending) lexical
        ordering of their display_name. The caller must have
        ``resourcemanager.folders.list`` permission on the identified
        parent.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_list_folders():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.ListFoldersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_folders(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.ListFoldersRequest, dict]):
                The request object. The ListFolders request message.
            parent (str):
                Required. The resource name of the organization or
                folder whose folders are being listed. Must be of the
                form ``folders/{folder_id}`` or
                ``organizations/{org_id}``. Access to this method is
                controlled by checking the
                ``resourcemanager.folders.list`` permission on the
                ``parent``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.resourcemanager_v3.services.folders.pagers.ListFoldersPager:
                The ListFolders response message.
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

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.ListFoldersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.ListFoldersRequest):
            request = folders.ListFoldersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_folders]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListFoldersPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_folders(
        self,
        request: Union[folders.SearchFoldersRequest, dict] = None,
        *,
        query: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchFoldersPager:
        r"""Search for folders that match specific filter criteria.
        ``search()`` provides an eventually consistent view of the
        folders a user has access to which meet the specified filter
        criteria.

        This will only return folders on which the caller has the
        permission ``resourcemanager.folders.get``.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_search_folders():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.SearchFoldersRequest(
                )

                # Make the request
                page_result = client.search_folders(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.SearchFoldersRequest, dict]):
                The request object. The request message for searching
                folders.
            query (str):
                Optional. Search criteria used to select the folders to
                return. If no search criteria is specified then all
                accessible folders will be returned.

                Query expressions can be used to restrict results based
                upon displayName, state and parent, where the operators
                ``=`` (``:``) ``NOT``, ``AND`` and ``OR`` can be used
                along with the suffix wildcard symbol ``*``.

                The ``displayName`` field in a query expression should
                use escaped quotes for values that include whitespace to
                prevent unexpected behavior.

                ::

                   | Field                   | Description                            |
                   |-------------------------|----------------------------------------|
                   | displayName             | Filters by displayName.                |
                   | parent                  | Filters by parent (for example: folders/123). |
                   | state, lifecycleState   | Filters by state.                      |

                Some example queries are:

                -  Query ``displayName=Test*`` returns Folder resources
                   whose display name starts with "Test".
                -  Query ``state=ACTIVE`` returns Folder resources with
                   ``state`` set to ``ACTIVE``.
                -  Query ``parent=folders/123`` returns Folder resources
                   that have ``folders/123`` as a parent resource.
                -  Query ``parent=folders/123 AND state=ACTIVE`` returns
                   active Folder resources that have ``folders/123`` as
                   a parent resource.
                -  Query ``displayName=\\"Test String\\"`` returns
                   Folder resources with display names that include both
                   "Test" and "String".

                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.resourcemanager_v3.services.folders.pagers.SearchFoldersPager:
                The response message for searching
                folders.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([query])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.SearchFoldersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.SearchFoldersRequest):
            request = folders.SearchFoldersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_folders]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchFoldersPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_folder(
        self,
        request: Union[folders.CreateFolderRequest, dict] = None,
        *,
        folder: folders.Folder = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a folder in the resource hierarchy. Returns an
        ``Operation`` which can be used to track the progress of the
        folder creation workflow. Upon success, the
        ``Operation.response`` field will be populated with the created
        Folder.

        In order to succeed, the addition of this new folder must not
        violate the folder naming, height, or fanout constraints.

        -  The folder's ``display_name`` must be distinct from all other
           folders that share its parent.
        -  The addition of the folder must not cause the active folder
           hierarchy to exceed a height of 10. Note, the full active +
           deleted folder hierarchy is allowed to reach a height of 20;
           this provides additional headroom when moving folders that
           contain deleted folders.
        -  The addition of the folder must not cause the total number of
           folders under its parent to exceed 300.

        If the operation fails due to a folder constraint violation,
        some errors may be returned by the ``CreateFolder`` request,
        with status code ``FAILED_PRECONDITION`` and an error
        description. Other folder constraint violations will be
        communicated in the ``Operation``, with the specific
        ``PreconditionFailure`` returned in the details list in the
        ``Operation.error`` field.

        The caller must have ``resourcemanager.folders.create``
        permission on the identified parent.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_create_folder():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                folder = resourcemanager_v3.Folder()
                folder.parent = "parent_value"

                request = resourcemanager_v3.CreateFolderRequest(
                    folder=folder,
                )

                # Make the request
                operation = client.create_folder(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.CreateFolderRequest, dict]):
                The request object. The CreateFolder request message.
            folder (google.cloud.resourcemanager_v3.types.Folder):
                Required. The folder being created,
                only the display name and parent will be
                consulted. All other fields will be
                ignored.

                This corresponds to the ``folder`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.resourcemanager_v3.types.Folder` A folder in an organization's resource hierarchy, used to
                   organize that organization's resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([folder])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.CreateFolderRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.CreateFolderRequest):
            request = folders.CreateFolderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if folder is not None:
                request.folder = folder

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_folder]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            folders.Folder,
            metadata_type=folders.CreateFolderMetadata,
        )

        # Done; return the response.
        return response

    def update_folder(
        self,
        request: Union[folders.UpdateFolderRequest, dict] = None,
        *,
        folder: folders.Folder = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a folder, changing its ``display_name``. Changes to the
        folder ``display_name`` will be rejected if they violate either
        the ``display_name`` formatting rules or the naming constraints
        described in the
        [CreateFolder][google.cloud.resourcemanager.v3.Folders.CreateFolder]
        documentation.

        The folder's ``display_name`` must start and end with a letter
        or digit, may contain letters, digits, spaces, hyphens and
        underscores and can be between 3 and 30 characters. This is
        captured by the regular expression:
        ``[\p{L}\p{N}][\p{L}\p{N}_- ]{1,28}[\p{L}\p{N}]``. The caller
        must have ``resourcemanager.folders.update`` permission on the
        identified folder.

        If the update fails due to the unique name constraint then a
        ``PreconditionFailure`` explaining this violation will be
        returned in the Status.details field.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_update_folder():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                folder = resourcemanager_v3.Folder()
                folder.parent = "parent_value"

                request = resourcemanager_v3.UpdateFolderRequest(
                    folder=folder,
                )

                # Make the request
                operation = client.update_folder(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.UpdateFolderRequest, dict]):
                The request object. The request sent to the
                [UpdateFolder][google.cloud.resourcemanager.v3.Folder.UpdateFolder]
                method.

                Only the `display_name` field can be changed. All other
                fields will be ignored. Use the
                [MoveFolder][google.cloud.resourcemanager.v3.Folders.MoveFolder]
                method to change the `parent` field.
            folder (google.cloud.resourcemanager_v3.types.Folder):
                Required. The new definition of the Folder. It must
                include the ``name`` field, which cannot be changed.

                This corresponds to the ``folder`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Fields to be updated. Only the
                ``display_name`` can be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.resourcemanager_v3.types.Folder` A folder in an organization's resource hierarchy, used to
                   organize that organization's resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([folder, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.UpdateFolderRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.UpdateFolderRequest):
            request = folders.UpdateFolderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if folder is not None:
                request.folder = folder
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_folder]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("folder.name", request.folder.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            folders.Folder,
            metadata_type=folders.UpdateFolderMetadata,
        )

        # Done; return the response.
        return response

    def move_folder(
        self,
        request: Union[folders.MoveFolderRequest, dict] = None,
        *,
        name: str = None,
        destination_parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Moves a folder under a new resource parent. Returns an
        ``Operation`` which can be used to track the progress of the
        folder move workflow. Upon success, the ``Operation.response``
        field will be populated with the moved folder. Upon failure, a
        ``FolderOperationError`` categorizing the failure cause will be
        returned - if the failure occurs synchronously then the
        ``FolderOperationError`` will be returned in the
        ``Status.details`` field. If it occurs asynchronously, then the
        FolderOperation will be returned in the ``Operation.error``
        field. In addition, the ``Operation.metadata`` field will be
        populated with a ``FolderOperation`` message as an aid to
        stateless clients. Folder moves will be rejected if they violate
        either the naming, height, or fanout constraints described in
        the
        [CreateFolder][google.cloud.resourcemanager.v3.Folders.CreateFolder]
        documentation. The caller must have
        ``resourcemanager.folders.move`` permission on the folder's
        current and proposed new parent.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_move_folder():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.MoveFolderRequest(
                    name="name_value",
                    destination_parent="destination_parent_value",
                )

                # Make the request
                operation = client.move_folder(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.MoveFolderRequest, dict]):
                The request object. The MoveFolder request message.
            name (str):
                Required. The resource name of the Folder to move. Must
                be of the form folders/{folder_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            destination_parent (str):
                Required. The resource name of the folder or
                organization which should be the folder's new parent.
                Must be of the form ``folders/{folder_id}`` or
                ``organizations/{org_id}``.

                This corresponds to the ``destination_parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.resourcemanager_v3.types.Folder` A folder in an organization's resource hierarchy, used to
                   organize that organization's resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, destination_parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.MoveFolderRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.MoveFolderRequest):
            request = folders.MoveFolderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if destination_parent is not None:
                request.destination_parent = destination_parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.move_folder]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            folders.Folder,
            metadata_type=folders.MoveFolderMetadata,
        )

        # Done; return the response.
        return response

    def delete_folder(
        self,
        request: Union[folders.DeleteFolderRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Requests deletion of a folder. The folder is moved into the
        [DELETE_REQUESTED][google.cloud.resourcemanager.v3.Folder.State.DELETE_REQUESTED]
        state immediately, and is deleted approximately 30 days later.
        This method may only be called on an empty folder, where a
        folder is empty if it doesn't contain any folders or projects in
        the
        [ACTIVE][google.cloud.resourcemanager.v3.Folder.State.ACTIVE]
        state. If called on a folder in
        [DELETE_REQUESTED][google.cloud.resourcemanager.v3.Folder.State.DELETE_REQUESTED]
        state the operation will result in a no-op success. The caller
        must have ``resourcemanager.folders.delete`` permission on the
        identified folder.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_delete_folder():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.DeleteFolderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_folder(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.DeleteFolderRequest, dict]):
                The request object. The DeleteFolder request message.
            name (str):
                Required. The resource name of the folder to be deleted.
                Must be of the form ``folders/{folder_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.resourcemanager_v3.types.Folder` A folder in an organization's resource hierarchy, used to
                   organize that organization's resources.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.DeleteFolderRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.DeleteFolderRequest):
            request = folders.DeleteFolderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_folder]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            folders.Folder,
            metadata_type=folders.DeleteFolderMetadata,
        )

        # Done; return the response.
        return response

    def undelete_folder(
        self,
        request: Union[folders.UndeleteFolderRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Cancels the deletion request for a folder. This method may be
        called on a folder in any state. If the folder is in the
        [ACTIVE][google.cloud.resourcemanager.v3.Folder.State.ACTIVE]
        state the result will be a no-op success. In order to succeed,
        the folder's parent must be in the
        [ACTIVE][google.cloud.resourcemanager.v3.Folder.State.ACTIVE]
        state. In addition, reintroducing the folder into the tree must
        not violate folder naming, height, and fanout constraints
        described in the
        [CreateFolder][google.cloud.resourcemanager.v3.Folders.CreateFolder]
        documentation. The caller must have
        ``resourcemanager.folders.undelete`` permission on the
        identified folder.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_undelete_folder():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.UndeleteFolderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_folder(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.resourcemanager_v3.types.UndeleteFolderRequest, dict]):
                The request object. The UndeleteFolder request message.
            name (str):
                Required. The resource name of the folder to undelete.
                Must be of the form ``folders/{folder_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.resourcemanager_v3.types.Folder` A folder in an organization's resource hierarchy, used to
                   organize that organization's resources.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a folders.UndeleteFolderRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, folders.UndeleteFolderRequest):
            request = folders.UndeleteFolderRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undelete_folder]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            folders.Folder,
            metadata_type=folders.UndeleteFolderMetadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: Union[iam_policy_pb2.GetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a folder. The returned policy
        may be empty if no such policy or resource exists. The
        ``resource`` field should be the folder's resource name, for
        example: "folders/1234". The caller must have
        ``resourcemanager.folders.getIamPolicy`` permission on the
        identified folder.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_get_iam_policy():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for `GetIamPolicy`
                method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: Union[iam_policy_pb2.SetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy on a folder, replacing any
        existing policy. The ``resource`` field should be the folder's
        resource name, for example: "folders/1234". The caller must have
        ``resourcemanager.folders.setIamPolicy`` permission on the
        identified folder.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_set_iam_policy():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for `SetIamPolicy`
                method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: Union[iam_policy_pb2.TestIamPermissionsRequest, dict] = None,
        *,
        resource: str = None,
        permissions: Sequence[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that a caller has on the specified folder.
        The ``resource`` field should be the folder's resource name, for
        example: "folders/1234".

        There are no permissions required for making this API call.


        .. code-block:: python

            from google.cloud import resourcemanager_v3

            def sample_test_iam_permissions():
                # Create a client
                client = resourcemanager_v3.FoldersClient()

                # Initialize request argument(s)
                request = resourcemanager_v3.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value_1', 'permissions_value_2'],
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for
                `TestIamPermissions` method.
            resource (str):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (Sequence[str]):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()
            if resource is not None:
                request.resource = resource
            if permissions:
                request.permissions.extend(permissions)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-resourcemanager",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("FoldersClient",)
