"""Re-derive every figure of the skill's ten examples from the bundle's reference files."""
import json
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
PAIRS = json.loads((BUNDLE / "research/raw/extract-pairs-reach-appetite/pairs.json").read_text())["models"]
PRICES = json.loads((BUNDLE / "tool/usage-prices.json").read_text())["models"]
PARAMS = json.loads((BUNDLE / "tool/usage-params.json").read_text())
PRICE_KEY = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5", "fable": "claude-fable-5-2"}
SUITE = "Terminal-Bench 4.0 [AA]"
EFFORTS = ("low", "high", "max")
MILLION = 1_000_000


def price(model, part):
    return PRICES[PRICE_KEY[model]][part]


def variant(model, effort):
    pair = PAIRS[model]["pairs"][effort]
    speed = {s.get("effort"): s["value"] for s in PAIRS[model]["speed"] if s.get("kind") == "published"}[effort]
    return {
        "capability": round(pair["reach"][SUITE]["value"], 3),
        "appetite": round(pair["tokens_generated"][SUITE]["value"]),
        "dollars": round(pair["dollars"][SUITE]["value"], 2),
        "speed": round(speed, 1),
    }


def generation_minutes(v):
    return v["appetite"] / v["speed"] / 60


def work_unit(v, check, rework):
    return (v["dollars"] + check + (1 - v["capability"]) * rework) / v["capability"]


V = {(m, e): variant(m, e) for m in PRICE_KEY for e in EFFORTS}

print("== variants: capability, appetite, dollars an attempt, speed, generation minutes, output share of dollars")
for (m, e), v in V.items():
    output_dollars = v["appetite"] * price(m, "output") / MILLION
    print(m, e, v["capability"], f"{v['appetite']:,}", v["dollars"], v["speed"], round(generation_minutes(v), 1), f"{output_dollars / v['dollars']:.0%}")

print("== effort: appetite, dollars and generation time, high over low, max over low, max over high; capability gained")
for m in PRICE_KEY:
    low, high, top = (V[m, e] for e in EFFORTS)
    ratios = [round(a[k] / b[k], 2) for k in ("appetite", "dollars") for a, b in ((high, low), (top, low), (top, high))]
    time_ratio = round(generation_minutes(top) / generation_minutes(high), 2)
    print(m, ratios, "generation max over high", time_ratio, "capability gained", round(high["capability"] - low["capability"], 3), round(top["capability"] - high["capability"], 3))

print("== one capability two ways")
for a, b in ((("haiku", "max"), ("opus", "low")), (("sonnet", "max"), ("fable", "low"))):
    va, vb = V[a], V[b]
    print(a, va, round(generation_minutes(va), 1), "|", b, vb, round(generation_minutes(vb), 1))
    print("  dollars ratio", round(max(va["dollars"], vb["dollars"]) / min(va["dollars"], vb["dollars"]), 2), "generation ratio", round(max(generation_minutes(va), generation_minutes(vb)) / min(generation_minutes(va), generation_minutes(vb)), 2), "capability gap", round(abs(va["capability"] - vb["capability"]), 3))

print("== check and rework: dollars a work unit, sonnet at high against opus at high")
for check, rework in ((0, 0), (6, 5)):
    print("check", check, "rework", rework, round(work_unit(V["sonnet", "high"], check, rework), 2), round(work_unit(V["opus", "high"], check, rework), 2))

print("== carry: a context starting at 40k tokens that gains 2k a step")
carry = lambda steps: steps * 40_000 + 2_000 * steps * (steps - 1) // 2
print("100 steps", carry(100), "200 steps", carry(200), "second hundred over first", round((carry(200) - carry(100)) / carry(100), 2))
for m in PRICE_KEY:
    print(m, "generated token in carried tokens", round(price(m, "output") / price(m, "cache_read")), "| a 300k step in generated tokens", round(300_000 * price(m, "cache_read") / price(m, "output")))

print("== wait past the TTL")
print("opus 380k cold start, 5-minute", 380_000 * price("opus", "cache_write_5m") / MILLION, "| two steps inside the TTL", 2 * 380_000 * price("opus", "cache_read") / MILLION)
for m in PRICE_KEY:
    print(m, "cold start in steps of carry: 5-minute", price(m, "cache_write_5m") / price(m, "cache_read"), "1-hour", price(m, "cache_write_1h") / price(m, "cache_read"))
print("1-hour intake over 5-minute intake", price("opus", "cache_write_1h") / price("opus", "cache_write_5m"), "| pays past this share of cold starts in intake", round(1 - 1.25 / 2, 3))

print("== continue or start fresh: opus, 440k held, cache lapsed, 1-hour TTL, 20 steps left")
cold = 440_000 * price("opus", "cache_write_1h") / MILLION
kept = 20 * 440_000 * price("opus", "cache_read") / MILLION
fresh = 60_000 * price("opus", "cache_write_1h") / MILLION + 20 * 80_000 * price("opus", "cache_read") / MILLION
print("continued", cold, "+", kept, "=", round(cold + kept, 2), "| fresh", round(fresh, 2), "| gap", round(cold + kept - fresh, 2), "= generated tokens", round((cold + kept - fresh) / price("opus", "output") * MILLION))
print("one warm step that writes a file", 440_000 * price("opus", "cache_read") / MILLION)

print("== where the bulk is read: 300k tokens of logs")
print("fable intake", 300_000 * price("fable", "cache_write_1h") / MILLION, "carry a step", 300_000 * price("fable", "cache_read") / MILLION, "| sonnet intake", 300_000 * price("sonnet", "cache_write_1h") / MILLION, "report of 3k into fable", 3_000 * price("fable", "cache_write_1h") / MILLION)

print("== own steps: 400k of context on fable")
step = 400_000 * price("fable", "cache_read") / MILLION
print("one step", step, "= generated tokens", step / price("fable", "output") * MILLION, "| 100 steps", 100 * step, "| cold start, 1-hour", 400_000 * price("fable", "cache_write_1h") / MILLION)

print("== limit weights against prices, opus")
share = PARAMS["limit_share_percent_per_million_tokens"]["claude-opus-5-5"]["value"]
print("weights output : intake : carry", round(share["output"] / share["cache_read"], 1), round(share["cache_write"] / share["cache_read"], 1), 1)
print("prices  output : 5-minute intake : carry", price("opus", "output") / price("opus", "cache_read"), price("opus", "cache_write_5m") / price("opus", "cache_read"), 1)
