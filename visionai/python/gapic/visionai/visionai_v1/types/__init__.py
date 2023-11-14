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
from .annotations import (
    AppPlatformCloudFunctionRequest,
    AppPlatformCloudFunctionResponse,
    AppPlatformEventBody,
    AppPlatformMetadata,
    ClassificationPredictionResult,
    ImageObjectDetectionPredictionResult,
    ImageSegmentationPredictionResult,
    NormalizedPolygon,
    NormalizedPolyline,
    NormalizedVertex,
    ObjectDetectionPredictionResult,
    OccupancyCountingPredictionResult,
    PersonalProtectiveEquipmentDetectionOutput,
    StreamAnnotation,
    StreamAnnotations,
    VideoActionRecognitionPredictionResult,
    VideoClassificationPredictionResult,
    VideoObjectTrackingPredictionResult,
    StreamAnnotationType,
)
from .common import (
    Cluster,
    GcsDestination,
    GcsSource,
    OperationMetadata,
    Point2D,
    Polygon2D,
)
from .lva import (
    AnalysisDefinition,
    AnalyzerDefinition,
    AttributeValue,
    OperatorDefinition,
    ResourceSpecification,
    RunStatus,
    RunMode,
)
from .lva_resources import (
    Analysis,
    Operator,
    Process,
)
from .lva_service import (
    BatchRunProcessRequest,
    BatchRunProcessResponse,
    CreateAnalysisRequest,
    CreateOperatorRequest,
    CreateProcessRequest,
    DeleteAnalysisRequest,
    DeleteOperatorRequest,
    DeleteProcessRequest,
    GetAnalysisRequest,
    GetOperatorRequest,
    GetProcessRequest,
    ListAnalysesRequest,
    ListAnalysesResponse,
    ListOperatorsRequest,
    ListOperatorsResponse,
    ListProcessesRequest,
    ListProcessesResponse,
    OperatorQuery,
    ResolveOperatorInfoRequest,
    ResolveOperatorInfoResponse,
    UpdateAnalysisRequest,
    UpdateOperatorRequest,
    UpdateProcessRequest,
    Registry,
)
from .platform import (
    AddApplicationStreamInputRequest,
    AddApplicationStreamInputResponse,
    AIEnabledDevicesInputConfig,
    Application,
    ApplicationConfigs,
    ApplicationInstance,
    ApplicationNodeAnnotation,
    ApplicationStreamInput,
    AutoscalingMetricSpec,
    BigQueryConfig,
    CreateApplicationInstancesRequest,
    CreateApplicationInstancesResponse,
    CreateApplicationRequest,
    CreateDraftRequest,
    CreateProcessorRequest,
    CustomProcessorSourceInfo,
    DedicatedResources,
    DeleteApplicationInstancesRequest,
    DeleteApplicationInstancesResponse,
    DeleteApplicationRequest,
    DeleteDraftRequest,
    DeleteProcessorRequest,
    DeployApplicationRequest,
    DeployApplicationResponse,
    Draft,
    EmbeddingsExtractorConfig,
    GcsOutputConfig,
    GeneralObjectDetectionConfig,
    GetApplicationRequest,
    GetDraftRequest,
    GetInstanceRequest,
    GetProcessorRequest,
    Instance,
    LabelDetectorConfig,
    ListApplicationsRequest,
    ListApplicationsResponse,
    ListDraftsRequest,
    ListDraftsResponse,
    ListInstancesRequest,
    ListInstancesResponse,
    ListPrebuiltProcessorsRequest,
    ListPrebuiltProcessorsResponse,
    ListProcessorsRequest,
    ListProcessorsResponse,
    LocalOutputConfig,
    MachineSpec,
    MediaWarehouseConfig,
    Node,
    OccupancyCountConfig,
    OperationNotificationSettings,
    PersonalProtectiveEquipmentDetectionConfig,
    PersonBlurConfig,
    PersonVehicleDetectionConfig,
    PostProcessingConfig,
    Processor,
    ProcessorConfig,
    ProcessorIOSpec,
    ProductDetectorConfig,
    ProductRecognizerConfig,
    RemoveApplicationStreamInputRequest,
    RemoveApplicationStreamInputResponse,
    ResourceAnnotations,
    StreamWithAnnotation,
    TagParsingConfig,
    TagRecognizerConfig,
    UndeployApplicationRequest,
    UndeployApplicationResponse,
    UniversalInputConfig,
    UpdateApplicationInstancesRequest,
    UpdateApplicationInstancesResponse,
    UpdateApplicationRequest,
    UpdateApplicationStreamInputRequest,
    UpdateApplicationStreamInputResponse,
    UpdateDraftRequest,
    UpdateProcessorRequest,
    VertexAutoMLVideoConfig,
    VertexAutoMLVisionConfig,
    VertexCustomConfig,
    VideoStreamInputConfig,
    AcceleratorType,
    DataType,
    DeploymentEnvironment,
    ModelType,
)
from .streaming_resources import (
    GstreamerBufferDescriptor,
    Packet,
    PacketHeader,
    PacketType,
    RawImageDescriptor,
    SeriesMetadata,
    ServerMetadata,
)
from .streaming_service import (
    AcquireLeaseRequest,
    CommitRequest,
    ControlledMode,
    EagerMode,
    EventUpdate,
    Lease,
    ReceiveEventsControlResponse,
    ReceiveEventsRequest,
    ReceiveEventsResponse,
    ReceivePacketsControlResponse,
    ReceivePacketsRequest,
    ReceivePacketsResponse,
    ReleaseLeaseRequest,
    ReleaseLeaseResponse,
    RenewLeaseRequest,
    RequestMetadata,
    SendPacketsRequest,
    SendPacketsResponse,
    LeaseType,
)
from .streams_resources import (
    Channel,
    Event,
    Series,
    Stream,
)
from .streams_service import (
    CreateClusterRequest,
    CreateEventRequest,
    CreateSeriesRequest,
    CreateStreamRequest,
    DeleteClusterRequest,
    DeleteEventRequest,
    DeleteSeriesRequest,
    DeleteStreamRequest,
    GenerateStreamHlsTokenRequest,
    GenerateStreamHlsTokenResponse,
    GetClusterRequest,
    GetEventRequest,
    GetSeriesRequest,
    GetStreamRequest,
    GetStreamThumbnailRequest,
    GetStreamThumbnailResponse,
    ListClustersRequest,
    ListClustersResponse,
    ListEventsRequest,
    ListEventsResponse,
    ListSeriesRequest,
    ListSeriesResponse,
    ListStreamsRequest,
    ListStreamsResponse,
    MaterializeChannelRequest,
    UpdateClusterRequest,
    UpdateEventRequest,
    UpdateSeriesRequest,
    UpdateStreamRequest,
)
from .warehouse import (
    AddCollectionItemRequest,
    AddCollectionItemResponse,
    AnalyzeAssetMetadata,
    AnalyzeAssetRequest,
    AnalyzeAssetResponse,
    AnalyzeCorpusMetadata,
    AnalyzeCorpusRequest,
    AnalyzeCorpusResponse,
    Annotation,
    AnnotationCustomizedStruct,
    AnnotationList,
    AnnotationMatchingResult,
    AnnotationValue,
    Asset,
    AssetSource,
    BoolValue,
    CircleArea,
    ClipAssetRequest,
    ClipAssetResponse,
    Collection,
    CollectionItem,
    Corpus,
    CreateAnnotationRequest,
    CreateAssetRequest,
    CreateCollectionMetadata,
    CreateCollectionRequest,
    CreateCorpusMetadata,
    CreateCorpusRequest,
    CreateDataSchemaRequest,
    CreateIndexEndpointMetadata,
    CreateIndexEndpointRequest,
    CreateIndexMetadata,
    CreateIndexRequest,
    CreateSearchConfigRequest,
    CreateSearchHypernymRequest,
    Criteria,
    DataSchema,
    DataSchemaDetails,
    DateTimeRange,
    DateTimeRangeArray,
    DeleteAnnotationRequest,
    DeleteAssetMetadata,
    DeleteAssetRequest,
    DeleteCollectionMetadata,
    DeleteCollectionRequest,
    DeleteCorpusRequest,
    DeleteDataSchemaRequest,
    DeleteIndexEndpointMetadata,
    DeleteIndexEndpointRequest,
    DeleteIndexMetadata,
    DeleteIndexRequest,
    DeleteSearchConfigRequest,
    DeleteSearchHypernymRequest,
    DeployedIndex,
    DeployedIndexReference,
    DeployIndexMetadata,
    DeployIndexRequest,
    DeployIndexResponse,
    FacetBucket,
    FacetGroup,
    FacetProperty,
    FacetValue,
    FloatRange,
    FloatRangeArray,
    GenerateHlsUriRequest,
    GenerateHlsUriResponse,
    GenerateRetrievalUrlRequest,
    GenerateRetrievalUrlResponse,
    GeoCoordinate,
    GeoLocationArray,
    GetAnnotationRequest,
    GetAssetRequest,
    GetCollectionRequest,
    GetCorpusRequest,
    GetDataSchemaRequest,
    GetIndexEndpointRequest,
    GetIndexRequest,
    GetSearchConfigRequest,
    GetSearchHypernymRequest,
    ImageQuery,
    ImportAssetsMetadata,
    ImportAssetsRequest,
    ImportAssetsResponse,
    Index,
    IndexAssetMetadata,
    IndexAssetRequest,
    IndexAssetResponse,
    IndexedAsset,
    IndexEndpoint,
    IndexingStatus,
    IngestAssetRequest,
    IngestAssetResponse,
    IntRange,
    IntRangeArray,
    ListAnnotationsRequest,
    ListAnnotationsResponse,
    ListAssetsRequest,
    ListAssetsResponse,
    ListCollectionsRequest,
    ListCollectionsResponse,
    ListCorporaRequest,
    ListCorporaResponse,
    ListDataSchemasRequest,
    ListDataSchemasResponse,
    ListIndexEndpointsRequest,
    ListIndexEndpointsResponse,
    ListIndexesRequest,
    ListIndexesResponse,
    ListSearchConfigsRequest,
    ListSearchConfigsResponse,
    ListSearchHypernymsRequest,
    ListSearchHypernymsResponse,
    Partition,
    RemoveCollectionItemRequest,
    RemoveCollectionItemResponse,
    RemoveIndexAssetMetadata,
    RemoveIndexAssetRequest,
    RemoveIndexAssetResponse,
    SchemaKeySortingStrategy,
    SearchAssetsRequest,
    SearchAssetsResponse,
    SearchCapability,
    SearchCapabilitySetting,
    SearchConfig,
    SearchCriteriaProperty,
    SearchHypernym,
    SearchIndexEndpointRequest,
    SearchIndexEndpointResponse,
    SearchResultItem,
    StringArray,
    UndeployIndexMetadata,
    UndeployIndexRequest,
    UndeployIndexResponse,
    UpdateAnnotationRequest,
    UpdateAssetRequest,
    UpdateCollectionRequest,
    UpdateCorpusRequest,
    UpdateDataSchemaRequest,
    UpdateIndexEndpointMetadata,
    UpdateIndexEndpointRequest,
    UpdateIndexMetadata,
    UpdateIndexRequest,
    UpdateSearchConfigRequest,
    UpdateSearchHypernymRequest,
    UploadAssetMetadata,
    UploadAssetRequest,
    UploadAssetResponse,
    UserSpecifiedAnnotation,
    ViewCollectionItemsRequest,
    ViewCollectionItemsResponse,
    ViewIndexedAssetsRequest,
    ViewIndexedAssetsResponse,
    FacetBucketType,
)

