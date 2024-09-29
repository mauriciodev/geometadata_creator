from typing import Literal
from typing_extensions import Self
from pydantic import (
    BaseModel,
    model_validator,
    Field,
)
from core.fields import FileExtractedFields as FEF


class FileExtractedFields(BaseModel):
    north_bound_lat: float = Field(alias=FEF.north_bound_lat)
    south_bound_lat: float = Field(alias=FEF.south_bound_lat)
    east_bound_lon: float = Field(alias=FEF.east_bound_lon)
    west_bound_lon: float = Field(alias=FEF.west_bound_lon)
    data_representation_type: Literal["Matricial", "Vetorial"] = Field(
        alias=FEF.data_representation_type
    )
    epsg_code: int = Field(alias=FEF.epsg_code)
    driver: str = Field(alias=FEF.driver)
    scale_denominator1: int = Field(alias=FEF.scale_denominator1)
    scale_denominator2: int = Field(alias=FEF.scale_denominator2)
    inom: str = Field(alias=FEF.inom)
    mi: str = Field(alias=FEF.mi)
    spatial_resolution: int | None = Field(alias=FEF.spatial_resolution, default=None)

    @model_validator(mode="after")
    def check_model_validation(self) -> Self:
        # Check that the driver is correct
        format_alias = {"GTif": "GeoTiff"}
        self.driver = (
            format_alias[self.driver]
            if self.driver in format_alias.keys()
            else self.driver
        )

        # Check that the ...
        contour_lines_height = {10000: 5, 25000: 10, 50000: 20, 100000: 50, 250000: 100}
        if self.spatial_resolution in contour_lines_height:
            self.spatial_resolution = contour_lines_height[self.spatial_resolution]
        else:
            self.spatial_resolution = None

        return self

    @classmethod
    def from_fields(cls, data: dict):
        mapped_fields = set(f.value for f in FEF)

        return FileExtractedFields(
            **{
                (FEF(label) if label in mapped_fields else label): value
                for label, value in data.items()
            }
        )

    def dump_fields(self):
        return {FEF[name].value: value for name, value in self}
