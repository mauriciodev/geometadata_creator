from enum import Enum


class UniversalFields(Enum):
    metadata_responsible_individual = "MD_Metadata-contact-individualName"
    metadata_responsible_organization = "MD_Metadata-contact-organisationName"
    metadata_project = "MD_Identification-citation-collectiveTitle"
    vertical_datum = "MD_DataIdentification-extent-verticalExtent-verticalDatum"
