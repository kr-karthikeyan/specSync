def build_blueprint_prompt(prd_text: str) -> str:
    """
    Builds the prompt we send to OpenAI.
    A good prompt = good output. This is the core of SpecSync.
    
    prd_text: the raw text extracted from the PRD document
    returns: a carefully structured prompt string
    """

    # This is an f-string — it embeds prd_text directly into the prompt
    prompt = f"""
You are a senior software architect. 
Analyze the following Product Requirements Document (PRD) and generate a complete technical blueprint.

Return your response as a valid JSON object with exactly this structure:

{{
  "api_contract": {{
    "project_name": "string",
    "endpoints": [
      {{
        "method": "GET | POST | PUT | DELETE",
        "route": "/api/example",
        "description": "what this endpoint does",
        "request_body": {{
          "fields": {{
            "field_name": "field_type"
          }}
        }},
        "response_body": {{
          "fields": {{
            "field_name": "field_type"
          }}
        }},
        "status_codes": [200, 400, 404]
      }}
    ]
  }},
  "database_schema": {{
    "tables": [
      {{
        "name": "table_name",
        "columns": [
          {{
            "name": "column_name",
            "data_type": "INTEGER | VARCHAR | BOOLEAN | TIMESTAMP",
            "is_primary_key": true,
            "nullable": false,
            "notes": "any extra info"
          }}
        ]
      }}
    ]
  }},
  "component_tree": {{
    "components": [
      {{
        "name": "ComponentName",
        "page": "PageName",
        "props": ["prop1", "prop2"],
        "children": ["ChildComponent1"]
      }}
    ]
  }},
  "user_flow_diagram": "graph TD\\n  A[User] --> B[Login Page]\\n  B --> C[Dashboard]"
}}

Important rules:
- Return ONLY the JSON. No explanation, no markdown, no code blocks.
- The user_flow_diagram must be a valid Mermaid.js graph string.
- Extract as many endpoints, tables, and components as the PRD implies.
- If something is unclear in the PRD, make a reasonable technical assumption.

PRD Document:
--------------
{prd_text}
--------------

Now generate the blueprint JSON:
"""
    return prompt