from typing import Annotated, Self
from pydantic import BaseModel, AfterValidator, model_validator


class Testar(BaseModel):
    myint: Annotated[int, AfterValidator(lambda v: v + 1)]

    @model_validator(mode="after")
    def validator(self) -> Self:
        self.myint += 1
        return self


Testar(myint=1)
