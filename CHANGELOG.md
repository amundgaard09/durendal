# DURENDAL CHANGELOG 2026

### Sunday - 07.06.2026

- Fixed circular import bugs in Vanguard - result of UniCLI importing straight from DuraPy instead of absolute import
- Fixed general upimporting bugs in DuraPy
- Fixed paths in Vanguard (AmundWorks -> Durendal)
- Removed unneccesary console messages in the MDC Pipeline / Pagefinder script
- Added Matrix struct in DuraC
- Added ROADMAP, NOTES & CHANGELOG Markdown files
- Added `execution_engine.py` and `intent_engine` to the `engines` directory for Icarus

### Monday - 08.06.2026

- Added a Vosk speech model. Vosk will serve as an offline fallback for STT. Whisper will serve as the main STT, when ICARUS is ran online.
- Added `Icarus/core/__init__.py` complete with doc-string.
- Added `entrypoint.py` as the main entrypoint for ICARUS.
- Added functional STT and TTS capabilities for ICARUS. (`communicative_engine_rev3`). Icarus can now hear and speak. 
- Added a simple `process()` function for processing the input text from the `communicative_engine`. This serves as a placeholder for future integration with the two other engines.
- Added `Icarus/skills` for SKILL.md files. Still need to figure out the architechture behind it.
- Added placeholder skills for future development (`calendar_lookup`, `web_search`)
- Added `skill_template.md`. It describes the structure of the skill folders for the intent/execution engines.
- Added individual GitHub projects for each Durendal project, instead of the DuraPy project serving as the singular project for the entirety of Durendal.
- Added XO Rev. IV. This will be optimalized to serve as the FFN/MLP as part of XO Rev. V, which will be a fully featured LLM, as part of the ICARUS complex.
- Added `Icarus`/`README.md`
- Added many new issues/TODOs in the ICARUS GitHub project.
- Changed (derivative) activation functions in UniCogni to take np/cp (xp) `ndarray`s instead of floats.
- Closed a lot of issues in all github projects.
- Made the `Article` class a dataclass.
- Started work on the MCP system for ICARUS.
- Made a `MCPTool` dataclass.
- Added functions for retriveing skills from the skills directory. Not complete yet, though.

### Tuesday - 09.06.2026

- Added `mcp_tool.py`, `input_schema.py` and `mcp_property.py`, all of which are dataclasses. 
- Added `mcp_server_kernel.py`.
- Added `Icarus`/`README.MD`.
- Added capabilities for exiting ICARUS by speech.
- Added capabilities for speaking to ICARUS indefinetly by adding a while-loop.
- Added `timeskill.py`, the first skill. It does not yet follow the standard skill template, but will be refactored.
- Added `pyproject.toml`, and plans to add a ICARUS startup script & CLI command.
