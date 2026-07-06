from pydantic import BaseModel,ConfigDict,Field

from . import field_element as FE


class EPCISMaster(BaseModel):
    model_config=ConfigDict(
        extra="allow",
        populate_by_name=True,
        validate_assignment=True,
    )

    vocabularyList: list[FE.Vocabulary]=Field(default_factory=list)
