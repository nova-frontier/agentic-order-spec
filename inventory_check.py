"""Inventory license provenance and review completeness; no legal eligibility verdict."""
import argparse, json, datetime

FIELDS = [
    "name",
    "version",
    "kind",
    "source_url",
    "license_expression",
    "license_text_url",
    "intended_use",
]


def inspect(manifest):
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be an object")
    rows = []
    components = manifest.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("components must be a nonempty list")
    seen = set()
    for c in components:
        if not isinstance(c, dict):
            raise ValueError("component must be an object")
        missing = [
            f for f in FIELDS if not isinstance(c.get(f), str) or not c[f].strip()
        ]
        key = tuple(
            c.get(f) if isinstance(c.get(f), str) else None
            for f in ["name", "version", "kind"]
        )
        if key in seen:
            missing.append("duplicate component identity")
        seen.add(key)
        review = c.get("review")
        if review is None:
            review = {}
        if not isinstance(review, dict):
            raise ValueError("review must be an object")
        status = review.get("status", "pending")
        if status not in ["pending", "reviewed"]:
            missing.append("invalid review status")
        if status == "reviewed":
            for f in ["reviewer", "reviewed_at", "notes"]:
                if not isinstance(review.get(f), str) or not review[f].strip():
                    missing.append("review." + f)
            try:
                datetime.date.fromisoformat(review.get("reviewed_at", ""))
            except (TypeError, ValueError):
                missing.append("review.reviewed_at must be ISO date")
        rows.append(
            {
                "name": c.get("name"),
                "version": c.get("version"),
                "review_status": status,
                "metadata_complete": not missing,
                "missing": missing,
            }
        )
    return {
        "components": rows,
        "complete_records": sum(r["metadata_complete"] for r in rows),
        "pending_reviews": sum(r["review_status"] != "reviewed" for r in rows),
        "commercial_permission_determined": False,
        "scope": "Metadata completeness is not a permission, compatibility, regulatory or legal determination.",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest")
    p.add_argument("--strict", action="store_true")
    a = p.parse_args()
    try:
        with open(a.manifest, encoding="utf-8-sig") as f:
            r = inspect(json.load(f))
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return (
            1
            if a.strict
            and any(
                not c["metadata_complete"] or c["review_status"] != "reviewed"
                for c in r["components"]
            )
            else 0
        )
    except ValueError as e:
        p.error(str(e))


if __name__ == "__main__":
    raise SystemExit(main())
