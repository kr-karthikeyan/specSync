import streamlit as st
import os
import json
from dotenv import load_dotenv

from src.utils.file_reader import get_api_key
from src.parsers.pdf_parser import extract_text_from_pdf
from src.parsers.docx_parser import extract_text_from_docx
from src.parsers.text_parser import extract_text_from_txt
from src.generators.blueprint_generator import generate_blueprint
import streamlit.components.v1 as components


# Load environment variables from .env file
# Must be called before get_api_key()
load_dotenv()

# st.set_page_config must be the FIRST streamlit command in the file
# It sets the browser tab title, icon, and layout
st.set_page_config(
    page_title="SpecSync",         # browser tab title
    page_icon="📋",                # browser tab icon
    layout="wide"                  # use full screen width
)

# st.title renders a large H1 heading
st.title("📋 SpecSync")

# st.markdown renders any markdown text
# The HTML <br> adds breathing space below
st.markdown("**PRD to Blueprint — instantly.** Paste your Product Requirements Document and get a complete technical blueprint.")
st.markdown("<br>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")

    # Let user choose which AI provider to use
    provider = st.radio(
        "AI Provider",
        options=["openai", "groq"],
        format_func=lambda x: "OpenAI (paid)" if x == "openai" else "Groq (free)"
    )

    # Show appropriate label based on selection
    key_label = "OpenAI API Key" if provider == "openai" else "Groq API Key"
    env_var = "OPENAI_API_KEY" if provider == "openai" else "GROQ_API_KEY"

    # Try loading from .env first
    try:
        api_key = os.getenv(env_var)
        if not api_key:
            raise ValueError("Key not found")
        st.success(f"{key_label} loaded from .env")
    except:
        api_key = st.text_input(
            f"Enter your {key_label}",
            type="password"
        )


        st.subheader("1. Upload your PRD")

# st.radio renders radio buttons for single selection
input_method = st.radio(
    "How would you like to provide your PRD?",
    options=["Paste Text", "Upload File"],
    horizontal=True    # display buttons side by side
)

# Initialize prd_text as empty string
# This variable will hold the extracted PRD content
prd_text = ""


# Show different UI based on what the user selected
if input_method == "Paste Text":
    
    # st.text_area renders a multi-line text input
    # height controls how tall the box is in pixels
    prd_text = st.text_area(
        "Paste your PRD here",
        height=300,
        placeholder="Describe your product requirements here..."
    )

elif input_method == "Upload File":
    
    # st.file_uploader renders a drag-and-drop upload box
    # type limits which file types are accepted
    uploaded_file = st.file_uploader(
        "Upload your PRD document",
        type=["pdf", "docx", "txt"]
    )
    
    # Only process if user actually uploaded something
    if uploaded_file is not None:
        
        # Save the uploaded file temporarily to disk
        # We need a file path to pass to our parsers
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Build the full file path
        # uploaded_file.name is the original filename
        file_path = os.path.join(upload_dir, uploaded_file.name)
        
        # Write the file to disk
        # "wb" means write in binary mode — works for all file types
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Now extract text based on file type
        # uploaded_file.name gives us the filename including extension
        if uploaded_file.name.endswith(".pdf"):
            prd_text = extract_text_from_pdf(file_path)
            
        elif uploaded_file.name.endswith(".docx"):
            prd_text = extract_text_from_docx(file_path)
            
        elif uploaded_file.name.endswith(".txt"):
            prd_text = extract_text_from_txt(file_path)
        
        # st.info shows a blue info box
        st.info(f"File uploaded: {uploaded_file.name}")


        st.markdown("<br>", unsafe_allow_html=True)
st.subheader("2. Generate Blueprint")

# st.button renders a clickable button
# Returns True when clicked, False otherwise
if st.button("⚡ Generate Blueprint", type="primary"):
    
    # Validate inputs before calling AI
    if not prd_text:
        # st.error shows a red error box
        st.error("Please provide a PRD first.")
    
    elif not api_key:
        st.error("Please provide your OpenAI API key.")
    
    else:
        # st.spinner shows a loading animation while code runs
        with st.spinner("Analysing your PRD and generating blueprint..."):
            
            # Call our AI generator
            # This is where everything connects together
            blueprint = generate_blueprint(prd_text, api_key, provider)
        
        # Show success message
        st.success("Blueprint generated successfully!")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ---- API Contract Section ----
        st.subheader("📡 API Contract")
        
        # Loop through each endpoint and display it
        for endpoint in blueprint.api_contract.endpoints:
            
            # st.expander creates a collapsible section
            # Label shows the method and route
            with st.expander(f"{endpoint.method} {endpoint.route}"):
                st.write(f"**Description:** {endpoint.description}")
                st.write(f"**Status codes:** {endpoint.status_codes}")
                
                if endpoint.request_body and endpoint.request_body.fields:
                    st.write("**Request body:**")
                    # st.json renders a formatted, collapsible JSON viewer
                    st.json(endpoint.request_body.fields)
                
                if endpoint.response_body and endpoint.response_body.fields:
                    st.write("**Response body:**")
                    st.json(endpoint.response_body.fields)
        
        # ---- Database Schema Section ----
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🗄️ Database Schema")
        
        for table in blueprint.database_schema.tables:
            with st.expander(f"Table: {table.name}"):
                
                # Build a list of dicts for the table display
                columns_data = []
                for col in table.columns:
                    columns_data.append({
                        "Column": col.name,
                        "Type": col.data_type,
                        "Primary Key": "✅" if col.is_primary_key else "❌",
                        "Nullable": "✅" if col.nullable else "❌",
                        "Notes": col.notes or ""
                    })
                
                # st.table renders a clean static table
                st.table(columns_data)
        
        # ---- Component Tree Section ----
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🧩 Component Tree")
        
        for component in blueprint.component_tree.components:
            with st.expander(f"{component.name} — {component.page}"):
                st.write(f"**Props:** {', '.join(component.props) if component.props else 'None'}")
                st.write(f"**Children:** {', '.join(component.children) if component.children else 'None'}")
        

        # ---- User Flow Diagram Section ----
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔀 User Flow Diagram")

        # Build HTML that loads Mermaid.js and renders our diagram
        # We embed the diagram string directly into the HTML
        mermaid_html = f"""
        <div class="mermaid">
        {blueprint.user_flow_diagram}
        </div>

        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
        """

        # Render the HTML inside Streamlit
        # height controls the box size — adjust if diagram looks cut off
        components.html(mermaid_html, height=400, scrolling=True)

        # Keep the raw code visible too — useful for copying into docs
        with st.expander("View raw Mermaid code"):
            st.code(blueprint.user_flow_diagram, language="mermaid")
        
        # ---- Export Section ----
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📥 Export Blueprint")
        
        # Convert blueprint to JSON string for download
        # model_dump() converts Pydantic model → Python dict
        # json.dumps() converts dict → formatted JSON string
        # indent=2 makes it human readable with 2 space indentation
        blueprint_json = json.dumps(blueprint.model_dump(), indent=2)
        
        # st.download_button renders a download button
        # Clicking it saves the file to the user's computer
        st.download_button(
            label="⬇️ Download as JSON",
            data=blueprint_json,
            file_name="specsync_blueprint.json",
            mime="application/json"
        )

