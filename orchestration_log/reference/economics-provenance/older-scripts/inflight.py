"""Print one row per agent whose transcript changed within the window: model, tokens spent, the size of its context (what a resume after cache expiry reads again), age, name."""
import json, os, sys, time, glob

SUBAGENTS_DIRECTORY = '/Users/ryzhakar/.claudes/anarchy/projects/-Users-ryzhakar-pp-estafette/73b37e7c-4410-437c-b9d0-0650d0663d2c/subagents'
DEFAULT_WINDOW_MINUTES = 30
PROMPT_KINDS = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
TOKEN_KINDS = ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')


def usage_by_message(transcript_path):
    seen = {}
    with open(transcript_path, errors='replace') as lines:
        for line in lines:
            if '"usage"' not in line:
                continue
            try:
                message = json.loads(line).get('message') or {}
            except ValueError:
                continue
            usage = message.get('usage')
            if usage and message.get('model') != '<synthetic>':
                seen[message.get('id') or len(seen)] = (message.get('model', '?'), usage)
    return seen


def agent_name(transcript_path):
    meta_path = transcript_path[:-len('.jsonl')] + '.meta.json'
    try:
        meta = json.load(open(meta_path))
    except (OSError, ValueError):
        return ''
    return str(meta.get('name') or meta.get('description') or meta.get('agentType') or '')


def main():
    window_minutes = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_WINDOW_MINUTES
    now = time.time()
    rows = []
    for transcript_path in glob.glob(SUBAGENTS_DIRECTORY + '/agent-*.jsonl'):
        idle_minutes = (now - os.path.getmtime(transcript_path)) / 60
        if idle_minutes > window_minutes:
            continue
        messages = usage_by_message(transcript_path)
        totals = {kind: sum(int(usage.get(kind) or 0) for _, usage in messages.values()) for kind in TOKEN_KINDS}
        models = sorted({model for model, _ in messages.values()})
        fresh = totals['input_tokens'] + totals['output_tokens'] + totals['cache_creation_input_tokens']
        last_usage = list(messages.values())[-1][1] if messages else {}
        context = sum(int(last_usage.get(kind) or 0) for kind in PROMPT_KINDS)
        rows.append((idle_minutes, fresh, totals['cache_read_input_tokens'], context, ','.join(models), agent_name(transcript_path)[:60]))
    print('idle_min | fresh_k | cache_read_k | context_k | model | agent')
    for idle_minutes, fresh, cache_read, context, models, name in sorted(rows):
        print(f'{idle_minutes:7.0f} | {fresh // 1000:7d} | {cache_read // 1000:12d} | {context // 1000:9d} | {models} | {name}')
    print(f'context_k of all rows: {sum(row[3] for row in rows) // 1000}')


main()