__all__ = (
    'AppPlatformCloudFunctionRequest',
    'AppPlatformCloudFunctionResponse',
    'AppPlatformEventBody',
    'AppPlatformMetadata',
    'ClassificationPredictionResult',
    'ImageObjectDetectionPredictionResult',
    'ImageSegmentationPredictionResult',
    'NormalizedPolygon',
    'NormalizedPolyline',
    'NormalizedVertex',
    'ObjectDetectionPredictionResult',
    'OccupancyCountingPredictionResult',
    'PersonalProtectiveEquipmentDetectionOutput',
    'StreamAnnotation',
    'StreamAnnotations',
    'VideoActionRecognitionPredictionResult',
    'VideoClassificationPredictionResult',
    'VideoObjectTrackingPredictionResult',
    'StreamAnnotationType',
    'Cluster',
    'GcsDestination',
    'GcsSource',
    'OperationMetadata',
    'Point2D',
    'Polygon2D',
    'AnalysisDefinition',
    'AnalyzerDefinition',
    'AttributeValue',
    'OperatorDefinition',
    'ResourceSpecification',
    'RunStatus',
    'RunMode',
    'Analysis',
    'Operator',
    'Process',
    'BatchRunProcessRequest',
    'BatchRunProcessResponse',
    'CreateAnalysisRequest',
    'CreateOperatorRequest',
    'CreateProcessRequest',
    'DeleteAnalysisRequest',
    'DeleteOperatorRequest',
    'DeleteProcessRequest',
    'GetAnalysisRequest',
    'GetOperatorRequest',
    'GetProcessRequest',
    'ListAnalysesRequest',
    'ListAnalysesResponse',
    'ListOperatorsRequest',
    'ListOperatorsResponse',
    'ListProcessesRequest',
    'ListProcessesResponse',
    'OperatorQuery',
    'ResolveOperatorInfoRequest',
    'ResolveOperatorInfoResponse',
    'UpdateAnalysisRequest',
    'UpdateOperatorRequest',
    'UpdateProcessRequest',
    'Registry',
    'AddApplicationStreamInputRequest',
    'AddApplicationStreamInputResponse',
    'AIEnabledDevicesInputConfig',
    'Application',
    'ApplicationConfigs',
    'ApplicationInstance',
    'ApplicationNodeAnnotation',
    'ApplicationStreamInput',
    'AutoscalingMetricSpec',
    'BigQueryConfig',
    'CreateApplicationInstancesRequest',
    'CreateApplicationInstancesResponse',
    'CreateApplicationRequest',
    'CreateDraftRequest',
    'CreateProcessorRequest',
    'CustomProcessorSourceInfo',
    'DedicatedResources',
    'DeleteApplicationInstancesRequest',
    'DeleteApplicationInstancesResponse',
    'DeleteApplicationRequest',
    'DeleteDraftRequest',
    'DeleteProcessorRequest',
    'DeployApplicationRequest',
    'DeployApplicationResponse',
    'Draft',
    'EmbeddingsExtractorConfig',
    'GcsOutputConfig',
    'GeneralObjectDetectionConfig',
    'GetApplicationRequest',
    'GetDraftRequest',
    'GetInstanceRequest',
    'GetProcessorRequest',
    'Instance',
    'LabelDetectorConfig',
    'ListApplicationsRequest',
    'ListApplicationsResponse',
    'ListDraftsRequest',
    'ListDraftsResponse',
    'ListInstancesRequest',
    'ListInstancesResponse',
    'ListPrebuiltProcessorsRequest',
    'ListPrebuiltProcessorsResponse',
    'ListProcessorsRequest',
    'ListProcessorsResponse',
    'LocalOutputConfig',
    'MachineSpec',
    'MediaWarehouseConfig',
    'Node',
    'OccupancyCountConfig',
    'OperationNotificationSettings',
    'PersonalProtectiveEquipmentDetectionConfig',
    'PersonBlurConfig',
    'PersonVehicleDetectionConfig',
    'PostProcessingConfig',
    'Processor',
    'ProcessorConfig',
    'ProcessorIOSpec',
    'ProductDetectorConfig',
    'ProductRecognizerConfig',
    'RemoveApplicationStreamInputRequest',
    'RemoveApplicationStreamInputResponse',
    'ResourceAnnotations',
    'StreamWithAnnotation',
    'TagParsingConfig',
    'TagRecognizerConfig',
    'UndeployApplicationRequest',
    'UndeployApplicationResponse',
    'UniversalInputConfig',
    'UpdateApplicationInstancesRequest',
    'UpdateApplicationInstancesResponse',
    'UpdateApplicationRequest',
    'UpdateApplicationStreamInputRequest',
    'UpdateApplicationStreamInputResponse',
    'UpdateDraftRequest',
    'UpdateProcessorRequest',
    'VertexAutoMLVideoConfig',
    'VertexAutoMLVisionConfig',
    'VertexCustomConfig',
    'VideoStreamInputConfig',
    'AcceleratorType',
    'DataType',
    'DeploymentEnvironment',
    'ModelType',
    'GstreamerBufferDescriptor',
    'Packet',
    'PacketHeader',
    'PacketType',
    'RawImageDescriptor',
    'SeriesMetadata',
    'ServerMetadata',
    'AcquireLeaseRequest',
    'CommitRequest',
    'ControlledMode',
    'EagerMode',
    'EventUpdate',
    'Lease',
    'ReceiveEventsControlResponse',
    'ReceiveEventsRequest',
    'ReceiveEventsResponse',
    'ReceivePacketsControlResponse',
    'ReceivePacketsRequest',
    'ReceivePacketsResponse',
    'ReleaseLeaseRequest',
    'ReleaseLeaseResponse',
    'RenewLeaseRequest',
    'RequestMetadata',
    'SendPacketsRequest',
    'SendPacketsResponse',
    'LeaseType',
    'Channel',
    'Event',
    'Series',
    'Stream',
    'CreateClusterRequest',
    'CreateEventRequest',
    'CreateSeriesRequest',
    'CreateStreamRequest',
    'DeleteClusterRequest',
    'DeleteEventRequest',
    'DeleteSeriesRequest',
    'DeleteStreamRequest',
    'GenerateStreamHlsTokenRequest',
    'GenerateStreamHlsTokenResponse',
    'GetClusterRequest',
    'GetEventRequest',
    'GetSeriesRequest',
    'GetStreamRequest',
    'GetStreamThumbnailRequest',
    'GetStreamThumbnailResponse',
    'ListClustersRequest',
    'ListClustersResponse',
    'ListEventsRequest',
    'ListEventsResponse',
    'ListSeriesRequest',
    'ListSeriesResponse',
    'ListStreamsRequest',
    'ListStreamsResponse',
    'MaterializeChannelRequest',
    'UpdateClusterRequest',
    'UpdateEventRequest',
    'UpdateSeriesRequest',
    'UpdateStreamRequest',
    'AddCollectionItemRequest',
    'AddCollectionItemResponse',
    'AnalyzeAssetMetadata',
    'AnalyzeAssetRequest',
    'AnalyzeAssetResponse',
    'AnalyzeCorpusMetadata',
    'AnalyzeCorpusRequest',
    'AnalyzeCorpusResponse',
    'Annotation',
    'AnnotationCustomizedStruct',
    'AnnotationList',
    'AnnotationMatchingResult',
    'AnnotationValue',
    'Asset',
    'AssetSource',
    'BoolValue',
    'CircleArea',
    'ClipAssetRequest',
    'ClipAssetResponse',
    'Collection',
    'CollectionItem',
    'Corpus',
    'CreateAnnotationRequest',
    'CreateAssetRequest',
    'CreateCollectionMetadata',
    'CreateCollectionRequest',
    'CreateCorpusMetadata',
    'CreateCorpusRequest',
    'CreateDataSchemaRequest',
    'CreateIndexEndpointMetadata',
    'CreateIndexEndpointRequest',
    'CreateIndexMetadata',
    'CreateIndexRequest',
    'CreateSearchConfigRequest',
    'CreateSearchHypernymRequest',
    'Criteria',
    'DataSchema',
    'DataSchemaDetails',
    'DateTimeRange',
    'DateTimeRangeArray',
    'DeleteAnnotationRequest',
    'DeleteAssetMetadata',
    'DeleteAssetRequest',
    'DeleteCollectionMetadata',
    'DeleteCollectionRequest',
    'DeleteCorpusRequest',
    'DeleteDataSchemaRequest',
    'DeleteIndexEndpointMetadata',
    'DeleteIndexEndpointRequest',
    'DeleteIndexMetadata',
    'DeleteIndexRequest',
    'DeleteSearchConfigRequest',
    'DeleteSearchHypernymRequest',
    'DeployedIndex',
    'DeployedIndexReference',
    'DeployIndexMetadata',
    'DeployIndexRequest',
    'DeployIndexResponse',
    'FacetBucket',
    'FacetGroup',
    'FacetProperty',
    'FacetValue',
    'FloatRange',
    'FloatRangeArray',
    'GenerateHlsUriRequest',
    'GenerateHlsUriResponse',
    'GenerateRetrievalUrlRequest',
    'GenerateRetrievalUrlResponse',
    'GeoCoordinate',
    'GeoLocationArray',
    'GetAnnotationRequest',
    'GetAssetRequest',
    'GetCollectionRequest',
    'GetCorpusRequest',
    'GetDataSchemaRequest',
    'GetIndexEndpointRequest',
    'GetIndexRequest',
    'GetSearchConfigRequest',
    'GetSearchHypernymRequest',
    'ImageQuery',
    'ImportAssetsMetadata',
    'ImportAssetsRequest',
    'ImportAssetsResponse',
    'Index',
    'IndexAssetMetadata',
    'IndexAssetRequest',
    'IndexAssetResponse',
    'IndexedAsset',
    'IndexEndpoint',
    'IndexingStatus',
    'IngestAssetRequest',
    'IngestAssetResponse',
    'IntRange',
    'IntRangeArray',
    'ListAnnotationsRequest',
    'ListAnnotationsResponse',
    'ListAssetsRequest',
    'ListAssetsResponse',
    'ListCollectionsRequest',
    'ListCollectionsResponse',
    'ListCorporaRequest',
    'ListCorporaResponse',
    'ListDataSchemasRequest',
    'ListDataSchemasResponse',
    'ListIndexEndpointsRequest',
    'ListIndexEndpointsResponse',
    'ListIndexesRequest',
    'ListIndexesResponse',
    'ListSearchConfigsRequest',
    'ListSearchConfigsResponse',
    'ListSearchHypernymsRequest',
    'ListSearchHypernymsResponse',
    'Partition',
    'RemoveCollectionItemRequest',
    'RemoveCollectionItemResponse',
    'RemoveIndexAssetMetadata',
    'RemoveIndexAssetRequest',
    'RemoveIndexAssetResponse',
    'SchemaKeySortingStrategy',
    'SearchAssetsRequest',
    'SearchAssetsResponse',
    'SearchCapability',
    'SearchCapabilitySetting',
    'SearchConfig',
    'SearchCriteriaProperty',
    'SearchHypernym',
    'SearchIndexEndpointRequest',
    'SearchIndexEndpointResponse',
    'SearchResultItem',
    'StringArray',
    'UndeployIndexMetadata',
    'UndeployIndexRequest',
    'UndeployIndexResponse',
    'UpdateAnnotationRequest',
    'UpdateAssetRequest',
    'UpdateCollectionRequest',
    'UpdateCorpusRequest',
    'UpdateDataSchemaRequest',
    'UpdateIndexEndpointMetadata',
    'UpdateIndexEndpointRequest',
    'UpdateIndexMetadata',
    'UpdateIndexRequest',
    'UpdateSearchConfigRequest',
    'UpdateSearchHypernymRequest',
    'UploadAssetMetadata',
    'UploadAssetRequest',
    'UploadAssetResponse',
    'UserSpecifiedAnnotation',
    'ViewCollectionItemsRequest',
    'ViewCollectionItemsResponse',
    'ViewIndexedAssetsRequest',
    'ViewIndexedAssetsResponse',
    'FacetBucketType',
)
