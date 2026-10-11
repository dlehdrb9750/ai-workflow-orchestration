# Synthetic workflow example

Run from the root of this repository:

```bash
python examples/workflow_demo.py
python -m unittest discover -s tests -v
```

The mock objective is a public-data briefing. The example records a transient source error, processes an independent layout task, chooses a separately permitted data source, stores a JSON checkpoint, and resumes final report verification.

Nothing is downloaded, scheduled or written to an external service. The script requires Python 3.10+ and only the standard library.
