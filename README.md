# TypeGen

Generate Python type stubs from JSON, YAML, YML and TOML for IDE autocomplete.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/github/license/grib-i/typegen?style=for-the-badge)](https://github.com/grib-i/typegen?tab=MIT-1-ov-file)
[![GitHub](https://img.shields.io/github/stars/grib-i/typegen?style=for-the-badge)](https://github.com/grib-i/typegen)

---

## Installation

### Linux

```bash
git clone https://github.com/grib-i/typegen
```

```bash
cd typegen
```

```bash
pipx install .
```

### Windows

```bash
git clone https://github.com/grib-i/typegen
```

```bash
cd typegen
```

```bash
pipx install .
```

### Requirements

- Python 3.10+
- pipx

Install pipx if needed:

```bash
python -m pip install --user pipx
pipx ensurepath
```

on linux distrs is recommended install pipx through package manager

---

## Usage

Initialize TypeGen in your project:

```bash
typegen init
```

Generate stubs using the project configuration:

```bash
typegen generate
```

Generate specific files:

```bash
typegen generate config.yaml tasks.toml
```

Generate using glob patterns:

```bash
typegen generate "*.yaml"
```

Override the output directory:

```bash
typegen generate -o .types
```

Override the package name:

```bash
typegen generate -p generated_types
```

Use a custom configuration file:

```bash
typegen generate -c myconfig.yaml
```

Generated:

```text
.typegen/
└── types/
    └── _typegen/
        ├── config.pyi
        └── tasks.pyi
```
