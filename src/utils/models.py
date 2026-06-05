from pydantic import BaseModel
from typing import List, Optional

# ----------------------------
# API Contract Models
# ----------------------------

class RequestBody(BaseModel):
    """
    Represents the request body of one API endpoint.
    Example: { "user_id": "string", "email": "string" }
    """
    # Dict of field name → field type
    # Optional means this field can be missing — not all endpoints have a body
    fields: Optional[dict] = None


class ResponseBody(BaseModel):
    """
    Represents what the API returns.
    Example: { "token": "string", "expires_in": "integer" }
    """
    fields: Optional[dict] = None


class APIEndpoint(BaseModel):
    """
    One complete API endpoint definition.
    Example: POST /api/auth/login
    """
    # HTTP method — GET, POST, PUT, DELETE
    method: str

    # The URL route
    # Example: /api/users/{id}
    route: str

    # Short description of what this endpoint does
    description: str

    # What the client sends to this endpoint
    request_body: Optional[RequestBody] = None

    # What the endpoint returns
    response_body: Optional[ResponseBody] = None

    # HTTP status codes this endpoint can return
    # Example: [200, 400, 401, 404]
    status_codes: List[int] = []


class APIContract(BaseModel):
    """
    The complete API contract — a collection of all endpoints.
    This is the top-level object we return to the UI.
    """
    # Name of the project/feature these endpoints belong to
    project_name: str

    # List of all API endpoints found in the PRD
    endpoints: List[APIEndpoint] = []


# ----------------------------
# Database Schema Models
# ----------------------------

class DBColumn(BaseModel):
    """
    One column in a database table.
    Example: id (INTEGER, primary key)
    """
    # Column name
    name: str

    # Data type — INTEGER, VARCHAR, BOOLEAN, TIMESTAMP etc
    data_type: str

    # Is this the primary key?
    is_primary_key: bool = False

    # Can this column be NULL?
    nullable: bool = True

    # Extra notes — foreign key references, unique constraints etc
    notes: Optional[str] = None


class DBTable(BaseModel):
    """
    One complete database table.
    Example: users table with id, email, password columns
    """
    # Table name
    name: str

    # List of all columns in this table
    columns: List[DBColumn] = []


class DatabaseSchema(BaseModel):
    """
    The complete database schema — all tables together.
    """
    tables: List[DBTable] = []


# ----------------------------
# Component Tree Models
# ----------------------------

class UIComponent(BaseModel):
    """
    One frontend UI component.
    Example: LoginForm component with email and password props
    """
    # Component name
    # Example: UserDashboard, LoginForm, NavBar
    name: str

    # What page does this component belong to?
    page: str

    # What data does this component need?
    # Example: ["user_id", "email", "role"]
    props: List[str] = []

    # Child components nested inside this one
    children: List[str] = []


class ComponentTree(BaseModel):
    """
    The complete frontend component tree.
    """
    components: List[UIComponent] = []


# ----------------------------
# Full Blueprint Model
# ----------------------------

class Blueprint(BaseModel):
    """
    The master output object.
    Contains everything SpecSync generates from a PRD.
    This is what gets shown in the UI and exported.
    """
    api_contract: APIContract
    database_schema: DatabaseSchema
    component_tree: ComponentTree

    # Mermaid.js diagram string for the user flow
    # We'll generate this as a raw string
    user_flow_diagram: str = ""