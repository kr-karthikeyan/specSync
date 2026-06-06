def build_api_prompt(prd_text: str) -> str:
    """
    Focused prompt for API contract only.
    Small output = no truncation.
    """
    return f"""
Analyze this PRD and return ONLY a JSON object for the API contract.
Maximum 5 endpoints. Keep descriptions under 8 words.

Return exactly this structure:
{{
  "project_name": "string",
  "endpoints": [
    {{
      "method": "GET",
      "route": "/api/example",
      "description": "short description",
      "request_body": {{"fields": {{"field": "type"}}}},
      "response_body": {{"fields": {{"field": "type"}}}},
      "status_codes": [200, 400]
    }}
  ]
}}

Rules:
- Return ONLY the JSON. Nothing else.
- Maximum 5 endpoints.
- No markdown, no explanation.

PRD:
{prd_text}
"""


def build_schema_prompt(prd_text: str) -> str:
    """
    Focused prompt for database schema only.
    Small output = no truncation.
    """
    return f"""
Analyze this PRD and return ONLY a JSON object for the database schema.
Maximum 4 tables. Keep it concise.

Return exactly this structure:
{{
  "tables": [
    {{
      "name": "table_name",
      "columns": [
        {{
          "name": "id",
          "data_type": "INTEGER",
          "is_primary_key": true,
          "nullable": false,
          "notes": ""
        }}
      ]
    }}
  ]
}}

Rules:
- Return ONLY the JSON. Nothing else.
- Maximum 4 tables, maximum 6 columns per table.
- No markdown, no explanation.

PRD:
{prd_text}
"""


def build_component_prompt(prd_text: str) -> str:
    """
    Focused prompt for component tree only.
    Small output = no truncation.
    """
    return f"""
Analyze this PRD and return ONLY a JSON object for the frontend component tree.
Maximum 6 components.

Return exactly this structure:
{{
  "components": [
    {{
      "name": "ComponentName",
      "page": "PageName",
      "props": ["prop1", "prop2"],
      "children": ["ChildComponent"]
    }}
  ]
}}

Rules:
- Return ONLY the JSON. Nothing else.
- Maximum 6 components.
- No markdown, no explanation.

PRD:
{prd_text}
"""


def build_flow_prompt(prd_text: str) -> str:
    """
    Focused prompt for user flow diagram only.
    Returns a Mermaid.js string — not JSON.
    """
    return f"""
Analyze this PRD and return ONLY a Mermaid.js flowchart string.
Maximum 8 nodes. Keep it simple.

Example format:
graph TD
  A[User] --> B[Login]
  B --> C[Dashboard]
  C --> D[Tasks]

Rules:
- Return ONLY the Mermaid diagram. Nothing else.
- No markdown code blocks, no explanation.
- Maximum 8 nodes.

PRD:
{prd_text}
"""