# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the TravelPlanner requirements and produce a complete design_spec.md detailing all pages, elements, interactions, and data storage specifications.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst writes requirements_analysis.md from user task description; "
        "then WebArchitect reads requirements_analysis.md and writes design_spec.md covering Flask routes, page titles, element IDs, "
        "navigation methods, data contracts for local text files, and interactions."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "prompt": """You are a Requirements Analyst specializing in software requirement extraction for web applications.

Your goal is to extract and document all user-visible pages, UI elements, navigation flows, and data storage specifications precisely as described, enabling downstream design.

Task Details:
- Read user_task_description thoroughly
- Extract every page with exact page titles as given
- Extract all UI element IDs precisely, including dynamic IDs with patterns
- Capture all navigation buttons and their target pages/actions
- Document data storage format and example data file specifications exactly as specified
- Do NOT add authentication or any hidden features beyond the user task

Output Artifact:
- Write requirements_analysis.md with detailed pages, elements, navigation flows, and data file descriptions

Requirements:
- Maintain exact naming and IDs as specified
- Cover all 10 pages with their detailed elements
- Include data format lines and realistic example data
- Produce a clear, structured, human-readable markdown report

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as requirements_analysis.md
- Do NOT add or omit any user-visible page or element
- Preserve all exact field orders and file names for data files

Output: requirements_analysis.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "agent_name": "WebArchitect",
            "prompt": """You are a Web Architect specializing in full-stack web application design for Python Flask frameworks.

Your goal is to create a detailed design_spec.md translating requirements analysis into Flask route specifications, page templates with exact element IDs, navigation mappings, and data storage contracts for local text files.

