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
    assert digest == "0717b5e90311f1fe407aa8fc06db231630dac44c969c4428afe2cf0097cbf4bd"


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
    assert not list((ROOT / "app").glob("*.py"))
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
            assert all(module.split(".")[0] not in {"app", "backend"} for module in modules), path
    assert app_locations == ["backend/src/skillmatch/main.py"]
