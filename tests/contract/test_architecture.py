import ast
import hashlib
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_canonical_app_preserves_openapi_contract() -> None:
    app = importlib.import_module("skillmatch.main").app
    digest = hashlib.sha256(
        json.dumps(app.openapi(), sort_keys=True).encode()
    ).hexdigest()
    assert digest == "b1a7a06babfbd06715844d2f3e5f8527ab2d6869c29783575a420277e76ced92"


def test_matching_has_no_http_database_or_orchestration_imports() -> None:
    package = ROOT / "backend/src/skillmatch/features/matching"
    assert package.is_dir()
    allowed = {"typing", "pydantic", "skillmatch.features.matching"}
    for path in package.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                assert node.level == 0, path
                modules = [node.module or ""]
            for module in modules:
                assert any(
                    module == name or module.startswith(name + ".")
                    for name in allowed
                ), (path, module)


def test_legacy_source_and_scaffold_are_removed() -> None:
    assert not (ROOT / "app").exists()
    assert not list((ROOT / "backend").glob("*.py"))
    for name in ("api", "domain", "repositories", "matching", "tests"):
        assert not list((ROOT / "backend" / name).rglob("*.py"))


def test_canonical_sources_have_one_app_and_no_legacy_imports() -> None:
    app_locations = []
    for path in (ROOT / "backend/src/skillmatch").rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "FastAPI":
                    app_locations.append(path.relative_to(ROOT).as_posix())
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            else:
                continue
            assert all(module.split(".")[0] not in {
                       "app", "backend"} for module in modules), path
    assert app_locations == ["backend/src/skillmatch/main.py"]


def test_entrypoint_and_error_module_have_no_duplicate_definitions() -> None:
    for relative_path in ('main.py', 'core/errors.py'):
        path = ROOT / 'backend/src/skillmatch' / relative_path
        names = [node.name for node in ast.parse(path.read_text()).body
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        assert len(names) == len(set(names)), (path, names)


def test_canonical_app_registers_both_auth_and_http_problem_handlers() -> None:
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException
    from skillmatch.core.errors import (
        ProblemError, http_error_handler, problem_handler, validation_handler,
    )
    app = importlib.import_module('skillmatch.main').app
    assert app.exception_handlers[ProblemError] is problem_handler
    assert app.exception_handlers[HTTPException] is http_error_handler
    assert app.exception_handlers[RequestValidationError] is validation_handler
