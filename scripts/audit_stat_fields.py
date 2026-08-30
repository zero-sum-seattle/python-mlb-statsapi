#!/usr/bin/env python3
"""Audit python-mlb-statsapi stat models against live MLB Stats API payloads.

This is a developer diagnostic tool, not a CI test. It compares raw MLB JSON
keys/values with the fields populated by python-mlb-statsapi and classifies
potential schema or alias problems without making CI depend on the live API.

Examples:
    poetry run python scripts/audit_stat_fields.py
    poetry run python scripts/audit_stat_fields.py --season 2024
    poetry run python scripts/audit_stat_fields.py --stat season --verbose
    poetry run python scripts/audit_stat_fields.py --player 592450:Judge
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable

import mlbstatsapi


DEFAULT_PLAYERS = (
    (592450, "Aaron Judge"),
    (660271, "Shohei Ohtani"),
    (665742, "Juan Soto"),
)
DEFAULT_STATS = ("season", "seasonAdvanced")
DEFAULT_GROUP = "hitting"
DEFAULT_SEASON = 2025
MLB_STATS_URL = "https://statsapi.mlb.com/api/v1/people/{player_id}/stats"


@dataclass(frozen=True)
class AuditRow:
    status: str
    raw_key: str
    model_field: str
    raw_value: Any
    parsed_value: Any


def fetch_raw_stat(player_id: int, group: str, stat_type: str, season: int) -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {"stats": stat_type, "group": group, "season": season}
    )
    url = f"{MLB_STATS_URL.format(player_id=player_id)}?{query}"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "python-mlb-statsapi-stat-audit"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)

    stats = payload.get("stats", [])
    if not stats:
        raise RuntimeError("MLB returned no stats entries")

    splits = stats[0].get("splits", [])
    if not splits:
        raise RuntimeError("MLB returned no stat splits")

    stat = splits[0].get("stat")
    if not isinstance(stat, dict):
        raise RuntimeError("MLB split did not contain a stat object")

    return stat


def fetch_parsed_stat(
    mlb: mlbstatsapi.Mlb,
    player_id: int,
    group: str,
    stat_type: str,
    season: int,
) -> Any:
    parsed = mlb.get_player_stats(
        player_id,
        stats=[stat_type],
        groups=[group],
        season=season,
    )

    try:
        container = parsed[group][stat_type]
        return container.splits[0].stat
    except (KeyError, IndexError, AttributeError) as exc:
        raise RuntimeError("library returned no matching parsed stat split") from exc


def audit_stat(raw_stat: dict[str, Any], parsed_stat: Any) -> list[AuditRow]:
    model_fields = type(parsed_stat).model_fields
    rows: list[AuditRow] = []
    known_aliases: set[str] = set()

    for field_name, field_info in model_fields.items():
        alias = field_info.alias or field_name
        if not isinstance(alias, str):
            alias = field_name

        known_aliases.add(alias)
        parsed_value = getattr(parsed_stat, field_name, None)

        if alias not in raw_stat:
            rows.append(
                AuditRow(
                    status="MLB OMITTED",
                    raw_key=alias,
                    model_field=field_name,
                    raw_value=None,
                    parsed_value=parsed_value,
                )
            )
            continue

        raw_value = raw_stat[alias]
        if parsed_value == raw_value:
            status = "PASS"
        elif parsed_value is None and raw_value is not None:
            status = "PARSE FAILURE"
        else:
            status = "MISMATCH"

        rows.append(
            AuditRow(
                status=status,
                raw_key=alias,
                model_field=field_name,
                raw_value=raw_value,
                parsed_value=parsed_value,
            )
        )

    for raw_key, raw_value in raw_stat.items():
        if raw_key not in known_aliases:
            rows.append(
                AuditRow(
                    status="MODEL MISSING",
                    raw_key=raw_key,
                    model_field="-",
                    raw_value=raw_value,
                    parsed_value=None,
                )
            )

    return rows


def print_rows(rows: Iterable[AuditRow], verbose: bool) -> Counter[str]:
    rows = list(rows)
    counts = Counter(row.status for row in rows)

    visible = rows if verbose else [row for row in rows if row.status != "PASS"]
    if visible:
        print(f"{'STATUS':14} {'RAW KEY':28} {'MODEL FIELD':28} {'RAW':18} PARSED")
        print("-" * 112)
        for row in visible:
            print(
                f"{row.status:14} "
                f"{row.raw_key:28} "
                f"{row.model_field:28} "
                f"{repr(row.raw_value):18.18} "
                f"{repr(row.parsed_value)}"
            )
    else:
        print("No discrepancies or omissions found.")

    return counts


def parse_player(value: str) -> tuple[int, str]:
    player_id_text, separator, name = value.partition(":")
    try:
        player_id = int(player_id_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("player must be ID or ID:Name") from exc

    return player_id, name.strip() if separator and name.strip() else str(player_id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare live MLB stat payloads with populated model fields."
    )
    parser.add_argument("--season", type=int, default=DEFAULT_SEASON)
    parser.add_argument("--group", default=DEFAULT_GROUP)
    parser.add_argument(
        "--stat",
        dest="stats",
        action="append",
        help="Stat type to audit; repeat for multiple types. Defaults to season and seasonAdvanced.",
    )
    parser.add_argument(
        "--player",
        dest="players",
        action="append",
        type=parse_player,
        help="Player as ID or ID:Name; repeat for multiple players.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print PASS rows too; default output focuses on omissions and discrepancies.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    players = tuple(args.players) if args.players else DEFAULT_PLAYERS
    stat_types = tuple(args.stats) if args.stats else DEFAULT_STATS
    mlb = mlbstatsapi.Mlb()

    overall = Counter()
    request_failures = 0

    for player_id, player_name in players:
        for stat_type in stat_types:
            print()
            print(f"=== {player_name} ({player_id}) | {args.group}/{stat_type} | {args.season} ===")

            try:
                raw_stat = fetch_raw_stat(player_id, args.group, stat_type, args.season)
                parsed_stat = fetch_parsed_stat(
                    mlb, player_id, args.group, stat_type, args.season
                )
            except Exception as exc:  # diagnostic script: keep auditing remaining cases
                request_failures += 1
                print(f"REQUEST ERROR: {exc}")
                continue

            print(f"Parsed model: {type(parsed_stat).__module__}.{type(parsed_stat).__name__}")
            counts = print_rows(audit_stat(raw_stat, parsed_stat), args.verbose)
            overall.update(counts)
            print(
                "Summary: "
                + ", ".join(
                    f"{status}={counts.get(status, 0)}"
                    for status in (
                        "PASS",
                        "MLB OMITTED",
                        "MODEL MISSING",
                        "PARSE FAILURE",
                        "MISMATCH",
                    )
                )
            )

    print()
    print("=== OVERALL ===")
    for status in (
        "PASS",
        "MLB OMITTED",
        "MODEL MISSING",
        "PARSE FAILURE",
        "MISMATCH",
    ):
        print(f"{status:14} {overall.get(status, 0)}")
    print(f"{'REQUEST ERROR':14} {request_failures}")

    # Only actual model/parsing discrepancies fail the command. MLB omissions are
    # informational because response shape varies by stat type and player.
    if overall["MODEL MISSING"] or overall["PARSE FAILURE"] or overall["MISMATCH"]:
        return 1
    if request_failures:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
