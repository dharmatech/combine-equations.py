
Video demo of the interactive equation editor:

https://youtu.be/O837G7cj5fE?si=wk4sURLNVGvgSIRq

## Install from github

```
uv pip install 'git+https://github.com/dharmatech/combine-equations.py'
```

## Install from cloned repository

```bash
git clone https://github.com/dharmatech/combine-equations.py.git
cd combine-equations.py
uv pip install -e .
```

Run examples:

```
python .\examples\eq-gui\demo_gui_features.py
python .\examples\up\ch4\up-example-4.7\up-example-4.7-000.py
```

## Testing

Install dev dependencies and run tests:

```bash
uv pip install -e ".[dev]"
uv run pytest
```
