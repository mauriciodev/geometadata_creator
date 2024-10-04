from enum import StrEnum


class UniversalFields(StrEnum):
    product_type = "MD_Identification-citation-series-name"


class CadastroGeralFields(StrEnum):
    metadata_responsible_individual = "MD_Metadata-contact-individualName"
    metadata_responsible_organization = "MD_Metadata-contact-organisationName"
    metadata_project = "MD_Identification-citation-collectiveTitle"
    vertical_datum = "MD_DataIdentification-extent-verticalExtent-verticalDatum"


class FileGeoDataFields(StrEnum):
    north_bound_lat = (
        "MD_DataIdentification-extent-geographicElement1-northBoundLatitude"
    )
    south_bound_lat = (
        "MD_DataIdentification-extent-geographicElement1-southBoundLatitude"
    )
    east_bound_lon = (
        "MD_DataIdentification-extent-geographicElement1-eastBoundLongitude"
    )
    west_bound_lon = (
        "MD_DataIdentification-extent-geographicElement1-westBoundLongitude"
    )
    data_representation_type = "MD_DataIdentification-spatialRepresentationType"
    epsg_code = "MD_ReferenceSystem-referenceSystemIdentifier-code"
    driver = "MD_Distribution-distributionFormat-name"
    scale_denominator1 = (
        "MD_DataIdentification-spatialResolution-equivalentScale-denominator1"
    )
    scale_denominator2 = (
        "MD_DataIdentification-spatialResolution-equivalentScale-denominator2"
    )
    inom = "MD_Identification-citation-alternateTitle"
    mi = "MD_Identification-citation-alternateTitle"
    spatial_resolution = "MD_DataIdentification-spatialResolution-distance"
