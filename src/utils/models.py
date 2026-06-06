from pydantic import BaseModel
from typing import List, Optional

class RequestBody(BaseModel):
    fields: Optional[dict] = None

class ResponseBody(BaseModel):
    fields: Optional[dict] = None

class APIEndpoint(BaseModel):
    method: str
    route: str
    description: str
    request_body: Optional[RequestBody] = None
    response_body: Optional[ResponseBody] = None
    status_codes: List[int] = []

class APIContract(BaseModel):
    project_name: str
    endpoints: List[APIEndpoint] = []

class DBColumn(BaseModel):
    name: str
    data_type: str
    is_primary_key: bool = False
    nullable: bool = True
    notes: Optional[str] = None

class DBTable(BaseModel):
    name: str
    columns: List[DBColumn] = []

class DatabaseSchema(BaseModel):
    tables: List[DBTable] = []

class UIComponent(BaseModel):
    name: str
    page: str
    props: List[str] = []
    children: List[str] = []

class ComponentTree(BaseModel):
    components: List[UIComponent] = []

class Blueprint(BaseModel):
    api_contract: APIContract
    database_schema: DatabaseSchema
    component_tree: ComponentTree
    user_flow_diagram: str = ""