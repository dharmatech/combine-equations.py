
`display_equations_` shows
 - known values in green 🟢
 - wanted value in red 🔴
 - unknown values in default color

<img width="874" height="357" alt="image" src="https://github.com/user-attachments/assets/91e6a073-4d32-41db-b7b3-7ed11ad511c6" />

Interactive equation editor:

<img width="1752" height="878" alt="image" src="https://github.com/user-attachments/assets/d7009494-f8b6-4fbf-a51e-50f52e30f2e2" />

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
