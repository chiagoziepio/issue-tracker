import os
from pathlib import Path
import subprocess
import sys
import unittest


class ModelImportTests(unittest.TestCase):
    def test_application_registers_all_models(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        environment = os.environ | {"PYTHONPATH": str(project_root / "src")}

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from sqlalchemy.orm import configure_mappers; "
                "import issue_tracker.main; configure_mappers()",
            ],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_models_can_be_imported_together(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        environment = os.environ | {"PYTHONPATH": str(project_root / "src")}

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import issue_tracker.model.user; import issue_tracker.model.issues_model",
            ],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
