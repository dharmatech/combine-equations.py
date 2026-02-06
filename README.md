
# Introduction

This is a set of experimental Python modules for solving equations in Sympy.

## `display_equations_`

`display_equations_` shows
 - known values in green 🟢
 - wanted value in red 🔴
 - unknown values in default color

<img width="500" alt="image" src="https://github.com/user-attachments/assets/91e6a073-4d32-41db-b7b3-7ed11ad511c6" />

## Interactive equation solver

```
python .\examples\eq-gui\demo_gui_features.py
```

<img width="800" alt="image" src="https://github.com/user-attachments/assets/d7009494-f8b6-4fbf-a51e-50f52e30f2e2" />

Video demo of the interactive equation editor:

https://youtu.be/O837G7cj5fE?si=wk4sURLNVGvgSIRq

## Interactive equation solver for JupyterLite Notebooks

<img alt="image" src="https://github.com/user-attachments/assets/2a56090d-5e0a-4c09-a80c-72c520e9db6d" />

Video demo:

https://youtu.be/7ysUdxTfKhU?si=KQiYmqjUhq6nNjXn

Notebook used in the demo available here:

https://github.com/dharmatech/github-pages-test

You can try out the interactive equation solver without installing anything as it runs in a browser.

## Examples

Examples from the textbook University Physics are here: [examples/up](examples/up).

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