Task Details:
- Read requirements_analysis.md and user_task_description carefully
- Specify Flask routes and HTTP methods for all pages with clear function names
- Define page titles and exact element IDs for each HTML template
- Specify template filenames matching page purposes
- Map navigation buttons to Flask route functions using url_for syntax
- Detail data file contracts for each local data file in data/*.txt including field orders and formats
- Include interactions like button functions and page linking

Output Artifact:
- Write comprehensive design_spec.md outlining backend routes, frontend elements, navigation, and data specs clearly for implementation

Requirements:
- Keep all element IDs exact as analyzed with no changes
- Use standard Flask conventions for route and function naming
- Maintain explicit data file field order and pipe-delimited format
- Clarify which templates correspond to which routes

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as design_spec.md
- Design must enable independent backend and frontend development based on this specification
- Follow exact data file naming and format as specified
- All page titles and element IDs must match input exactly

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "RequirementsAnalyst",
            "reviewer_agent": "WebArchitect",
            "review_criteria": "Ensure requirements_analysis.md covers every user-visible page, exact element IDs, navigation buttons, and data file format as specified.",
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "source_agent": "WebArchitect",
            "reviewer_agent": "BackendDeveloper",
            "review_criteria": "Verify design_spec.md is coherent, complete, and ready for implementation including precise Flask routing and data file usage.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the TravelPlanner Flask web application consisting of app_draft.py and templates_draft/*.html from design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "BackendDeveloper writes app_draft.py using design_spec.md with routes, local file data handling, and button navigation; "
        "FrontendDeveloper writes all templates_draft/*.html files implementing page layout, element IDs, forms, and buttons."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "prompt": """You are a Backend Developer specializing in Flask web applications.

Your goal is to develop a functional Flask backend implementation that matches design specifications.

Task Details:
- Read design_spec.md and user_task_description for project context
- Implement app_draft.py with all Flask routes as specified
- Use local text files for data storage, reading, and writing exactly as described
- Implement routing logic and button-triggered navigation per specification
- Output is app_draft.py fully implementing backend logic and routing

Implementation Requirements:
1. **Flask Application Setup**:
   ```python
   from flask import Flask, render_template, redirect, url_for, request
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'dev-secret-key'
   ```

2. **Routing and Methods**:
   - Implement ALL routes with correct HTTP methods (GET/POST) from design_spec.md
   - Routes must render templates or redirect as defined
   - Pass correct context variables to templates

3. **Data Handling**:
   - Read and write data to local text files in 'data/' folder
   - Parse and serialize pipe-delimited data files exactly as specified
   - Reflect changes in files when relevant (e.g., adding trips, bookings)

4. **Button-triggered Navigation**:
   - Implement backend handling for button actions navigating between pages
   - Use url_for and redirect as appropriate

5. **Error Handling**:
   - Gracefully handle file access errors and invalid inputs
   - Provide default empty lists or values when data missing

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save output as app_draft.py
- Strictly follow design_spec.md for routes, data structure, and navigation
- Do NOT include frontend code or templates here
- Do NOT assume data formats beyond those described
- Ensure function names, route paths, and context variables match specification exactly

Output: app_draft.py""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"}
            ]
        },
        {
            "agent_name": "FrontendDeveloper",
            "prompt": """You are a Frontend Developer specializing in HTML and Jinja2 templating for Flask web applications.

Your goal is to create complete HTML template files implementing all pages with specified element IDs and UI structure.

Task Details:
- Read design_spec.md and user_task_description to understand page layouts and UI requirements
- Implement ALL templates_draft/*.html files with all container divs, buttons, inputs, dropdowns, and other UI elements
- Use the exact element IDs as specified, including dynamic ID patterns
- Implement forms and buttons consistent with backend routing for user interactions
- Output final set of HTML files as templates_draft/*.html

Implementation Requirements:
1. **Template Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8" />
       <title>Page Title</title>
   </head>
   <body>
       <div id="container-id">
           <!-- Implement specified elements -->
       </div>
   </body>
   </html>
   ```

2. **Element IDs**:
   - Include all specified IDs exactly as provided (case-sensitive)
   - For dynamic IDs like view-destination-button-{dest_id}, use Jinja2 syntax:
     id="view-destination-button-{{ dest_id }}"

3. **Forms and Buttons**:
   - Forms must send data via POST where applicable
   - Button IDs must match specification
   - Navigation buttons link using url_for functions consistent with backend routes

4. **Page Titles and Headers**:
   - Use exact page titles as specified in design_spec.md in both <title> and <h1>

5. **Data Binding**:
   - Use Jinja2 variables passed from backend for dynamic data display
   - Iterate lists and conditionally display content as needed

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save each HTML template in templates_draft/
- Element IDs and page titles must match design_spec.md exactly
- Templates must be ready to integrate with Flask backend without modification
- Do NOT include backend code or data file handling here

Output: templates_draft/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDeveloper",
            "reviewer_agent": "FrontendDeveloper",
            "review_criteria": "Ensure app_draft.py routes correctly map to templates with proper reading/writing of local text data files.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "Tester",
            "review_criteria": "Validate templates_draft/*.html files contain all specified page elements, IDs, and navigation buttons consistent with backend routes.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate and finalize app.py and templates/*.html to ensure a fully functional TravelPlanner application meeting all specifications.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "Tester validates app_draft.py and templates_draft/*.html and produces validation_report.md; "
        "FinalIntegrator implements fixes from the report producing the final app.py and templates/*.html files."
    ),
    team: list = [
        {
            "agent_name": "Tester",
            "prompt": """You are a Software Test Engineer specializing in web application validation with expertise in Python Flask backend and HTML frontend.

Your goal is to perform comprehensive syntax, runtime, and functional validation of the draft backend and frontend artifacts to produce a detailed validation report with actionable findings.

Task Details:
- Read app_draft.py and all files in templates_draft/*.html along with design_spec.md and user_task_description
- Validate complete implementation correctness against specifications including routes, navigation, data file interactions, and presence of all UI elements with correct IDs
- Produce a validation_report.md that documents all syntax/runtime errors, missing or incorrect elements, navigation mismatches, and data handling issues with clear, actionable instructions
- Focus exclusively on the provided draft code and specification without suggesting new features

Validation Requirements:
1. **Python Backend Validation**:
   - Use validate_python_file tool to check syntax and runtime errors on app_draft.py
   - Execute critical paths where possible to verify dynamic functionality
   - Confirm all Flask routes match design_spec.md routes exactly, including HTTP methods and context variables
   - Verify data file reading conforms to specified field orders and handles errors gracefully

2. **Frontend Templates Validation**:
   - Check all required HTML elements with exact IDs exist in templates_draft/*.html
   - Confirm page titles and headings match design_spec.md precisely
   - Ensure navigation mappings (url_for calls) are correctly implemented
   - Validate dynamic IDs follow templating conventions matching patterns from design_spec.md

3. **Integration Checks**:
   - Confirm data flows between backend and frontend via context variables are consistent
   - Identify any mismatch between backend data provision and frontend data usage
   - Verify forms and buttons use correct methods and actions as per specification

CRITICAL REQUIREMENTS:
- Use validate_python_file and execute_python_code tools to perform thorough backend validation
- Use write_text_file tool to write validation_report.md with clear sections for syntax errors, runtime errors, UI issues, navigation inconsistencies, and data handling problems
- Output validation_report.md exactly as specified

Output: validation_report.md""",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "app_draft.py", "source": "BackendDeveloper"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "FrontendDeveloper"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "FinalIntegrator",
            "prompt": """You are a Software Engineer specializing in backend and frontend integration for Flask web applications.

Your goal is to implement all fixes and improvements identified in validation_report.md to produce final, fully conformant app.py and HTML templates that meet all specification requirements and pass all validation criteria.

Task Details:
- Read validation_report.md, app_draft.py, and all templates_draft/*.html along with design_spec.md and user_task_description
- Apply all fixes described in validation_report.md related to syntax, runtime, routing, navigation, UI elements, and data file handling
- Output final app.py and templates/*.html ensuring full compliance with design_spec.md functionality and UI element specifications
- Focus strictly on fixing issues detailed in validation_report.md without adding unrequested features or modifications

Implementation Guidelines:
1. **Backend Fixes**:
   - Correct all syntax and runtime errors in app_draft.py per report
   - Adjust Flask routes, data loading, and context variables as required for conformity
   - Ensure root route and all page routes operate as specified

2. **Frontend Fixes**:
   - Fix or add missing UI elements with exact IDs per design_spec.md
   - Correct page titles and headings to match specification
   - Fix navigation links/buttons using url_for with accurate route names and parameters
   - Ensure dynamic IDs in templates follow proper Jinja2 syntax and match specification patterns

3. **Testing and Verification**:
   - Validate fixes do not introduce new errors
   - Confirm consistency between backend context data and frontend usage
   - Prepare final deliverables with all fixes incorporated

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save final app.py and all templates/*.html files
- All fixes must strictly address issues from validation_report.md
- Resulting files must fully conform to design_spec.md and user_task_description
- Deliverables must be ready for final deployment and testing

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "Tester"},
                {"type": "text_file", "name": "app_draft.py", "source": "BackendDeveloper"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "FrontendDeveloper"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "Tester",
            "reviewer_agent": "FinalIntegrator",
            "review_criteria": "Verify that validation_report.md covers all needed fixes and that all issues are actionable and traceable to design_spec.md.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "source_agent": "FinalIntegrator",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm final app.py and templates/*.html fully implement design_spec.md and pass all key functional and UI requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Build the TravelPlanner Flask web application fully implementing the specified pages, data handling, and UI elements per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce design specification for TravelPlanner app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce complete design_spec.md covering pages, UI, navigation, and data."}
            ]
        },
        {
            "step": 2,
            "description": "Implement Flask backend and frontend templates based on design specifications.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce app_draft.py and templates_draft/*.html as draft implementation."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and finalize the TravelPlanner application ensuring correctness and compliance.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Produce final app.py and templates/*.html validated against requirements."}
            ]
        }
    ]
): pass
# Orchestrate_End