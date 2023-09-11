from functools import lru_cache
from pathlib import Path


@lru_cache()
def get_python_project_root_dir() -> Path:
    path = Path().cwd()
    while Path(path, "__init__.py").exists():
        path = path.parent
    return path
