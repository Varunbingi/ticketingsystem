Run the API locally
-------------------

This project includes a local virtual environment at `.venv/` inside the `backend/` folder.

Preferred, repeatable ways to run the app from the `backend/` directory:

1) Activate the venv then run uvicorn (recommended):

	source .venv/bin/activate
	uvicorn main:app --reload

2) Without activating, run directly with the venv python:

	./.venv/bin/python -m uvicorn main:app --reload

Notes
- If you see a warning like:
  `VIRTUAL_ENV=/Users/naveen/ticketingsystem/.venv does not match the project environment path ".venv" and will be ignored`
  it means your shell has a different VIRTUAL_ENV set (or points to a non-existent path). Fixes:

  - Deactivate the current environment (run `deactivate` if available) or unset the variable: `unset VIRTUAL_ENV`.
  - Activate the backend venv: `source .venv/bin/activate`.
  - Or run the venv's python directly as shown in (2).

Developer helper
- There's a tiny helper script `run.sh` you can use to start the app (see `backend/run.sh`).

