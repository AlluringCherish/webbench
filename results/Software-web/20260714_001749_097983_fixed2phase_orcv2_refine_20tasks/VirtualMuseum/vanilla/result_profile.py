# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the complete design specification and UI contract for the VirtualMuseum Python web application including all pages, element IDs, navigation flows, and data storage, producing design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator produces design_spec.md detailing all required pages (Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides), UI elements with IDs, navigation button mappings, and data file formats; "
        "DesignCritic reviews design_spec.md for completeness, clarity, and consistency writing design_feedback.md starting with [APPROVED] or NEED_MODIFY for revision; "
        "This refinement loop runs at most two iterations."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Architect specializing in Python web application design specifications.

Your goal is to author and refine a comprehensive design specification document for the VirtualMuseum web application, including page layouts, exact UI element IDs, navigation schemes, and local data file formats, iterating at most twice based on critic feedback.

Task Details:
- Read the user_task_description from CONTEXT to understand all functional requirements.
- Read existing design_spec.md and design_feedback.md artifacts for incremental refinement.
- Output a complete design_spec.md detailing all seven required pages, UI element IDs, navigation button mappings, and file format data structures.
- On iteration two, apply all NEED_MODIFY feedback by rewriting the entire design_spec.md. On approval, preserve current design_spec.md.

**Section 1: Page Layouts and Element IDs**
- Specify each page (Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides).
- Include all UI elements with their exact type and unique element IDs as provided.
- Provide container element IDs and detailed description of key UI components.

**Section 2: Navigation Mapping**
- Define navigation button IDs on each page and their destination pages.
- Ensure navigation paths start from Dashboard as the main hub.
- Maintain consistency of button IDs and their target pages per User Task description.

**Section 3: Data Storage Formats**
- Specify all data files within the 'data' directory with exact filenames.
- Define file formats (pipe-separated) and full schemas for each data type (users, galleries, exhibitions, artifacts, audioguides, tickets, events, event registrations, collection logs).
- Provide example records as specified without inventing data fields.

