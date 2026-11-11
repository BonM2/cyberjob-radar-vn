"""Manual, read-only Phase 0 probe for two candidate job boards.

Before running, verify permission for the selected board and permission to
display/retain the aggregate report. If request frequency is unverified, only
one GET is allowed per invocation; this is not a provider-approved rate. This probe
does not establish those permissions or mark a source as verified. It outputs
only a JSON report to stdout; it never saves response bodies or job descriptions.
Lever may include descriptions in its response even though this script only
examines titles and locations. No requests are made on import.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit


SOURCES = {
    "axon": {
        "provider": "greenhouse",
        "endpoint": "https://boards-api.greenhouse.io/v1/boards/axon/jobs",
        "board": "https://job-boards.greenhouse.io/axon",
    },
    "amanotes": {
        "provider": "lever",
        "endpoint": "https://api.lever.co/v0/postings/amanotes",
        "board": "https://jobs.lever.co/amanotes",
    },
}

# These deliberately narrow indicators are not a trained classifier.
SECURITY_PATTERN = re.compile(
    r"\b(?:cybersecurity|cyber security|information security|"
    r"network security|security operations|security analyst|security engineer|"
    r"security architect|security specialist|security consultant|soc analyst|soc engineer|"
    r"application security|cloud security|infosec|"
    r"an toan thong tin|an ninh thong tin|an ninh mang|bao mat thong tin)\b"
)
ENTRY_LEVEL_PATTERN = re.compile(r"\b(?:intern|internship|thuc tap|fresher|junior)\b")
VIETNAM_PATTERN = re.compile(
    r"\b(?:viet nam|vietnam|ho chi minh|hcmc|hcm|"
    r"saigon|ha noi|hanoi|da nang|danang)\b"
)
MAX_BODY_BYTES = 8 * 1024 * 1024


def normalized_text(value: str) -> str:
    text = unicodedata.normalize("NFD", value.casefold().replace("đ", "d"))
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).split())


def valid_public_url(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parts = urlsplit(value.strip())
        return (
            parts.scheme in {"http", "https"}
            and bool(parts.hostname)
            and parts.username is None
            and parts.password is None
            and parts.port != 0
        )
    except ValueError:
        return False


def evidence_url(value: str) -> str:
    """Accept a public, credential-free reference without query or fragment."""
    try:
        parts = urlsplit(value)
        if (
            parts.scheme != "https"
            or not parts.hostname
            or "." not in parts.hostname
            or ".." in parts.hostname
            or not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", parts.hostname)
            or parts.username is not None
            or parts.password is not None
            or parts.query
            or parts.fragment
            or parts.port not in (None, 443)
        ):
            raise ValueError
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Provide an HTTPS evidence URL without credentials, query, or fragment."
        ) from exc
    return value


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Manual GET-only smoke test. Verify the selected board's access, "
            "and aggregate-report permissions before running. An unknown request "
            "frequency limits each invocation to one GET; it does not establish permission."
        )
    )
    parser.add_argument(
        "--source", choices=tuple(SOURCES), default="axon",
        help="Board to inspect (default: axon).",
    )
    parser.add_argument(
        "--access-basis", type=evidence_url,
        help="HTTPS access reference; defaults to provider API documentation, not board-specific permission.",
    )
    parser.add_argument(
        "--rate-basis", type=evidence_url, default=None,
        help="HTTPS rate evidence, if verified. If omitted, report it as unknown and allow only one GET.",
    )
    access_confirmation = parser.add_mutually_exclusive_group(required=True)
    access_confirmation.add_argument(
        "--confirm-access", action="store_true",
        help="Confirm permitted read-only access to this board; does not confirm its rate limit.",
    )
    access_confirmation.add_argument(
        "--confirm-access-and-rate", action="store_true",
        help="Confirm that the selected board's read access and run frequency are permitted.",
    )
    parser.add_argument(
        "--confirm-report-permission", required=True, action="store_true",
        help="Confirm that displaying the aggregate technical report is permitted.",
    )
    parser.add_argument(
        "--max-requests", type=int, choices=range(1, 4), default=1,
        help="Maximum GET requests for this run (1-3; default: 1).",
    )
    parser.add_argument(
        "--min-interval-seconds", type=float, default=5.0,
        help="Minimum interval between request starts (at least 5 seconds).",
    )
    parser.add_argument(
        "--page-size", type=int, choices=range(1, 51), default=50,
        help="Lever page size (1-50; default: 50); unused for Greenhouse.",
    )
    args = parser.parse_args()
    if args.access_basis is None:
        args.access_basis = (
            "https://docs.greenhouse.io/job-board"
            if args.source == "axon"
            else "https://github.com/lever/postings-api"
        )
    if args.confirm_access_and_rate and args.rate_basis is None:
        parser.error("--confirm-access-and-rate requires --rate-basis")
    if args.max_requests > 1 and not (args.rate_basis and args.confirm_access_and_rate):
        parser.error("More than one GET requires --rate-basis and --confirm-access-and-rate")
    if not 5.0 <= args.min_interval_seconds <= 3600.0:
        parser.error("--min-interval-seconds must be between 5 and 3600")
    return args


def location_for(job: dict[str, Any], provider: str) -> str | None:
    if provider == "greenhouse":
        location = job.get("location")
        value = location.get("name") if isinstance(location, dict) else None
    else:
        categories = job.get("categories")
        value = categories.get("location") if isinstance(categories, dict) else None
    return value.strip() if isinstance(value, str) and value.strip() else None


def check_jobs(jobs: list[Any], provider: str, seen: set[str]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "received_count": len(jobs),
        "invalid_record_count": 0,
        "missing_or_invalid": {"id": 0, "title": 0, "location": 0, "url": 0},
        "possible_cybersecurity_vietnam_count": 0,
        "possible_cybersecurity_vietnam_entry_level_count": 0,
        "title_keyword_without_explicit_vietnam_count": 0,
        "duplicate_id_count": 0,
    }
    for job in jobs:
        if not isinstance(job, dict):
            result["invalid_record_count"] += 1
            for field in result["missing_or_invalid"]:
                result["missing_or_invalid"][field] += 1
            continue
        job_id = job.get("id")
        valid_id = (
            isinstance(job_id, (str, int))
            and not isinstance(job_id, bool)
            and bool(str(job_id).strip())
        )
        title = job.get("title" if provider == "greenhouse" else "text")
        valid_title = isinstance(title, str) and bool(title.strip())
        location = location_for(job, provider)
        url = job.get("absolute_url" if provider == "greenhouse" else "hostedUrl")
        checks = {
            "id": valid_id,
            "title": valid_title,
            "location": location is not None,
            "url": valid_public_url(url),
        }
        for field, valid in checks.items():
            if not valid:
                result["missing_or_invalid"][field] += 1
        if valid_id:
            key = str(job_id).strip()
            if key in seen:
                result["duplicate_id_count"] += 1
            seen.add(key)
        if valid_title and SECURITY_PATTERN.search(normalized_text(title)):
            if location and VIETNAM_PATTERN.search(normalized_text(location)):
                result["possible_cybersecurity_vietnam_count"] += 1
                if ENTRY_LEVEL_PATTERN.search(normalized_text(title)):
                    result["possible_cybersecurity_vietnam_entry_level_count"] += 1
            else:
                result["title_keyword_without_explicit_vietnam_count"] += 1
    return result


def run_probe(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    source = SOURCES[args.source]
    provider = source["provider"]
    report: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": args.source,
        "provider": provider,
        "board": source["board"],
        "endpoint": source["endpoint"],
        "source_status": "candidate; not verified by this tool",
        "access_basis_reference": args.access_basis,
        "access_reference_note": "A provider documentation URL is not proof of board-specific permission.",
        "rate_evidence_supplied_by_operator": args.rate_basis,
        "rate_status": "operator_confirmed_not_independently_verified" if args.confirm_access_and_rate else "unverified",
        "request_limit": args.max_requests,
        "min_interval_seconds": args.min_interval_seconds,
        "run_outcome": "not_completed",
        "count_note": "Counts describe received records only; zero pages is not evidence of an empty board.",
        "exit_code_note": "Zero means no request or parsing error, not source verification or Phase 0 PASS.",
        "request_count": 0,
        "requests": [],
        "pages_read": 0,
        "received_count": 0,
        "unique_identified_jobs": 0,
        "missing_or_invalid": {"id": 0, "title": 0, "location": 0, "url": 0},
        "invalid_record_count": 0,
        "duplicate_id_count": 0,
        "possible_cybersecurity_vietnam_count": 0,
        "possible_cybersecurity_vietnam_entry_level_count": 0,
        "title_keyword_without_explicit_vietnam_count": 0,
        "pagination_complete": None,
        "pagination_evidence": [],
        "errors": [],
        "unverified_conditions": [
            "The operator-supplied access and rate evidence has not been verified by this script.",
            "Permission to store or display job metadata, descriptions, and fixtures remains to be verified separately.",
            "Pagination semantics, full board coverage, and a stable snapshot require manual verification.",
            "The original job URL has not been opened or verified by this script.",
            "Real response fixtures and labelled classifier samples have not been created.",
        ],
        "classification_limitations": (
            "Indicators use only title and a single location string, not JD text. "
            "They can miss relevant jobs or count unrelated/ambiguous jobs. "
            "Counts include duplicates and must not be treated as validated classification."
        ),
    }
    if not args.confirm_access_and_rate:
        report["unverified_conditions"].append(
            "Allowed request frequency is unverified. One GET per invocation is a local cap, "
            "not a provider rate limit; repeated runs also require consideration."
        )
    try:
        import httpx
    except ImportError:
        report["errors"].append("HTTPX is not installed in the selected Python environment.")
        report["run_outcome"] = "error"
        return report, 1

    seen: set[str] = set()
    offset = 0
    last_started: float | None = None
    # No redirects, retries, credentials, proxy environment, or automatic source discovery.
    with httpx.Client(timeout=15.0, follow_redirects=False, trust_env=False) as client:
        for _ in range(args.max_requests):
            if last_started is not None:
                time.sleep(max(0.0, args.min_interval_seconds - (time.monotonic() - last_started)))
            params = {"mode": "json", "limit": args.page_size, "skip": offset} if provider == "lever" else {}
            entry: dict[str, Any] = {
                "endpoint": source["endpoint"], "params": params, "http_status": None,
                "content_type": None, "time_to_headers_ms": None,
                "elapsed_ms": None, "json_valid": None,
            }
            report["requests"].append(entry)
            report["request_count"] += 1
            last_started = time.monotonic()
            started = time.perf_counter()
            try:
                with client.stream("GET", source["endpoint"], params=params) as response:
                    entry["time_to_headers_ms"] = round((time.perf_counter() - started) * 1000, 1)
                    entry["http_status"] = response.status_code
                    entry["content_type"] = response.headers.get("content-type")
                    if response.status_code != 200:
                        report["errors"].append(f"HTTP {response.status_code}; stopped without retry or redirect.")
                        break
                    media_type = (entry["content_type"] or "").split(";", 1)[0].strip().lower()
                    if media_type != "application/json" and not media_type.endswith("+json"):
                        report["errors"].append("Unexpected content type; body not examined.")
                        break
                    chunks: list[bytes] = []
                    size = 0
                    for chunk in response.iter_bytes():
                        size += len(chunk)
                        if size > MAX_BODY_BYTES:
                            raise ValueError("Response exceeded the in-memory size limit.")
                        chunks.append(chunk)
                    try:
                        payload = json.loads(b"".join(chunks))
                    except (ValueError, UnicodeDecodeError):
                        entry["json_valid"] = False
                        report["errors"].append("Response is not valid JSON.")
                        break
                    entry["json_valid"] = True
                    if provider == "greenhouse":
                        jobs = payload.get("jobs") if isinstance(payload, dict) else None
                    else:
                        jobs = payload
                    if not isinstance(jobs, list):
                        report["errors"].append("Unexpected JSON structure: job list missing.")
                        break
                    page = check_jobs(jobs, provider, seen)
                    entry["page"] = page
                    report["pages_read"] += 1
                    for key in ("received_count", "invalid_record_count", "duplicate_id_count",
                                "possible_cybersecurity_vietnam_count",
                                "possible_cybersecurity_vietnam_entry_level_count",
                                "title_keyword_without_explicit_vietnam_count"):
                        report[key] += page[key]
                    for field, count in page["missing_or_invalid"].items():
                        report["missing_or_invalid"][field] += count
                    if provider == "greenhouse":
                        meta = payload.get("meta")
                        total = meta.get("total") if isinstance(meta, dict) else None
                        if isinstance(total, int) and not isinstance(total, bool) and total >= 0:
                            report["pagination_evidence"].append(
                                f"Greenhouse meta.total={total}; received={len(jobs)}. "
                                "Equality alone does not prove complete board coverage."
                            )
                        else:
                            report["pagination_evidence"].append(
                                "No usable meta.total; full board coverage is not established."
                            )
                        break
                    if not jobs:
                        report["pagination_evidence"].append(
                            f"Lever returned an empty page at skip={offset}; "
                            "confirm pagination semantics and snapshot completeness manually."
                        )
                        break
                    if page["duplicate_id_count"] or page["invalid_record_count"]:
                        report["pagination_evidence"].append(
                            "Duplicate IDs or malformed records were observed; pagination is inconclusive."
                        )
                        break
                    report["pagination_evidence"].append(
                        f"Lever skip={offset}, limit={args.page_size}, received={len(jobs)}."
                    )
                    offset += len(jobs)
            except httpx.HTTPError as exc:
                report["errors"].append(f"Request failed: {type(exc).__name__}; no retry.")
                break
            except ValueError:
                report["errors"].append("Response could not be processed or exceeded the size limit.")
                break
            finally:
                entry["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 1)
        else:
            report["pagination_evidence"].append("Request budget exhausted; end of listing was not established.")
    report["unique_identified_jobs"] = len(seen)
    report["run_outcome"] = "error" if report["errors"] else "observations_require_review"
    return report, 1 if report["errors"] else 0


def main() -> int:
    args = parse_arguments()
    report, exit_code = run_probe(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
