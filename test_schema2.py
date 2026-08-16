from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel, Field, WithJsonSchema
import json

StrictDecimal = Annotated[
    Decimal, WithJsonSchema({"type": "number", "format": "decimal"})
]


class EmployeeUpdate(BaseModel):
    salary: StrictDecimal | None = Field(
        None, ge=Decimal("0.01"), le=Decimal("99999999.99")
    )


schema = EmployeeUpdate.model_json_schema()
print(json.dumps(schema["properties"]["salary"], indent=2))
