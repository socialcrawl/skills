#!/usr/bin/env python3
"""Quote a call or a plan in credits before paying. Free either way.

usage: estimate.py <platform/resource> [k=v ...] [--items N]
       estimate.py --plan plan.json

With a key set this calls GET /v1/utility/estimate (the authoritative quote). With no key, or
when that route answers 404 / is unreachable, it falls back to the offline catalogue
(assets/endpoints.json) and says so: `source` is "api" or "offline", and an offline quote adds
an `offline` warning. The hold is the most a call can cost; the unused part is refunded.

--items N quotes reading N rows from a paged endpoint (pages x price). Offline, a request that turns
on an include= row join (the catalogue's `hydration[]`) is held at the base price plus that join's
ceiling (rows x credits_per_row, rows capped by the row-cap param, default_rows or max_rows, and a
batch join capped per lookup); joins left off are taken out of cost.max. A per_unit cost is quoted
as rate x units when the request names its units (`urls`, `items`), never as exact; otherwise
the hold is null and the formula states the rate. plan.json is
{"calls": [{"id", "params"?, "body"?, "repeat"?, "items"?, "ref"?}], "fan_out"?}; an offline plan
total is `exact: false` whenever a price is a range, a page size is unknown or fan_out is used.
Prints JSON to stdout; exit 1 when the quote is invalid. A key is optional here.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import sys
import urllib.parse

import sclib

OFFLINE_WARNING = "offline: quoted from assets/endpoints.json, not the live estimator; metered ranges are the registry's bounds"


# --------------------------------------------------------------------------- offline


def _int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def check(ep: dict, given: dict) -> str | None:
    """The first reason this call would be rejected, or None."""
    spec = {p["name"]: p for p in ep["params"]}
    for p in ep["params"]:
        if p.get("required") and given.get(p["name"]) in (None, ""):
            return f"Missing required parameter: {p['name']}"
    for group in ep.get("one_of") or []:
        if not any(given.get(n) not in (None, "") for n in group):
            return f"Provide at least one of: {', '.join(group)}"
    for name, value in given.items():
        p = spec.get(name)
        if not p:
            continue
        if p.get("type") == "enum" and str(value) not in p.get("enum", []):
            return f"{name} must be one of: {', '.join(p['enum'])}"
        if p.get("type") == "integer":
            n = _int(value)
            if n is None:
                return f"{name} must be an integer"
            if p.get("minimum") is not None and n < p["minimum"]:
                return f"{name} must be at least {p['minimum']}"
            if p.get("maximum") is not None and n > p["maximum"]:
                return f"{name} must be at most {p['maximum']}"
        csv_rule = p.get("csv")
        if csv_rule and isinstance(value, str):
            parts = [x for x in value.split(",") if x]
            if csv_rule.get("max") and len(parts) > csv_rule["max"]:
                return f"{name} takes at most {csv_rule['max']} comma-separated values"
            if csv_rule.get("enum") and any(x not in csv_rule["enum"] for x in parts):
                return f"{name} values must each be one of: {', '.join(csv_rule['enum'])}"
    return None


UNIT_KEYS = ("urls", "items")


def count_units(given: dict) -> int | None:
    """How many units a per_unit request covers, when it names them in a list."""
    for k in UNIT_KEYS:
        v = given.get(k)
        v = sclib.jsonish(v) if isinstance(v, str) else v
        if isinstance(v, list):
            return len(v)
    return None


def _credits(n) -> str:
    return f"{n:g} credit{'' if n == 1 else 's'}"


def quote_per_unit(cost: dict, given: dict) -> tuple[dict, list]:
    unit = cost.get("unit") or "unit"
    lo_rate, hi_rate = cost.get("min") or 0, cost.get("max")
    rate = hi_rate if hi_rate is not None else lo_rate
    n = count_units(given)
    rule = cost.get("rule")
    warnings = [f"per_unit: priced per {unit}, so the quote is not exact." + (f" Rule: {rule}" if rule else "")]
    if n is None:
        band = _credits(lo_rate) if hi_rate is None else f"{lo_rate:g}-{_credits(hi_rate)}"
        formula = (f"Priced per {unit} (from {band} each): the total depends on how many {unit}s the request runs, "
                   "so there is no fixed hold to quote.")
        return {"hold": None, "expected_min": None, "expected_max": None, "exact": False, "formula": formula,
                "units": {"unit": unit, "count": None, "rate": rate}}, warnings
    lo, hi = lo_rate * n, rate * n
    formula = f"{_credits(rate)} per {unit} x {n} = {_credits(hi)}" + ("." if lo == hi else f" (at least {_credits(lo)}).")
    return {"hold": hi, "expected_min": lo, "expected_max": hi, "exact": False, "formula": formula,
            "units": {"unit": unit, "count": n, "rate": rate}}, warnings


def quote_call(cat: dict, call: dict, items: int | None = None) -> dict:
    endpoint_id = sclib.normalize_id(call["id"])
    method = (call.get("method") or "").upper() or None
    ep = sclib.find_endpoint(cat, endpoint_id, method)
    given = {**(call.get("params") or {}), **(call.get("body") or {})}
    given = {k: v for k, v in given.items() if v is not None}
    out = {"id": endpoint_id, "valid": True, "unit": "credits", "normalized_params": {k: v for k, v in (call.get("params") or {}).items() if v is not None},
           "levers": [], "warnings": [], "source": "offline"}
    if call.get("ref"):
        out["ref"] = call["ref"]
    if ep is None:
        out.update(valid=False, hold=0, expected_min=0, expected_max=0, rejection={"code": "ENDPOINT_NOT_FOUND", "message": f"{endpoint_id} is not in the offline catalogue"})
        return out
    reason = check(ep, given)
    if reason:
        out.update(valid=False, hold=0, expected_min=0, expected_max=0, rejection={"code": "INVALID_REQUEST", "message": reason})
        return out
    cost = ep["cost"]
    paging = ep.get("paging")
    out["pricing"] = cost["model"]
    if cost["model"] == "per_unit":
        quote, warnings = quote_per_unit(cost, given)
        out.update(quote)
        out["warnings"] += warnings + [OFFLINE_WARNING]
        return out
    metered = cost["model"] != "flat"
    lo, hi, exact = cost["min"], sclib.call_ceiling(ep, given), not metered
    joins = sclib.joins_on(ep, given)
    if joins:
        out["hydration"] = [{"param": j.get("param") or "include", "token": j["token"], "rows": sclib.hydration_rows(j, given),
                             "credits": sclib.hydration_credits(j, given)} for j in joins]
    if hi is None:
        out.update(hold=None, expected_min=lo, expected_max=None, exact=False,
                   formula=f"At least {_credits(lo)}; the catalogue has no ceiling for this call.")
        out["warnings"] += ["ceiling_unknown: the offline catalogue has no cost.max for this endpoint", OFFLINE_WARNING]
        return out
    formula = f"{hi} credit{'s' if hi != 1 else ''} per call, flat." if not metered else (
        f"Metered: {hi} credits held up front (the most this request can cost); the unused part is refunded, so a successful call settles between {lo} and {hi}.")
    if joins:
        formula += " Includes " + ", ".join(f"include={j['token']} up to {_credits(sclib.hydration_credits(j, given))}" for j in joins) + "."
    n = items if items is not None else call.get("items")
    if n:
        if not paging:
            out["warnings"].append(f"not_paged: {endpoint_id} does not page, so items={n} is ignored")
        elif not paging.get("page_size"):
            out["warnings"].append(f"pages_unknown: {endpoint_id} has no verified page size, so {n} items cannot be turned into a page count. Quote one page and count pages as you go.")
            exact = False
        else:
            pages = math.ceil(n / paging["page_size"])
            cap = paging.get("max_pages")
            if cap and pages > cap:
                pages = cap
                out["warnings"].append(f"items_capped: {endpoint_id} serves at most {cap} pages, so {n} items are not all reachable.")
            basis = paging.get("price_basis")
            if basis == "per_row":
                rows = min(n, pages * paging["page_size"])
                lo = hi = rows * paging["credits_per_row"]
            else:
                per = paging.get("credits_per_page") or {"min": cost["min"], "max": hi}
                # A join-bearing page is held at this request's ceiling, not at every join's.
                per_max = hi if ep.get("hydration") or per.get("max") is None else per["max"]
                lo, hi = pages * per["min"], pages * per_max
                if basis == "unknown" or per.get("max") is None:
                    out["warnings"].append("price_basis_unknown: the per-page price of this endpoint is not proven, so the hold is the registry's ceiling per page.")
                    exact = False
                else:
                    exact = lo == hi
            out["items"] = {"n": n, "page_size": paging["page_size"], "pages": pages, "price_basis": basis}
            formula = f"{n} items: {paging.get('per_n_items') or 'pages x price'} = {pages} pages, {lo}-{hi} credits." if lo != hi else f"{n} items: {paging.get('per_n_items') or 'pages x price'} = {pages} pages, {hi} credits."
    out.update(hold=hi, expected_min=lo, expected_max=hi, formula=formula, exact=exact)
    out["warnings"].append(OFFLINE_WARNING)
    return out


def quote_plan(cat: dict, plan: dict) -> dict:
    calls = []
    for c in plan.get("calls", []):
        q = quote_call(cat, c)
        runs = c.get("repeat") if isinstance(c.get("repeat"), int) and c["repeat"] > 0 else 1
        q["runs"] = runs
        q["hold_total"] = q["hold"] * runs if q.get("hold") is not None else None
        q["expected_min_total"] = (q.get("expected_min") or 0) * runs
        calls.append(q)
    warnings = [OFFLINE_WARNING]
    unpriced = [c["id"] for c in calls if c["valid"] and c["hold_total"] is None]
    if unpriced:
        warnings.append(f"unpriced: {', '.join(unpriced)} {'has' if len(unpriced) == 1 else 'have'} no fixed hold "
                        "(a per_unit cost with no unit count, or no ceiling); the totals leave them out")
    exact = all(c.get("exact", False) for c in calls if c["valid"]) and not unpriced
    if plan.get("fan_out"):
        warnings.append("fan_out_unknown: offline quotes do not expand fan_out; the total is a floor for those calls")
        exact = False
    held = sum(c["hold_total"] for c in calls if c["hold_total"] is not None)
    total = {"hold": held, "expected_min": sum(c["expected_min_total"] for c in calls),
             "expected_max": held, "exact": exact and len(calls) > 0}
    return {"valid": all(c["valid"] for c in calls), "unit": "credits", "calls": calls, "total": total, "warnings": warnings, "source": "offline"}


# --------------------------------------------------------------------------- online


def online(key: str, endpoint_id: str | None, kv: dict, plan: dict | None):
    """The live estimate, or None when the route is unavailable (404 / unreachable)."""
    if plan is not None:
        raw = base64.urlsafe_b64encode(json.dumps(plan, separators=(",", ":")).encode()).decode().rstrip("=")
        resp = sclib.request("GET", "utility/estimate", {"plan": raw}, key=key)
    else:
        resp = sclib.request("GET", "utility/estimate", {"id": endpoint_id, "params": sclib.encode_query(kv)}, key=key)
    if resp.status in (0, 404, 405) or resp.code == "ENDPOINT_NOT_FOUND":
        return None
    return resp


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("endpoint", nargs="?")
    ap.add_argument("params", nargs="*", help="k=v params of the call")
    ap.add_argument("--items", type=int, help="quote reading N rows from a paged endpoint")
    ap.add_argument("--plan", help="path to a plan JSON file")
    ap.add_argument("--offline", action="store_true", help="never call the API")
    args = ap.parse_intermixed_args(argv)
    if not args.endpoint and not args.plan:
        ap.error("give <platform/resource> or --plan plan.json")

    plan = None
    if args.plan:
        with open(args.plan, encoding="utf-8") as f:
            plan = json.load(f)
    endpoint_id = sclib.normalize_id(args.endpoint) if args.endpoint else None
    kv = sclib.parse_kv(args.params)
    if plan is None and args.items:
        plan = {"calls": [{"id": endpoint_id, "params": kv, "items": args.items}]}

    result = None
    key = None if args.offline else sclib.resolve_key()
    if key:
        resp = online(key, endpoint_id, kv, plan)
        if resp is not None:
            if not resp.ok:
                print(json.dumps(resp.body if resp.body is not None else {"raw": resp.raw}))
                sclib.report_error(resp)
                return sclib.exit_code_for(resp)
            data = dict((resp.body or {}).get("data") or {})
            if args.items and args.endpoint and not args.plan and isinstance(data.get("total"), dict):
                first = (data.get("calls") or [{}])[0]
                data = {**first, **{k: data["total"].get(k) for k in ("hold", "expected_min", "expected_max")}, "total": data["total"]}
            data["source"] = "api"
            result = data
    if result is None:
        cat = sclib.load_catalogue()
        if not cat:
            print(json.dumps({"valid": False, "source": "offline", "rejection": {"code": "NO_CATALOGUE", "message": "assets/endpoints.json is missing and the live estimator is unavailable"}}))
            return 1
        if args.plan:
            result = quote_plan(cat, plan)
        else:
            result = quote_call(cat, {"id": endpoint_id, "params": kv}, args.items)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("valid", True) else 1


if __name__ == "__main__":
    sys.exit(main())
