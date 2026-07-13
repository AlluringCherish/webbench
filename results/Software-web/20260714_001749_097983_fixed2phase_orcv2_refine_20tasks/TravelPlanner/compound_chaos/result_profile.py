# Phase1_Start
def design_specification_phase(
    goal: str = "Create and refine the detailed design specification for the TravelPlanner web application, producing 'design_spec.md' and gated 'design_feedback.md'.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator drafts and revises the comprehensive design_spec.md including all pages, UI element IDs, data storage format, and user navigation flows. "
        "DesignCritic reviews design_spec.md for completeness, consistency, and adherence to requirements, producing design_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Architect specializing in Python web application design specifications.

Your goal is to develop and iteratively refine the complete design specification for the TravelPlanner web application, producing a full design_spec.md document.

Task Details:
- Read user_task_description from CONTEXT to understand overall requirements
- On first iteration, create comprehensive design_spec.md covering all pages, UI element IDs, local data storage formats, and navigation flows
- On feedback starting with NEED_MODIFY, apply all provided changes fully and overwrite design_spec.md
- When feedback starts with [APPROVED], preserve the approved design specification and stop iteration
- Read current design_spec.md and design_feedback.md from CONTEXT for iterative refinement
- Output the complete design_spec.md after each iteration using write_text_file

**Section 1: Page Specifications**
- Define each of the ten pages with title, overview, and container element IDs
- Specify all essential UI elements with exact IDs and types as per user requirements
- Include navigation flow and button linkage descriptions between pages

**Section 2: Data Storage Formats**
- Specify exact text file names and locations under a data directory
- For each data file, define format schema including field names, delimiters, and example rows
- Include all data described in user requirements: destinations, itineraries, hotels, flights, packages, trips, bookings

**Section 3: Consistency and Completeness**
- Ensure all UI elements and data fields exactly match requirements document
- Maintain uniform ID and naming conventions across page and data specs
- Avoid adding requirements not stated by user_task_description

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save the full design_spec.md file each iteration
- Limit to at most two iterations and cease on receiving [APPROVED] feedback
- Provide complete, clear, and consistent design specification for backend and frontend implementation
- Do not include feedback status marker inside design_spec.md

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "agent_name": "DesignCritic",
            "prompt": """You are a Design Reviewer specializing in Python web application design specifications for TravelPlanner.

Your goal is to evaluate the submitted design_spec.md for completeness, correctness, and adherence to the user requirements, providing gated feedback labeled [APPROVED] or NEED_MODIFY.

Task Details:
- Read user_task_description and the design_spec.md from CONTEXT
- Review that all ten pages are fully specified with correct titles, container IDs, and UI element IDs/types matching user requirements
- Verify that all required data files are specified with correct formats, field orders, delimiter, and representative examples
- Confirm that navigation flow and page linkage details are clearly described
- Check naming consistency of IDs, fields and data files
- Provide feedback beginning exactly with [APPROVED] when design_spec.md meets all criteria
- Provide feedback beginning exactly with NEED_MODIFY followed by detailed correction points if gaps or inconsistencies exist
- Write complete feedback using write_text_file

Review Requirements:
1. Completeness of each page’s specification with all listed UI elements and IDs
2. Accuracy and completeness of each data file format and example content
3. Consistency of naming conventions and adherence to user specifications
4. No introduction of new features or departures from the user requirements document

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md must be exactly [APPROVED] or NEED_MODIFY
- No preceding whitespace, headings, or extraneous characters before marker
- Use write_text_file tool to save the complete feedback
- Limit to at most two review iterations and stop immediately upon [APPROVED]

Output: design_feedback.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Verify completeness of page designs, all element IDs, data formats, and ensure no missing features per user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Iteratively develop and refine the TravelPlanner Python Flask web application including app.py and templates/*.html, producing code feedback for gating.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes and revises the Flask app.py and HTML templates based on design_spec.md and code_feedback.md. "
        "CodeCritic reviews the implementation for functional correctness, alignment with design, route conformance, element IDs, and performance, producing code_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specializing in full-stack web application development with local file data management.

Your goal is to implement and iteratively refine the complete TravelPlanner Flask application, including app.py and HTML templates, guided by the design specification and critic feedback.

Task Details:
- Read design_spec.md and previous app.py, templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, create complete app.py and all templates/*.html according to design_spec.md
- On subsequent iterations where code_feedback.md begins with NEED_MODIFY, apply every suggested modification and rewrite the full app.py and templates/*.html
- When code_feedback.md begins with [APPROVED], preserve the approved implementation unchanged

**Section 1: Flask Application Implementation**
- Implement all routes corresponding to pages specified in design_spec.md with correct route paths and HTTP methods
- Implement handlers that read and write data using local text files as described in design_spec.md
- Ensure all element IDs in templates correspond exactly to specification for front-end integration
- Provide navigation links enabling user flow starting at the Dashboard page

**Section 2: HTML Templates Implementation**
- Create templates for all pages described in design_spec.md with fully specified page structure and elements
- Include all specified element IDs for buttons, inputs, div containers, tables, etc.
- Templates must be valid HTML with Flask Jinja2 syntax as needed for dynamic content insertion

**Section 3: Integration and Data Handling**
- Manage data inputs and outputs to/from local text files exactly as per design_spec.md field definitions and formats
- Implement data conversions and date handling as required for itinerary and bookings
- Maintain consistency between route logic and template data context

CRITICAL REQUIREMENTS:
- Run at most two iterations of generation and review
- Always write complete and updated app.py and templates/*.html files on modification requests
- Use the write_text_file tool to output updated app.py and template files
- Focus implementation strictly on specified input/output artifacts from design_spec.md and feedback files

Output: app.py and templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
                {"type": "text_file", "name": "code_feedback.md", "source": "CodeCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "CodeCritic",
            "prompt": """You are a Software Test Engineer and Code Reviewer specialized in Python Flask applications with local text file data storage.

Your goal is to review the implementation of app.py and templates/*.html against design_spec.md and provide gated feedback to ensure functional correctness and specification compliance.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate app.py syntax and runtime correctness using validate_python_file tool
- Check routes implemented match design_spec.md with correct URLs and HTTP methods
- Verify presence and correctness of all specified element IDs in HTML templates
- Confirm compliance with all design_spec.md requirements for data handling, page flow, and UI elements
- Produce code_feedback.md beginning with exactly [APPROVED] if implementation is complete and correct, otherwise NEED_MODIFY followed by detailed correction instructions

Review Criteria:
1. All required pages and routes are implemented and accessible starting from the Dashboard
2. All specified element IDs appear exactly and functionally in templates
3. Data input/output follows the specified local text file formats and field structures
4. app.py has no syntax or runtime errors as validated by the tool
5. Adherence to design_spec.md with no missing features or deviations

CRITICAL REQUIREMENTS:
- Feedback must start with the exact prefixes [APPROVED] or NEED_MODIFY in code_feedback.md
- Use write_text_file to write the feedback file atomically
- Use validate_python_file tool to verify app.py correctness
- Run at most two critique iterations and stop upon receiving [APPROVED]

Output: code_feedback.md""",
            "tools": ["write_text_file", "validate_python_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "code_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Ensure all required pages, routes, element IDs, local text file data handling, and design conformance are correctly implemented and error-free.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the TravelPlanner Python Flask web application with complete page implementations and data handling as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Iterative creation and refinement of the detailed design specification for the TravelPlanner app.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce a comprehensive design contract capturing all pages, UI elements, and data formats."
                }
            ]
        },
        {
            "step": 2,
            "description": "Iterative implementation and verification of the TravelPlanner Flask app code including templates, following the approved design spec.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Develop and refine the complete app.py and HTML templates with correctness and adherence to design."
                }
            ]
        }
    ]
): pass
# Orchestrate_End