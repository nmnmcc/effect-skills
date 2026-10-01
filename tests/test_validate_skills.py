import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-skills.py"
spec = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / "effect-example"
        self.folder.mkdir()
        self.skill = self.folder / "SKILL.md"

    def test_spec_optional_yaml_fields_and_folded_description(self):
        self.skill.write_text("""---
name: effect-example
description: >-
  Use when validating a sample.
metadata:
  author: example
compatibility: Effect 4.0.0
---
Instructions.
[Pinned source](https://github.com/Effect-TS/effect/blob/effect%404.0.0/packages/effect/src/Effect.ts)
""", encoding="utf-8")
        self.assertEqual(validator.check_skill(self.skill), [])

    def test_duplicate_yaml_field_is_rejected(self):
        self.skill.write_text("""---
name: effect-example
name: different
description: Use when testing.
---
Instructions.
""", encoding="utf-8")
        self.assertIn("invalid YAML", " ".join(validator.check_skill(self.skill)))

    def test_unpublished_entrypoint_is_rejected(self):
        self.skill.write_text("""---
name: effect-example
description: Use when testing.
---
Import `effect/unstable/http` here.
""", encoding="utf-8")
        self.assertIn("not exported", " ".join(validator.check_skill(self.skill)))

    def test_renamed_entrypoint_is_rejected(self):
        self.skill.write_text("""---
name: effect-example
description: Use when testing.
---
Import `effect/httpapi` here.
""", encoding="utf-8")
        self.assertIn("not exported", " ".join(validator.check_skill(self.skill)))

    def test_missing_local_reference_is_rejected(self):
        self.skill.write_text("[missing](references/missing.md)\n", encoding="utf-8")
        self.assertIn("missing local reference", " ".join(validator.check_links(self.skill, set())))

    def test_missing_reference_style_link_is_rejected(self):
        self.skill.write_text("[missing][guide]\n\n[guide]: references/missing.md\n", encoding="utf-8")
        self.assertIn("missing local reference", " ".join(validator.check_links(self.skill, set())))


if __name__ == "__main__":
    unittest.main()
