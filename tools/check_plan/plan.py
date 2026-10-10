"""Parse the repository's small Markdown WP format, without executing Markdown."""

import re
from dataclasses import dataclass, field
from datetime import date

FIELDS = ("Status", "Lane", "Depends on", "Owned paths", "Learning note", "Change record")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WP = re.compile(r"WP-(\d+\.\d+)\s+(.+)")
BRANCH = re.compile(r"wp-(\d+\.\d+)-[a-zA-Z0-9][a-zA-Z0-9._/-]*")
DAY = r"\d{4}-\d{2}-\d{2}"
NAME = r"[^|\n]+?"
CLAUSES = r"due to .+?, while original was .+?, as it was better for .+?"
STATUSES = (
    ("Not started", re.compile(r"\[ \] Not started")),
    ("In progress", re.compile(
        rf"\[~\] In progress \| {NAME} \| branch (?P<branch>\S+) \| started "
        rf"(?P<date>{DAY})(?: \| blocked by [^|\n]+)?")),
    ("Done", re.compile(
        rf"\[x\] Done \| implemented by {NAME}(?: \| verified by {NAME})?"
        rf" \| commit (?:[0-9a-f]{{7,40}}|bootstrap) \| (?P<date>{DAY})")),
    ("Changed design", re.compile(
        rf"\[!\] Changed design \| {CLAUSES} \| {NAME} \| (?P<date>{DAY})")),
)


@dataclass
class WorkPackage:
    id: str
    title: str
    start: int
    end: int = 0
    fields: dict[str, list[tuple[int, str]]] = field(default_factory=dict)
    change_end: int = 0
    status: str = "Invalid"

    def value(self, name):
        entries = self.fields.get(name, [])
        return entries[0][1] if entries else ""


@dataclass
class Plan:
    lines: list[str]
    packages: dict[str, WorkPackage]
    errors: list[str]
    headings: list[tuple[int, int, str]]


def visible_lines(lines):
    """Ignore fenced examples; Markdown headings inside them are not live WPs."""
    fence = None
    for number, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", stripped)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                if not marker[2].strip():
                    fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        yield number, stripped


def parse_plan(text):
    lines = text.splitlines(keepends=True)
    packages, errors, headings = {}, [], []
    current = None
    for number, line in visible_lines(lines):
        heading = HEADING.fullmatch(line)
        if heading:
            level, title = len(heading[1]), heading[2]
            headings.append((number, level, title))
            if level <= 3 and current:
                current.end = number
                current = None
            if level == 3 and title.startswith("WP-"):
                match = WP.fullmatch(title)
                if not match:
                    errors.append(f"line {number + 1}: malformed WP heading")
                    continue
                wp_id = "WP-" + match[1]
                if wp_id in packages:
                    errors.append(f"{wp_id}: duplicate WP heading")
                current = WorkPackage(wp_id, match[2], number, len(lines))
                packages[wp_id] = current
        if current:
            for name in FIELDS:
                if line.startswith(name + ":"):
                    current.fields.setdefault(name, []).append(
                        (number, line[len(name) + 1:].strip()))
    if not packages:
        errors.append("PLAN: no work packages found")
    for wp in packages.values():
        for name in FIELDS:
            entries = wp.fields.get(name, [])
            if len(entries) != 1:
                errors.append(f"{wp.id}: expected exactly one {name}: field, found {len(entries)}")
            elif not entries[0][1] and name != "Change record":
                errors.append(f"{wp.id}: {name}: must not be empty")
        raw_status = wp.value("Status")
        for label, pattern in STATUSES:
            match = pattern.fullmatch(raw_status)
            if not match:
                continue
            wp.status = label
            if "date" in match.groupdict():
                try:
                    date.fromisoformat(match["date"])
                except ValueError:
                    errors.append(f"{wp.id}: Status: invalid calendar date")
            if label == "In progress":
                branch = BRANCH.fullmatch(match["branch"])
                if not branch or "WP-" + branch[1] != wp.id:
                    errors.append(f"{wp.id}: Status: branch must name this WP")
            break
        else:
            errors.append(f"{wp.id}: Status: must use one of the four formats; Changed design "
                          "requires due to, while original was, as it was better for")
        changes = wp.fields.get("Change record", [])
        if len(changes) == 1:
            # Change record is the final field, ending before the WP separator.
            start = changes[0][0]
            end = wp.end
            for number in range(start + 1, wp.end):
                if lines[number].strip() == "---":
                    end = number
                    break
            while end > start + 1 and not lines[end - 1].strip():
                end -= 1
            wp.change_end = end
            if wp.status == "Changed design":
                sentence = raw_status.split(" | ", 2)[1]
                record = "".join(lines[start:end])
                if sentence not in record:
                    errors.append(f"{wp.id}: Change record: must retain the Changed design sentence")
    return Plan(lines, packages, errors, headings)


def summary(plan):
    rows = [(wp.id, wp.status, wp.title) for wp in plan.packages.values()]
    widths = [max(len(row[i]) for row in [("WP", "Status", "Title"), *rows]) for i in (0, 1)]
    return "\n".join(f"{a:<{widths[0]}}  {b:<{widths[1]}}  {c}"
                     for a, b, c in [("WP", "Status", "Title"), *rows])
