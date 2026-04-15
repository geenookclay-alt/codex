from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def validate_text_items(text_items: list[dict]) -> ValidationResult:
    result = ValidationResult()
    seen_indexes: set[int] = set()
    previous_index: int | None = None

    for item in text_items:
        idx = item.get("source_index")
        if not isinstance(idx, int):
            result.errors.append(f"Invalid index in item: {item}")
            continue

        if idx in seen_indexes:
            result.warnings.append(f"Duplicate source_index detected: {idx}")
        seen_indexes.add(idx)

        if previous_index is not None and idx < previous_index:
            result.warnings.append(
                f"Reversed ordering detected: {idx} after {previous_index}"
            )
        previous_index = idx

    return result
