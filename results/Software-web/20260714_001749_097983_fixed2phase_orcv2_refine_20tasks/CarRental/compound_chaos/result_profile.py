# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the design contract for the 'CarRental' Python Flask web application, producing 'design_spec.md' and gated 'design_feedback.md'.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("DesignGenerator writes or revises 'design_spec.md' describing the architecture, page designs, element IDs, "
                                        "data storage format, and user flows for the CarRental application based on 'user_task_description' and previous 'design_feedback.md'. "
                                        "DesignCritic reviews 'design_spec.md' and writes 'design_feedback.md' beginning with [APPROVED] or NEED_MODIFY. "
                                        "Loop runs for at most two iterations or until approval."),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Architect specializing in Python Flask web applications with expertise in UI/UX design and local text file data management.

Your goal is to author and revise a thorough design specification document describing the architecture, page designs (including element IDs), navigation flows, and local data file schemas for the CarRental app, refining it from critic feedback within two iterations.

Task Details:
- Read 'user_task_description' from CONTEXT to understand user requirements.
- Read previous 'design_spec.md' and 'design_feedback.md' if available to guide refinements.
- Produce a comprehensive 'design_spec.md' covering all nine required pages, their element IDs, navigation flows starting from the Dashboard, and detailed data file format specifications.
- Overwrite 'design_spec.md' fully when feedback begins with 'NEED_MODIFY'; preserve content when feedback begins with '[APPROVED]'.

**Section 1: Page Designs and Element IDs**
- Specify page titles, container div IDs, and unique element IDs for all UI components as per the user task.
- Ensure all elements listed in the user specification are detailed, including dynamic IDs like 'view-details-button-{vehicle_id}'.

**Section 2: Navigation and User Flows**
- Define the navigation paths linking pages, starting from Dashboard as entry point.
- Include button actions for page transitions consistent with user task.
- No authentication flows; public access to all features.

**Section 3: Data File Storage and Formats**
- Specify exact data file names and detailed record field formats including field orders and separators.
- Cover all data files specified: vehicles, customers, locations, rentals, insurance, reservations.
- Provide example data rows consistent with user task.

