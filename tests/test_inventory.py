import unittest
from inventory_check import inspect


def component():
    return dict(
        name="example",
        version="0.1",
        kind="code",
        source_url="recorded-source",
        license_expression="MIT",
        license_text_url="recorded-license",
        intended_use="internal prototype",
        review={"status": "pending"},
    )


class InventoryTests(unittest.TestCase):
    def test_empty_and_malformed_inventory_rejected(self):
        for manifest in [
            [],
            {"components": []},
            {"components": [dict(component(), review="yes")]},
        ]:
            with self.subTest(manifest=manifest), self.assertRaises(ValueError):
                inspect(manifest)

    def test_complete_is_not_permission(self):
        r = inspect({"components": [component()]})
        self.assertEqual(r["complete_records"], 1)
        self.assertFalse(r["commercial_permission_determined"])
        self.assertEqual(r["pending_reviews"], 1)

    def test_missing_license_stays_missing(self):
        c = component()
        c["license_expression"] = ""
        self.assertIn(
            "license_expression",
            inspect({"components": [c]})["components"][0]["missing"],
        )

    def test_review_must_be_identified_and_dated(self):
        c = component()
        c["review"] = {"status": "reviewed"}
        self.assertFalse(
            inspect({"components": [c]})["components"][0]["metadata_complete"]
        )

    def test_duplicate_identity(self):
        c = component()
        self.assertIn(
            "duplicate component identity",
            inspect({"components": [c, c]})["components"][1]["missing"],
        )


if __name__ == "__main__":
    unittest.main()
