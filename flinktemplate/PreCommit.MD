## Pre-commit Config

**This repository is associated with
a [blog post](https://www.laac.dev/blog/automating-convention-linting-formatting-python/)
about linting and formatting Python code. For a repo with more up-to-date configuration files
see [here](https://github.com/laactech/pre-commit-config-latest)**
or [here](https://sourcery.ai/blog/python-best-practices/)
and [this](https://www.laac.dev/blog/automating-convention-linting-formatting-python/)

[pre-commit](https://pre-commit.com/) is used to install four Python code linting and formatting
tools:

* [flake8](http://flake8.pycqa.org/en/latest/) a Python style guide linter
* [bandit](https://github.com/PyCQA/bandit) a Python security vulnerability linter
* [black](https://black.readthedocs.io/en/stable/) a Python automatic code formatter
* [isort](https://github.com/timothycrosley/isort) a Python automatic import formatter
* [mypy](https://github.com/python/mypy) an optional type checker for Python
* [seed-isort-config](https://github.com/asottile/seed-isort-config) a tool to statically
  populate the "known_third_party" part of the `.isort.cfg`

### Getting started

**Requires `python >=3.6`, `pre-commit>=1.14` and a `git` repository**

1. `git add` the previous files to your git repository
1. Run `pip install pre-commit`
1. Add pre-commit to your project's requirements
1. Run `pre-commit install` and `pre-commit install --install-hooks`
1. `git commit` the new configuration files
1. Run `pre-commit run -a` to lint and format your entire project
1. `git add` and `git commit` the formatting and linting changes once you've resolved any issues

Now on every commit, `pre-commit` will use a git hook to run the tools.
**Warning: the first commit will take some time because the tools are being installed by
`pre-commit`**

### Resolving failed commits

* If `black` or `isort` fail, they have reformatted your code. `git add` and `git commit`
  the changes.
* If `flake8`, `bandit`, or `mypy` fail, they will output a complaint and where that complaint
  exists. Fix the code that they complain about and `git add` and `git commit` the changes.

### How to bypass pre-commit hooks

At certain points, you may wish to do a git commit and bypassing checks performed by pre-commit hooks. This can be done
by providing --no-verify option:

```bash
git commit -m "Bypassing pre-commit hooks" --no-verify
```
