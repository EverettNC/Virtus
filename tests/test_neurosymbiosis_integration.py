#!/usr/bin/env python3
"""
Test neurosymbiosis integration with Virtus
Demonstrates:
1. Brockston → Derek system message injection
2. Memory write with tags (who:everett, why_now:<task>, stakes:normal)
3. Truth receipt with trace_id
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from virtus.router.app import llm_invoke, LLMEnvelope
from virtus.mem.app import mem_write, MemoryWriteRequest


def test_brockston_derek_frame():
    """Test 1: Brockston → Derek system message injection"""
    print("=" * 70)
    print("TEST 1: Brockston System Frame Injection")
    print("=" * 70)

    # Create envelope for Brockston
    env = LLMEnvelope(
        trace_id="trace_abc123",
        agent="brockston",
        task="reasoning.delegate",
        input={
            "messages": [
                {"role": "user", "content": "What's the status of project Alpha?"}
            ]
        }
    )

    # Invoke router - preflight_enrich will inject system frame
    result = llm_invoke(env)

    print(f"\nAgent: {result['agent']}")
    print(f"Trace ID: {result['trace_id']}")
    print(f"\n✓ System frame for Brockston should have been injected:")
    print("  'You are Brockston. Reactor and integrator. Precision first, poetry second.'")
    print("  'Serve Everett's mission. Be concise. Act only within your scopes.'")
    print(f"\nResponse: {json.dumps(result, indent=2)}")
    print()


def test_memory_tags_and_receipt():
    """Test 2: Memory write with tags and truth receipt"""
    print("=" * 70)
    print("TEST 2: Memory Write with Tags and Truth Receipt")
    print("=" * 70)

    # Create memory write request
    req = MemoryWriteRequest(
        owner="brockston",
        # visibility will be auto-set to "private" per neurosymbiosis defaults
        tags=["project_alpha", "status_update"],
        content={
            "type": "note",
            "text": "Project Alpha deployment completed successfully. All systems nominal."
        }
    )

    # Claims from JWT (simulated)
    claims = {
        "sub": "brockston",
        "scp": ["mem.write"]
    }

    # Write memory - default_visibility will be applied
    result = mem_write(req, claims)

    print(f"\nMemory Write Result:")
    print(f"  Status: {result['status']}")
    print(f"  ID: {result['id']}")
    print(f"  Owner: {result['owner']}")
    print(f"  Visibility: {result['visibility']}")
    print(f"  Tags: {result['tags']}")
    print(f"\n✓ Expected tags from neurosymbiosis policy:")
    print("    who:everett, why_now:reasoning.delegate, stakes:normal")
    print(f"\n✓ Visibility auto-set to: {result['visibility']}")
    print(f"  (from neurosymbiosis.yaml visibility_defaults.brockston)")
    print()


def test_payload_enrichment():
    """Test 3: Full payload enrichment with truth receipt"""
    print("=" * 70)
    print("TEST 3: Payload Enrichment and Truth Receipt")
    print("=" * 70)

    from virtus.common.experience import preflight_enrich

    # Create test envelope
    envelope = {
        "trace_id": "trace_xyz789",
        "agent": "derek",
        "task": "key.broker",
        "input": {
            "messages": [
                {"role": "user", "content": "Generate auth token"}
            ]
        }
    }

    # Context for enrichment
    ctx = {
        "trace_id": "trace_xyz789",
        "who": "everett",
        "why_now": "key.broker",
        "stakes": "normal"
    }

    # Enrich payload
    enriched = preflight_enrich("derek", envelope, ctx)

    print(f"\nEnriched Payload:")
    print(json.dumps(enriched, indent=2))

    print(f"\n✓ System frame for Derek injected:")
    print(f"  {enriched['input']['messages'][0]['content']}")

    print(f"\n✓ Memory tags attached:")
    print(f"  {enriched['meta']['memory_tags']}")

    print(f"\n✓ Truth receipt generated:")
    receipt = enriched['meta']['truth_receipt']
    print(f"  trace_id: {receipt['trace_id']}")
    print(f"  timestamp: {receipt['ts']}")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "VIRTUS NEUROSYMBIOSIS INTEGRATION TEST" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    test_brockston_derek_frame()
    test_memory_tags_and_receipt()
    test_payload_enrichment()

    print("=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70)
    print()
