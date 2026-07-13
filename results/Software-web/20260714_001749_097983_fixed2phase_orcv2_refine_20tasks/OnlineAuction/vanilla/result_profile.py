# Phase1_Start
def design_specification_phase(
    goal: str = "Create and refine the full design specification for the OnlineAuction Python Flask web app including detailed page structure and data storage contract; deliver design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator drafts design_spec.md from user_task_description and design_feedback.md; DesignCritic reviews and writes design_feedback.md with [APPROVED] or NEED_MODIFY markers for refinement",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Architect specializing in Python Flask web application design specifications.

Your goal is to produce and iteratively refine a complete design specification document capturing page layouts, element IDs, navigation flow, and local text file data schemas for the OnlineAuction application.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- Initially create the full design_spec.md covering all required pages and data files
- On feedback beginning with NEED_MODIFY, apply all required corrections and rewrite the entire design_spec.md
- Stop refinement after at most two iterations or upon receiving [APPROVED] feedback
- Output the complete design_spec.md as a text file artifact

**Page Layout Specifications**
- Define each page with its title and overview
- Include container div IDs and all specified element IDs with their types and brief descriptions
- Specify navigation buttons and their target pages where applicable

**Data Storage Contract**
- Include all local text file data schemas with exact filenames
- Specify each file's data fields, formats, and provide example records
- Preserve data field names and formats as declared in user requirements

**Consistency and Scope**
- Reflect all pages and elements exactly as in user_task_description
- Do not add authentication or unrequested features
- Focus on enabling developers to implement the front-end, back-end routing, and data management from the specification

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to write design_spec.md artifact
- Run a maximum of two Generator/Critic iterations, stopping on [APPROVED]
- Accurately represent all page and data file specifications from user input
- Fully incorporate correction requests beginning with NEED_MODIFY without adding new requirements
- Do not write feedback status markers inside design_spec.md

Output: design_spec.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Software Design Reviewer specializing in Python Flask web application design review.

Your goal is to critically evaluate design_spec.md against user_task_description and provide gated feedback for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Verify completeness and accuracy of page layouts, element IDs, navigation flow
- Verify correctness and consistency of declared local data file schemas including field names and data formats
- Write feedback in design_feedback.md beginning exactly with [APPROVED] if fully compliant or NEED_MODIFY with clear, itemized corrections

Review Checklist:
1. Confirm design_spec.md includes all nine required pages with specified page titles and element IDs
2. Confirm navigation buttons and their target pages match user requirements on all pages
3. Validate data storage schemas for all declared text files, field names, data formats, and examples are consistent with user_task_description
4. Ensure no unrequested features like authentication or additional pages are introduced
5. Ensure naming conventions and element IDs are consistent across pages
6. Provide actionable feedback if issues found, else approve design_spec.md

CRITICAL REQUIREMENTS:
- Write the first bytes of design_feedback.md exactly as [APPROVED] or NEED_MODIFY
- No extra prefix, heading, or whitespace before the status marker
- Use write_text_file tool to output design_feedback.md

Output: design_feedback.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Ensure the design_spec.md fully covers all required pages, element IDs, navigation links, and data storage files per user requirements; provide constructive feedback to achieve final approval",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and iteratively refine the OnlineAuction Flask web app source code including app.py and templates/*.html with full functionality and correct element IDs; generate code_feedback.md with validation",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises app.py and templates/*.html using design_spec.md and code_feedback.md; CodeCritic evaluates functionality, correctness, completeness, element IDs, and data file integration then writes code_feedback.md starting with [APPROVED] or NEED_MODIFY",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specialized in building web applications with backend and frontend integration.

Your goal is to implement and iteratively refine the complete OnlineAuction Flask backend (app.py) and frontend templates (*.html) according to the design specifications and feedback for at most two iterations.

Task Details:
- Read design_spec.md, current app.py, templates/*.html, and code_feedback.md from CONTEXT
- On the first iteration, implement full app.py and templates/*.html based on design_spec.md
- On NEED_MODIFY feedback, apply all corrections and rewrite the entire app.py and templates/*.html accordingly
- On [APPROVED] feedback, preserve the approved implementation
- Output complete app.py and all templates/*.html files in the designated folders

**Section 1: Flask Backend Implementation**
- Implement Flask routes for all specified pages: Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status
- Integrate data loading and saving from local text files in the 'data' directory as specified (auctions.txt, categories.txt, bids.txt, winners.txt, bid_history.txt, items.txt, trending.txt)
- Ensure data consistency and correct file format handling for all operations (viewing, placing bids, filtering)
- Provide handlers for navigation and filtering as per design_spec.md

**Section 2: Frontend Templates (*.html)**
- Implement HTML templates with the exact required page titles and element IDs listed in the design specification
- Each template must contain the specified container elements, buttons, inputs, dropdowns, tables, and display areas exactly matching IDs (e.g., dashboard-page, featured-auctions, bids-table, place-bid-page, etc.)
- Bind frontend elements correctly with backend context data for dynamic content rendering
- Keep the UI navigation consistent with buttons leading to the corresponding Flask routes

**Section 3: Iterative Refinement and Feedback Usage**
- At feedback NEED_MODIFY, comprehensively identify and fix issues across backend and frontend code
- Validate all element IDs, navigation routes, and data file interactions per feedback
- Do not introduce extra functionalities beyond the design_spec.md and USER_TASK scope

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output completed app.py and templates/*.html files
- Maintain exact element IDs, page titles, and data file integration as specified
- Stop after two iterations or immediately upon receiving [APPROVED] feedback in code_feedback.md

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
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
            "prompt": """You are a Software Test Engineer with expertise in Python Flask application validation and front-end verification.

Your goal is to perform comprehensive review and validation of app.py and templates/*.html against design_spec.md, ensuring full compliance, correct element IDs, navigation, and data integration; provide feedback limited to [APPROVED] or NEED_MODIFY for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate completeness and correctness of all required Flask routes and backend functionality
- Verify all page titles, container elements, buttons, inputs, dropdowns, tables, and IDs exactly as specified in design_spec.md
- Check integration of all local text data files for correct access, parsing, and writing operations
- Ensure navigation flows correctly among all defined pages
- Write feedback in code_feedback.md starting exactly with [APPROVED] if fully compliant or NEED_MODIFY followed by detailed, actionable corrections

Validation Checklist:
1. Confirm all 9 pages (Dashboard, Auction Catalog, Auction Details, Place Bid, Bid History, Auction Categories, Winners, Trending Auctions, Auction Status) exist with correct Flask routes
2. Confirm every specified element ID is present in the related HTML template exactly as defined
3. Confirm all data file interactions respect specified formats and fields in the USER_TASK and design_spec.md
4. Confirm navigation buttons and links function correctly to corresponding routes
5. Identify missing or inconsistent features, broken IDs, or data handling errors clearly in feedback

CRITICAL REQUIREMENTS:
- Feedback artifact code_feedback.md MUST begin exactly with [APPROVED] or NEED_MODIFY on byte 1
- Use write_text_file tool to save complete feedback file
- Use validate_python_file tool to check app.py syntax and runtime, report errors
- Feedback must be precise, actionable, and strictly reference design_spec.md compliance

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
            "review_criteria": "Gate the conformity of app.py and templates/*.html to the design_spec.md and data storage schemes; verify that all required pages and element IDs exist and function correctly; ensure no regression or functionality gaps",
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
    goal: str = "Develop the OnlineAuction Python Flask web application conforming to detailed design and data requirements using at most two refinement iterations per phase",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine OnlineAuction design specification through generator and critic collaboration.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Generate and review the complete design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the OnlineAuction app backend and frontend with iterative feedback.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Build and refine the app.py and templates based on design spec and feedback."}
            ]
        }
    ]
): pass
# Orchestrate_End