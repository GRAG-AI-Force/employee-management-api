from app.schemas.employee import EmployeeUpdate
import json

schema = EmployeeUpdate.model_json_schema()
print(json.dumps(schema["properties"]["salary"], indent=2))
