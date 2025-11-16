import yaml, time

NS = yaml.safe_load(open("neurosymbiosis.yaml"))

def frame_for(agent: str) -> list[str]:
    return NS["experience_frames"].get(agent, [])

def preflight_enrich(agent: str, envelope: dict, ctx: dict) -> dict:
    system_lines = frame_for(agent)
    if system_lines:
        prelude = "\n".join(system_lines)
        envelope["input"]["messages"] = [{"role":"system","content": prelude}] + envelope["input"]["messages"]

    # memory tags
    tags = []
    for k in NS["memory_policies"]["tagging"]["required"]:
        v = ctx.get(k, None)
        if v:
            tags.append(f"{k}:{v}")
    envelope.setdefault("meta", {})["memory_tags"] = tags

    # truth receipt
    envelope.setdefault("meta", {})["truth_receipt"] = {
        "trace_id": ctx["trace_id"],
        "ts": int(time.time())
    }

    return envelope

def default_visibility(agent: str) -> str:
    return NS["memory_policies"]["visibility_defaults"][agent]