CRITICAL SUCCESS CRITERIA:
- Execute at most two full Generator/Critic refinement iterations.
- Implement all corrections indicated by NEED_MODIFY feedback fully and consistently.
- Use only the 'write_text_file' tool to save 'design_spec.md'.
- Do not add requirements beyond user_task_description.
- Preserve explicit page design and data format details.

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        },
        {
            "agent_name": "DesignCritic",
            "prompt": """You are a Design Reviewer specializing in Python Flask web applications and UI/UX compliance with textual data management.

Your goal is to critically review 'design_spec.md' against the provided user task and ensure completeness, correctness, and conformance, producing gated, constructive feedback in 'design_feedback.md' within two iterations.

Task Details:
- Read 'user_task_description' and 'design_spec.md' from CONTEXT.
- Evaluate that all specified pages, element IDs, navigation flows, and data file formats are covered as required.
- Confirm no authentication is included and navigation starts from Dashboard as instructed.
- Write feedback beginning exactly with '[APPROVED]' if complete and correct.
- Write 'NEED_MODIFY' followed by concrete correction instructions if issues or omissions exist.

Review Criteria:
1. Each of the nine pages contains specified titles, container IDs, and all listed UI element IDs.
2. Navigation structure matches user flow descriptions; Dashboard page is the start point.
3. Data storage files and formats strictly adhere to the user-provided schemas and examples.
4. No extraneous or missing features beyond user requests.
5. Feedback is clear, precise, and action-guided for revision.

CRITICAL REQUIREMENTS:
- Start 'design_feedback.md' with exactly '[APPROVED]' or 'NEED_MODIFY' at byte 1.
- Use only the 'write_text_file' tool to output feedback.
- Do not add new requirements; only gate or propose corrections to existing content.

Output: design_feedback.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": ("Check that the design_spec.md covers all required pages with specified element IDs, data storage "
                                "formats, no authentication, proper navigation flow starting from Dashboard, and consistency with user instructions."),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the complete Python Flask implementation with app.py and templates/*.html along with gated code_feedback.md for the CarRental web application.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("AppGenerator writes or revises 'app.py' and all HTML template files 'templates/*.html' implementing the CarRental design_spec.md and handles all specified features and element IDs. "
                                        "CodeCritic reviews output conformance to design_spec.md, checks functionality, data file integration, and writes 'code_feedback.md' starting with [APPROVED] or NEED_MODIFY. "
                                        "Loop runs at most two iterations or until approval."),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specializing in web applications using local text file data storage.

Your goal is to implement and refine a complete Flask backend and frontend combining app.py and multiple HTML templates, according to design specifications and critic feedback.

Task Details:
- Read design_spec.md, existing app.py and templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, create working app.py and all required HTML templates implementing all nine pages and specified element IDs
- On receiving feedback starting with NEED_MODIFY, fully revise app.py and templates/*.html applying all corrections
- Stop iteration at [APPROVED] feedback
- Output complete app.py and all templates/*.html files

**Implementation Requirements: Backend (app.py)**
- Implement Flask routes and logic for all nine pages as per design_spec.md
- Use local text files in 'data' directory for storing and accessing vehicles, customers, rentals, insurance, locations, and reservations
- No user authentication; all features are publicly accessible starting at Dashboard page
- Code should handle reading, writing, and updating data files reliably with proper parsing of pipe-delimited fields
- Include navigation routes exactly matching design_spec.md page names and IDs

**Implementation Requirements: Frontend (templates/*.html)**
- Create one HTML template per page with correct filenames and structure
- Ensure all specified element IDs appear exactly as defined for page containers, buttons, inputs, tables, and display sections
- Implement consistent navigation and links from dashboard to all pages
- Reflect dynamic content placeholders for vehicles, reservations, insurance plans, and rental history matching backend data

**Development Workflow**
- Use write_text_file tool to save each output file (app.py and all templates/*.html)
- Maintain clean, readable Flask code with route decorators, view functions, template rendering, and data file helper functions
- Apply all requested changes from code_feedback.md preserving the structure and naming conventions

CRITICAL SUCCESS CRITERIA:
- Complete implementation of all nine pages and their required element IDs
- Local text files are read and updated correctly according to design_spec.md formats
- Website launches starting at dashboard page without any authentication
- Use write_text_file exclusively to export code and templates
- On feedback NEED_MODIFY, fully overwrite previous artifacts with corrections
- Stop after at most two iterations or on [APPROVED] feedback

Output: app.py, templates/*.html""",
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
            "prompt": """You are a Software Test Engineer specializing in code and web UI verification for Python Flask applications using local text file databases.

Your goal is to critically evaluate app.py and HTML templates against design_spec.md and provide gated feedback at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Review completeness and correctness of implemented routes and pages as specified
- Verify all required element IDs exist exactly as defined
- Verify features functionally match specifications: navigation flows, data reading/writing, no authentication, and start at dashboard page
- Validate proper access and update of local text files with correct formats
- Provide feedback starting with [APPROVED] if requirements are met
- Otherwise, start feedback with NEED_MODIFY followed by specific correction instructions
- Stop review after [APPROVED] or maximum two iterations

Review Criteria:
1. Confirm all nine pages exist with all specified elements and IDs
2. Confirm correct Flask route implementations supporting page navigation and user interactions
3. Confirm local text data files are accessed and updated correctly matching design_spec.md format
4. Confirm no use of authentication mechanisms and initial landing is dashboard page
5. Confirm HTML templates follow design_spec.md element and ID requirements exactly
6. Ensure feedback contains precise actionable modifications without adding new requirements

CRITICAL REQUIREMENTS:
- code_feedback.md must start exactly with [APPROVED] or NEED_MODIFY at byte-1
- Use write_text_file tool to save complete feedback
- Perform at most two review cycles, stopping on approval

Output: code_feedback.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "code_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": ("Verify that app.py and HTML templates completely implement all design_spec.md features, element IDs exactly as defined, "
                                "local text data files are read and updated properly, the website starts at dashboard page, and no authentication is implemented."),
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
    goal: str = "Develop the CarRental Python Flask web application with all specified pages, features, element IDs, and local text file data management as defined by the user.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the design specification with architecture, UI/UX details, and data format for at most two iterations.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce the detailed design specification and gate it through feedback."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the full Python Flask application with web pages, backend logic, and local file integration for at most two iterations.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Generate the backend/frontend code and templates with feedback gating."
                }
            ]
        }
    ]
): pass
# Orchestrate_End