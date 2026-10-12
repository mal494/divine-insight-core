#!/usr/bin/env python3
"""Validate tarot datasets and art manifest slug references."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MANIFEST_PATH = ROOT / "art" / "manifest.json"

EXPECTED_DATASET_VERSIONS = {"1.4", "1.5", "1.6", "1.6.1"}
SHORT_DESCRIPTION_VERSIONS = {"1.6", "1.6.1"}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
POSITIONAL_KEYS = ("past", "obstacle", "present", "future", "advice", "hopes_fears")
MINOR_SUITS = {"Wands", "Cups", "Swords", "Pentacles"}

CARD_REQUIRED_FIELDS = {
    "key",
    "card_type",
    "id",
    "number",
    "slug",
    "name",
    "arcana",
    "suit",
    "element",
    "elemental_weight",
    "astrology",
    "tags",
    "life_domains",
    "meanings",
    "positional_weights",
    "positional_text",
}


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def add_error(errors: list[str], context: str, message: str) -> None:
    errors.append(f"{context}: {message}")


def load_json(path: Path, errors: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        add_error(errors, str(path.relative_to(ROOT)), "file not found")
    except json.JSONDecodeError as exc:
        add_error(errors, str(path.relative_to(ROOT)), f"invalid JSON ({exc})")
    return None


def validate_manifest(errors: list[str]) -> set[str]:
    manifest = load_json(MANIFEST_PATH, errors)
    if not isinstance(manifest, dict):
        add_error(errors, "art/manifest.json", "must be a JSON object")
        return set()

    cards = manifest.get("cards")
    if not isinstance(cards, dict):
        add_error(errors, "art/manifest.json.cards", "must be an object of slug => asset id")
        return set()

    if len(cards) != 78:
        add_error(errors, "art/manifest.json.cards", f"must contain 78 slugs, found {len(cards)}")

    manifest_slugs: set[str] = set()
    for slug, asset_id in cards.items():
        path = f"art/manifest.json.cards.{slug}"
        if not isinstance(slug, str) or not SLUG_RE.match(slug):
            add_error(errors, path, "slug key must be kebab-case")
            continue
        manifest_slugs.add(slug)
        if not isinstance(asset_id, str) or not asset_id.strip():
            add_error(errors, path, "asset id must be a non-empty string")

    return manifest_slugs


def validate_card(
    card: Any,
    dataset_name: str,
    index: int,
    dataset_version: str,
    taxonomy_domains: set[str],
    taxonomy_elements: set[str],
    errors: list[str],
) -> str | None:
    card_ctx = f"{dataset_name}.cards[{index}]"
    if not isinstance(card, dict):
        add_error(errors, card_ctx, "must be an object")
        return None

    required_fields = set(CARD_REQUIRED_FIELDS)
    if dataset_version in SHORT_DESCRIPTION_VERSIONS:
        required_fields.add("short_description")

    missing = sorted(required_fields - set(card))
    if missing:
        add_error(errors, card_ctx, f"missing required fields: {', '.join(missing)}")

    for field in ("key", "card_type", "id", "slug", "name", "arcana", "element", "astrology"):
        if field in card and not isinstance(card[field], str):
            add_error(errors, f"{card_ctx}.{field}", "must be a string")

    card_type = card.get("card_type")
    if isinstance(card_type, str) and card_type not in {"Major Arcana", "Pip Card", "Court Card"}:
        add_error(errors, f"{card_ctx}.card_type", "must be one of 'Major Arcana', 'Pip Card', or 'Court Card'")

    if dataset_version in SHORT_DESCRIPTION_VERSIONS and "short_description" in card:
        if not isinstance(card["short_description"], str) or not card["short_description"].strip():
            add_error(errors, f"{card_ctx}.short_description", "must be a non-empty string")

    slug = card.get("slug")
    if isinstance(slug, str) and not SLUG_RE.match(slug):
        add_error(errors, f"{card_ctx}.slug", "must be kebab-case")

    number = card.get("number")
    if "number" in card and not isinstance(number, int):
        add_error(errors, f"{card_ctx}.number", "must be an integer")

    suit = card.get("suit")
    if "suit" in card and suit is not None and not isinstance(suit, str):
        add_error(errors, f"{card_ctx}.suit", "must be a string or null")

    arcana = card.get("arcana")
    if isinstance(arcana, str):
        if arcana not in {"Major", "Minor"}:
            add_error(errors, f"{card_ctx}.arcana", "must be either 'Major' or 'Minor'")
        elif arcana == "Major":
            if suit is not None:
                add_error(errors, f"{card_ctx}.suit", "must be null for Major arcana cards")
            if isinstance(number, int) and not (0 <= number <= 21):
                add_error(errors, f"{card_ctx}.number", "must be between 0 and 21 for Major arcana cards")
            if card.get("card_type") != "Major Arcana":
                add_error(errors, f"{card_ctx}.card_type", "must be 'Major Arcana' when arcana is 'Major'")
        else:
            if suit not in MINOR_SUITS:
                add_error(errors, f"{card_ctx}.suit", "must be one of Wands/Cups/Swords/Pentacles for Minor arcana cards")
            if isinstance(number, int) and not (1 <= number <= 14):
                add_error(errors, f"{card_ctx}.number", "must be between 1 and 14 for Minor arcana cards")
            if isinstance(number, int):
                expected_minor_type = "Pip Card" if number <= 10 else "Court Card"
                if card.get("card_type") != expected_minor_type:
                    add_error(
                        errors,
                        f"{card_ctx}.card_type",
                        f"must be {expected_minor_type!r} when arcana is 'Minor' and number is {number}",
                    )

    if card.get("key") != card.get("id"):
        add_error(errors, f"{card_ctx}.id", "must match key")

    if "elemental_weight" in card and not is_number(card["elemental_weight"]):
        add_error(errors, f"{card_ctx}.elemental_weight", "must be a number")

    for list_field in ("tags", "life_domains"):
        value = card.get(list_field)
        if value is None:
            continue
        if not isinstance(value, list):
            add_error(errors, f"{card_ctx}.{list_field}", "must be an array of strings")
            continue
        for value_index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                add_error(errors, f"{card_ctx}.{list_field}[{value_index}]", "must be a non-empty string")

    for domain in card.get("life_domains", []):
        if isinstance(domain, str) and taxonomy_domains and domain not in taxonomy_domains:
            add_error(errors, f"{card_ctx}.life_domains", f"contains unknown domain '{domain}'")

    element = card.get("element")
    if isinstance(element, str) and taxonomy_elements and element not in taxonomy_elements:
        add_error(errors, f"{card_ctx}.element", f"contains unknown element '{element}'")

    meanings = card.get("meanings")
    if meanings is not None:
        if not isinstance(meanings, dict):
            add_error(errors, f"{card_ctx}.meanings", "must be an object")
        else:
            for orientation in ("upright", "reversed"):
                meaning = meanings.get(orientation)
                if not isinstance(meaning, dict):
                    add_error(errors, f"{card_ctx}.meanings.{orientation}", "must be an object")
                    continue
                keywords = meaning.get("keywords")
                if not isinstance(keywords, list) or not keywords:
                    add_error(errors, f"{card_ctx}.meanings.{orientation}.keywords", "must be a non-empty array")
                else:
                    for keyword_index, keyword in enumerate(keywords):
                        if not isinstance(keyword, str) or not keyword.strip():
                            add_error(
                                errors,
                                f"{card_ctx}.meanings.{orientation}.keywords[{keyword_index}]",
                                "must be a non-empty string",
                            )
                description = meaning.get("description")
                if not isinstance(description, str) or not description.strip():
                    add_error(errors, f"{card_ctx}.meanings.{orientation}.description", "must be a non-empty string")

    for field_name, value_type in (("positional_weights", "number"), ("positional_text", "string")):
        value = card.get(field_name)
        if value is None:
            continue
        if not isinstance(value, dict):
            add_error(errors, f"{card_ctx}.{field_name}", "must be an object")
            continue
        missing_keys = sorted(set(POSITIONAL_KEYS) - set(value))
        if missing_keys:
            add_error(errors, f"{card_ctx}.{field_name}", f"missing keys: {', '.join(missing_keys)}")
        for key in POSITIONAL_KEYS:
            if key not in value:
                continue
            field_value = value[key]
            field_path = f"{card_ctx}.{field_name}.{key}"
            if value_type == "number" and not is_number(field_value):
                add_error(errors, field_path, "must be a number")
            if value_type == "string" and (not isinstance(field_value, str) or not field_value.strip()):
                add_error(errors, field_path, "must be a non-empty string")

    return slug if isinstance(slug, str) else None


def validate_dataset(path: Path, manifest_slugs: set[str], errors: list[str]) -> None:
    dataset = load_json(path, errors)
    dataset_name = str(path.relative_to(ROOT))
    if not isinstance(dataset, dict):
        add_error(errors, dataset_name, "must be a JSON object")
        return

    for key in ("deck_metadata", "taxonomy", "cards"):
        if key not in dataset:
            add_error(errors, dataset_name, f"missing top-level key '{key}'")

    metadata = dataset.get("deck_metadata")
    if not isinstance(metadata, dict):
        add_error(errors, f"{dataset_name}.deck_metadata", "must be an object")
        return

    for key in ("version", "engine_compatibility", "total_cards", "description", "schema_version"):
        if key not in metadata:
            add_error(errors, f"{dataset_name}.deck_metadata", f"missing key '{key}'")

    if "total_cards" in metadata and metadata["total_cards"] != 78:
        add_error(errors, f"{dataset_name}.deck_metadata.total_cards", f"must be 78, found {metadata['total_cards']}")

    if "schema_version" in metadata and not isinstance(metadata["schema_version"], str):
        add_error(errors, f"{dataset_name}.deck_metadata.schema_version", "must be a string")

    file_version = path.stem.removeprefix("tarot_data_v")
    schema_version = metadata.get("schema_version")
    if isinstance(schema_version, str) and schema_version != file_version:
        add_error(
            errors,
            f"{dataset_name}.deck_metadata.schema_version",
            f"must match filename version {file_version!r}, found {schema_version!r}",
        )

    taxonomy = dataset.get("taxonomy")
    taxonomy_domains: set[str] = set()
    taxonomy_elements: set[str] = set()
    if not isinstance(taxonomy, dict):
        add_error(errors, f"{dataset_name}.taxonomy", "must be an object")
    else:
        domains = taxonomy.get("life_domains")
        if not isinstance(domains, list):
            add_error(errors, f"{dataset_name}.taxonomy.life_domains", "must be an array of strings")
        else:
            for index, domain in enumerate(domains):
                if not isinstance(domain, str) or not domain.strip():
                    add_error(errors, f"{dataset_name}.taxonomy.life_domains[{index}]", "must be a non-empty string")
                else:
                    taxonomy_domains.add(domain)

        elements = taxonomy.get("element")
        if not isinstance(elements, list):
            add_error(errors, f"{dataset_name}.taxonomy.element", "must be an array of strings")
        else:
            for index, element in enumerate(elements):
                if not isinstance(element, str) or not element.strip():
                    add_error(errors, f"{dataset_name}.taxonomy.element[{index}]", "must be a non-empty string")
                else:
                    taxonomy_elements.add(element)

    cards = dataset.get("cards")
    if not isinstance(cards, list):
        add_error(errors, f"{dataset_name}.cards", "must be an array")
        return

    if len(cards) != 78:
        add_error(errors, f"{dataset_name}.cards", f"must contain 78 cards, found {len(cards)}")

    seen_slugs: set[str] = set()
    for index, card in enumerate(cards):
        slug = validate_card(
            card,
            dataset_name,
            index,
            file_version,
            taxonomy_domains,
            taxonomy_elements,
            errors,
        )
        if slug is None:
            continue
        if slug in seen_slugs:
            add_error(errors, f"{dataset_name}.cards[{index}].slug", f"duplicate slug '{slug}'")
        seen_slugs.add(slug)

    if len(seen_slugs) != 78:
        add_error(errors, f"{dataset_name}.cards.slug", f"must have 78 unique slugs, found {len(seen_slugs)}")

    unknown_manifest_slugs = sorted(manifest_slugs - seen_slugs)
    if unknown_manifest_slugs:
        add_error(
            errors,
            f"{dataset_name} vs art/manifest.json",
            f"manifest includes unknown slugs: {', '.join(unknown_manifest_slugs)}",
        )

    missing_manifest_slugs = sorted(seen_slugs - manifest_slugs)
    if missing_manifest_slugs:
        add_error(
            errors,
            f"{dataset_name} vs art/manifest.json",
            f"manifest is missing slugs: {', '.join(missing_manifest_slugs)}",
        )


def main() -> int:
    errors: list[str] = []
    manifest_slugs = validate_manifest(errors)

    dataset_paths = sorted(DATA_DIR.glob("tarot_data_v*.json"))
    dataset_versions = {path.stem.removeprefix("tarot_data_v") for path in dataset_paths}

    missing_versions = sorted(EXPECTED_DATASET_VERSIONS - dataset_versions)
    if missing_versions:
        add_error(errors, "data/", f"missing expected dataset versions: {', '.join(missing_versions)}")

    for path in dataset_paths:
        validate_dataset(path, manifest_slugs, errors)

    if errors:
        print("Dataset validation failed:")
        for message in errors:
            print(f"- {message}")
        return 1

    print(
        f"Validated {len(dataset_paths)} dataset files and art/manifest.json successfully "
        f"({', '.join(sorted(dataset_versions))})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