CRITICAL SUCCESS CRITERIA:
- Follow the Refinement Loop with at most two iterations, rewriting design_spec.md completely on NEED_MODIFY feedback.
- Ensure clarity, completeness, and strict adherence to user_task_description.
- Use write_text_file tool to save the design_spec.md file.
- Output exactly as design_spec.md.""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}],
        },
        {
            "agent_name": "DesignCritic",
            "prompt": """You are a Software Design Reviewer specializing in Python web application design specification validation.

Your goal is to review the design_spec.md document for completeness, clarity, alignment with the VirtualMuseum requirements, and consistency; produce gated feedback in design_feedback.md starting with [APPROVED] or NEED_MODIFY to guide refinement, running at most two iterations.

Task Details:
- Read user_task_description and the current design_spec.md from CONTEXT.
- Verify all seven required pages and their UI element IDs are specified completely.
- Verify navigation button mappings accurately connect the pages as described.
- Check data file formats, table schemas, pipe-delimited fields, and example records strictly follow the requirements.
- Identify missing, inconsistent, or unclear elements and provide detailed NEED_MODIFY feedback.
- Write [APPROVED] if the specification fully meets the requirements with no missing or inconsistent information.

Review Requirements:
1. Confirm page container IDs and all element IDs match those declared in the user task.
2. Validate navigation button IDs and their correct target page mappings.
3. Confirm all data files with exact names, their pipe-separated field schemas, and example content are fully documented.
4. Ensure consistency and no undocumented features beyond user requirements.

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY followed immediately by clear corrections.
- Use write_text_file tool to save design_feedback.md.
- Stop after at most two review iterations or immediately upon approval.
- Provide feedback only within the defined context and scope.

Output: design_feedback.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_feedback.md"}],
        },
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Check for completeness of all pages, element IDs, navigation accuracy, adherence to data format specifications, and clarity of design_spec.md; ensure no requirements are omitted or inconsistent.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}],
        }
    ],
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and refine the full backend and frontend implementation of VirtualMuseum Python web app including app.py and templates/*.html from design_spec.md and address code_feedback.md to final approved quality",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes or revises app.py and templates/*.html implementing all specified pages, elements, navigation, data loading/saving from local text files in 'data' directory as defined in design_spec.md; "
        "CodeCritic reviews code bundle for functional completeness, conformance to design_spec.md, syntax, runtime validation, and UI correctness producing code_feedback.md starting with [APPROVED] or NEED_MODIFY; "
        "The refinement loop runs at most two iterations."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Full Stack Developer specializing in Python web applications with expertise in integrating backend logic and frontend UI using local text files for data persistence.

Your goal is to implement or revise the complete app.py backend and HTML templates under templates/*.html for the VirtualMuseum platform, ensuring compliance with design_spec.md and addressing all feedback in code_feedback.md within at most two iterations.

Task Details:
- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT
- On first iteration, implement complete app.py and HTML templates covering all specified pages, UI elements with exact IDs, navigation, and local text file data handling under 'data' directory
- On feedback starting with NEED_MODIFY, apply all corrections fully and overwrite both app.py and templates/*.html
- On feedback starting with [APPROVED], preserve the approved implementation without changes

**Implementation Requirements: Backend**
- Implement Python backend in app.py managing all routes, data loading/saving from local text files as specified in design_spec.md
- Provide complete data persistence using local text files with pipe-delimited formats in the 'data' directory
- Include all business logic for exhibitions, artifacts, audio guides, tickets, events, and registrations
- Ensure route handlers match design_spec.md page names and support the required UI interactions

**Implementation Requirements: Frontend**
- Develop HTML templates for all seven pages named and structured as per design_spec.md requirements under templates/*.html
- Use exact element IDs for all UI components listed (e.g., dashboard-page, exhibition-summary, artifact-catalog-button, etc.)
- Implement navigation buttons and filters exactly as specified
- Embed dynamic content bindings consistent with backend context variables

**Quality and Testing**
- Use validate_python_file tool to check syntax and runtime for app.py after generation
- Use write_text_file tool to save app.py and all templates/*.html after edits
- Focus on correctness of all UI elements, exact navigation paths, proper data file reads/writes, and adherence to all design contracts

CRITICAL SUCCESS CRITERIA:
- Produce complete, consistent app.py and templates/*.html implementing all design features
- Apply all NEED_MODIFY feedback fully within at most two iterations
- Use write_text_file tool to save all output files
- Use validate_python_file tool to validate app.py correctness before saving

Output: app.py, templates/*.html""",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Software Test Engineer specialized in Python web applications and frontend UI review, focusing on verifying backend logic, data handling, UI correctness, and code validity.

Your goal is to review app.py and templates/*.html for correctness, complete adherence to design_spec.md, correct local text file data operations, and successful syntax and runtime validation; then produce code_feedback.md starting with [APPROVED] or NEED_MODIFY within at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify all required pages, UI elements, and navigation exactly match design_spec.md
- Check all element IDs exist and are correctly implemented in frontend templates
- Confirm backend routes and logic implement all features specified including data persistence with pipe-delimited local text files in 'data' directory
- Validate app.py syntax and runtime using validate_python_file tool
- Write code_feedback.md starting exactly with [APPROVED] if all criteria met or NEED_MODIFY followed by detailed correction instructions
- Stop refinement loop upon first [APPROVED] feedback or after two iterations

Review Requirements:
1. Confirm all seven pages exist with all specified UI elements and IDs as per design_spec.md
2. Verify navigation buttons correctly link pages as stated
3. Verify backend reads/writes all local text data files correctly with the defined formats and fields
4. Validate app.py syntax and runtime pass with no errors
5. Check UI correctness and backend logic completeness

CRITICAL REQUIREMENTS:
- code_feedback.md MUST start with exactly [APPROVED] or NEED_MODIFY on byte 1
- Use write_text_file tool to save full feedback text
- Provide clear, actionable corrections on NEED_MODIFY

Output: code_feedback.md""",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Verify code conformance to design_spec.md, correctness of data file interactions, completeness of all pages and UI elements with specified IDs, and successful syntax/runtime validation.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the complete Python VirtualMuseum web application with dashboard start page, seven defined pages, exact element IDs, local text file data storage, and robust functionality as specified",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the full design specification and UI contract for VirtualMuseum including pages, elements, navigation, and data formats.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Adaptive design refinement and contract specification for VirtualMuseum web app.",
                }
            ],
        },
        {
            "step": 2,
            "description": "Develop and refine implementation including app.py and templates/*.html from design_spec.md until approved.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Adaptive backend and frontend implementation refinement for VirtualMuseum.",
                }
            ],
        },
    ],
): pass
# Orchestrate_End