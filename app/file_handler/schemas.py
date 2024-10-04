from typing import Literal
from typing_extensions import Self
from pydantic import (
    BaseModel,
    model_validator,
    Field,
)
from core.fields import FileGeoDataFields as FEF
from numpy import allclose


class FileExtractedFields(BaseModel):
    north_bound_lat: float = Field(alias=FEF.north_bound_lat.name)
    south_bound_lat: float = Field(alias=FEF.south_bound_lat.name)
    east_bound_lon: float = Field(alias=FEF.east_bound_lon.name)
    west_bound_lon: float = Field(alias=FEF.west_bound_lon.name)
    data_representation_type: Literal["Matricial", "Vetorial"] = Field(
        alias=FEF.data_representation_type.name, default="Matricial"
    )
    epsg_code: int = Field(alias=FEF.epsg_code.name)
    driver: str = Field(alias=FEF.driver.name)
    scale_denominator1: int = Field(alias=FEF.scale_denominator1.name)
    scale_denominator2: int = Field(alias=FEF.scale_denominator2.name)
    inom: str = Field(alias=FEF.inom.name)
    mi: str = Field(alias=FEF.mi.name)
    spatial_resolution: int | None = Field(
        alias=FEF.spatial_resolution.name, default=None
    )

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

    @classmethod
    def _compare(cls, v1, v2) -> bool:
        if isinstance(v1, float) and isinstance(v2, float):
            return allclose(v1, v2)
        else:
            return v1 == v2

    def compare(self, other) -> dict:
        differences = {}

        other_dict = other.dump_fields()
        for key, v1 in self.dump_fields().items():
            if not self._compare(v1, other_dict[key]):
                differences[key] = f"{v1} != {other_dict[key]}"

        return differences
