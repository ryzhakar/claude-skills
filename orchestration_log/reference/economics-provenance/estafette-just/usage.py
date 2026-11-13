"""Catch Claude Code's account limit figures from the status line input and report them, and list the agents in flight with their cost."""
import argparse
import json
import math
import os
import re
import shlex
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY_ROOT = SCRIPT_DIRECTORY.parent
PRICES_PATH = SCRIPT_DIRECTORY / 'usage-prices.json'
SCRATCH_ROOT_VARIABLE = 'ESTAFETTE_SCRATCH_ROOT'
SCRATCH_ROOT_BELOW_CHECKOUT = Path('docs') / 'orchestration_log' / 'recon'
CONFIG_DIRECTORY_VARIABLE = 'CLAUDE_CONFIG_DIR'
SESSION_ID_VARIABLE = 'CLAUDE_CODE_SESSION_ID'
DEFAULT_CONFIG_DIRECTORY_NAME = '.claude'
LIMITS_FILE_NAME = 'usage-limits.json'
CHECKPOINTS_FILE_NAME = 'usage-checkpoints.jsonl'
COLD_TURN_TALLY_FIELDS = ('cold_turns', 'cold_written', 'warm_turns', 'warm_written', 'all_written')
CHECKPOINT_KIND_FIELDS = {'fresh': 'input_tokens', 'cache_write': 'cache_creation_input_tokens', 'cache_read': 'cache_read_input_tokens', 'output': 'output_tokens'}
LIMIT_WINDOWS = ('five_hour', 'seven_day')
MODEL_EFFORT_SEPARATOR = ' '
LIMIT_FIELDS = ('used_percentage', 'resets_at')
GIT_FILE_POINTER_PREFIX = 'gitdir:'
LEVELS_FROM_WORKTREE_GIT_DIRECTORY_TO_CHECKOUT = 3
SECONDS_PER_MINUTE = 60
DEFAULT_WINDOW_MINUTES = 30
NAME_COLUMN_WIDTH = 60
TOKENS_PER_THOUSAND = 1000
TOKENS_PER_PRICE_UNIT = 1_000_000
LONG_PROMPT_TOKENS = 100_000
LONG_PROMPT_RATES_KEY = 'over_100k_prompt'
PROMPT_KINDS = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
TOKEN_KINDS = ('input_tokens', 'output_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
COST_KINDS = ('fresh', 'cache_write', 'cache_read', 'output')
UNKNOWN_MARK = '?'
FIVE_MINUTE_TTL = '5m'
ONE_HOUR_TTL = '1h'
SECONDS_BY_TTL = {FIVE_MINUTE_TTL: 5 * 60, ONE_HOUR_TTL: 60 * 60}
INTAKE_RATE_BY_TTL = {FIVE_MINUTE_TTL: 'cache_write_5m', ONE_HOUR_TTL: 'cache_write_1h'}
ONE_HOUR_WRITE_PATTERN = re.compile(r'"ephemeral_1h_input_tokens": ?[1-9]')
PARAMS_PATH = SCRIPT_DIRECTORY / 'usage-params.json'
EFFORTS = ('low', 'high', 'max')
ROLE_TTLS = {'agent': FIVE_MINUTE_TTL, 'lead': ONE_HOUR_TTL}
COMPONENT_LABELS = {'output': 'output', 'carry': 'carry', 'cold_start': 'cold start', 'first_intake': 'first intake'}
FULL_MODEL_BY_SHORT_NAME = {'haiku': 'claude-haiku-5-5', 'sonnet': 'claude-sonnet-5-5', 'opus': 'claude-opus-5-5', 'fable': 'claude-fable-5-2'}
DOLLARS_UNIT = 'usd'
LIMIT_WEIGHT_UNIT = 'percent'
MINUTES_UNIT = 'min'
SECONDS_UNIT = 'seconds'
CAPABILITY_UNIT = 'capability'
APPETITE_UNIT = 'thousand tokens'
UNIT_FORMATS = {DOLLARS_UNIT: '${:.2f}', LIMIT_WEIGHT_UNIT: '{:.4f}%', MINUTES_UNIT: '{:.1f}', SECONDS_UNIT: '{:.0f} s', CAPABILITY_UNIT: '{:.3f}', APPETITE_UNIT: '{:.1f}'}
LIMIT_WEIGHT_PREFIX = 'limit weight'
TTL_LABEL = 'TTL'
PUBLISHED_ATTEMPT_LABEL = f'{DOLLARS_UNIT} published attempt'
LINEUP_ROLE = 'agent'
HARNESS_EFFORT_NOTE_KEY = 'harness_recorded_effort_note'
LINEUP_HEADER = f'model | effort | {CAPABILITY_UNIT} | appetite_k | {DOLLARS_UNIT} attempt | {MINUTES_UNIT} | {DOLLARS_UNIT} per work unit'
MISSING_CAPABILITY = 'capability'
MISSING_APPETITE = 'appetite'
MISSING_GENERATION_SPEED = 'generation speed'


def login_directory(environment, home_directory):
    """The directory of the Claude Code login this process runs under."""
    configured = environment.get(CONFIG_DIRECTORY_VARIABLE)
    return Path(configured) if configured else home_directory / DEFAULT_CONFIG_DIRECTORY_NAME


def root_checkout(repository_root):
    """The root checkout of the repository, found through the pointer file a worktree holds in place of a git directory."""
    git_entry = repository_root / '.git'
    if not git_entry.is_file():
        return repository_root
    worktree_git_directory = Path(git_entry.read_text().removeprefix(GIT_FILE_POINTER_PREFIX).strip())
    return worktree_git_directory.parents[LEVELS_FROM_WORKTREE_GIT_DIRECTORY_TO_CHECKOUT - 1]


def scratch_directory(environment, repository_root):
    """The directory the usage files live in, the same whichever checkout runs."""
    scratch_root = environment.get(SCRATCH_ROOT_VARIABLE)
    return Path(scratch_root) if scratch_root else root_checkout(repository_root) / SCRATCH_ROOT_BELOW_CHECKOUT


def window_figures(window):
    """The used percentage and reset time of one window, or None when the window is absent."""
    if not isinstance(window, dict):
        return None
    return {field: window.get(field) for field in LIMIT_FIELDS}


def limit_figures(status_input):
    """Both windows' figures from a status line input, or None when the input carries no rate_limits."""
    rate_limits = status_input.get('rate_limits') if isinstance(status_input, dict) else None
    if not isinstance(rate_limits, dict):
        return None
    return {name: window_figures(rate_limits.get(name)) for name in LIMIT_WINDOWS}


def write_limits_file(path, figures, now):
    """Write the figures and the time of writing by a temporary file renamed over the final name."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f'{path.name}.tmp-{os.getpid()}')
    temporary_path.write_text(json.dumps({'written_at': int(now), 'rate_limits': figures}))
    os.replace(temporary_path, path)


def login_status_line_command(login):
    """The status line command the login already sets, or None when it sets none or sets this script."""
    try:
        settings = json.loads((login / 'settings.json').read_text())
    except (OSError, ValueError):
        return None
    command = (settings.get('statusLine') or {}).get('command')
    if not isinstance(command, str) or Path(__file__).name in command:
        return None
    return command


def own_status_line(figures):
    """One line naming the used percentage of each window, for a login with no status line command."""
    if figures is None:
        return 'usage: no rate limits'
    parts = [f'{name} {window["used_percentage"]}%' for name, window in figures.items() if window]
    return 'usage: ' + (' '.join(parts) or 'no rate limits')


def capture(raw_input, now, limits_path, login):
    """Write the limit figures from the status line input, then print the login's own status line unchanged."""
    figures = None
    try:
        figures = limit_figures(json.loads(raw_input))
        write_limits_file(limits_path, figures, now)
    except (OSError, ValueError) as failure:
        print(f'usage capture failed: {failure}', file=sys.stderr)
    command = login_status_line_command(login)
    if command is None:
        print(own_status_line(figures))
        return 0
    forwarded = subprocess.run(command, shell=True, input=raw_input, capture_output=True, check=False)
    sys.stdout.buffer.write(forwarded.stdout)
    sys.stdout.buffer.flush()
    return forwarded.returncode


def limits(max_age_minutes, now, limits_path):
    """Print the last written figures and their age; return 1 when the file is missing, unreadable or older than the bound."""
    if not limits_path.exists():
        print(f'no limit figures written: {limits_path} is missing', file=sys.stderr)
        return 1
    try:
        written = json.loads(limits_path.read_text())
        age_minutes = (now - written['written_at']) / SECONDS_PER_MINUTE
        windows = written['rate_limits']
    except (ValueError, KeyError, TypeError) as failure:
        print(f'limit figures unreadable: {limits_path}: {failure!r}', file=sys.stderr)
        return 1
    print(f'written {age_minutes:.1f} min ago')
    if windows is None:
        print('rate_limits absent from the status line input')
    for name, window in (windows or {}).items():
        print(f'{name}: ' + ('absent' if window is None else f'{window["used_percentage"]}% resets_at {window["resets_at"]}'))
    return 1 if age_minutes > max_age_minutes else 0


def own_session_transcript(login, checkout, environment):
    """The transcript of the session this process runs in, named by its environment; refuses when the variable is unset or names no transcript, never taking the newest file instead."""
    session_id = environment.get(SESSION_ID_VARIABLE)
    if not session_id:
        raise SystemExit(f'{SESSION_ID_VARIABLE} is unset: cannot tell which session transcript to read')
    project_directory = login / 'projects' / re.sub(r'[^A-Za-z0-9]', '-', str(checkout))
    transcript = project_directory / f'{session_id}.jsonl'
    if not transcript.is_file():
        raise SystemExit(f'no transcript of session {session_id} under {project_directory}')
    return transcript


def subagents_directory_of(session_transcript):
    """The directory holding the transcripts of the agents a session launched."""
    return session_transcript.with_suffix('') / 'subagents'


class Turn(NamedTuple):
    """One model message: its model, its effort, its usage, and the seconds since the previous model message, which is how long its cache sat unused (None for the first message)."""

    model: str
    effort: str
    usage: dict
    gap_seconds: float | None


def assistant_turns(transcript_path):
    """Each model message once per message id, in order of first appearance."""
    seen = {}
    previous_model_time = None
    with open(transcript_path, errors='replace') as lines:
        for line in lines:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            entry_time = datetime.fromisoformat(entry['timestamp']).timestamp() if entry.get('timestamp') else None
            message = entry.get('message') or {}
            usage = message.get('usage')
            if usage and message.get('model') != '<synthetic>':
                key = message.get('id') or len(seen)
                gap_seconds = seen[key].gap_seconds if key in seen else (None if previous_model_time is None or entry_time is None else entry_time - previous_model_time)
                seen[key] = Turn(message.get('model', '?'), str(entry.get('effort') or UNKNOWN_MARK), usage, gap_seconds)
                if entry_time is not None:
                    previous_model_time = entry_time
    return seen


def agent_name(transcript_path):
    """The agent's name from its meta file, empty when the file is unreadable."""
    meta_path = transcript_path.with_suffix('.meta.json')
    try:
        meta = json.loads(meta_path.read_text())
    except (OSError, ValueError):
        return ''
    return str(meta.get('name') or meta.get('description') or meta.get('agentType') or '')


def token_count(usage, kind):
    """The tokens of one kind in a usage record, zero when absent."""
    return int(usage.get(kind) or 0)


def rates_for(prices, model, prompt_tokens):
    """The price per million tokens of the model at this prompt length, or None when the model is not listed."""
    rates = prices['models'].get(prices['alias'].get(model, model))
    if rates is None:
        return None
    return rates.get(LONG_PROMPT_RATES_KEY, rates) if prompt_tokens > LONG_PROMPT_TOKENS else rates


def dollars_at_rates(rates, usage):
    """Dollars by kind for one usage record at the given rates per million tokens."""
    fresh = token_count(usage, 'input_tokens')
    cache_write = token_count(usage, 'cache_creation_input_tokens')
    write_one_hour = token_count(usage.get('cache_creation') or {}, 'ephemeral_1h_input_tokens')
    write_five_minutes = cache_write - write_one_hour
    dollars = {
        'fresh': fresh * rates['input'],
        'cache_write': write_five_minutes * rates['cache_write_5m'] + write_one_hour * rates['cache_write_1h'],
        'cache_read': token_count(usage, 'cache_read_input_tokens') * rates['cache_read'],
        'output': token_count(usage, 'output_tokens') * rates['output'],
    }
    return {kind: amount / TOKENS_PER_PRICE_UNIT for kind, amount in dollars.items()}


def message_cost(prices, model, usage):
    """Dollars by kind for one message, or None when the model is not listed."""
    prompt_tokens = sum(token_count(usage, kind) for kind in PROMPT_KINDS)
    rates = rates_for(prices, model, prompt_tokens)
    return None if rates is None else dollars_at_rates(rates, usage)


def cost_by_kind(prices, messages):
    """Dollars by kind summed over the messages, or None when any message's model is not listed."""
    costs = [message_cost(prices, turn.model, turn.usage) for turn in messages.values()]
    if None in costs:
        return None
    return {kind: sum(cost[kind] for cost in costs) for kind in COST_KINDS}


def transcript_ttl(transcript_path):
    """The TTL the transcript's cache writes are made at: 1h when any write is one-hour, else 5m."""
    with open(transcript_path, errors='replace') as lines:
        one_hour_written = any(ONE_HOUR_WRITE_PATTERN.search(line) for line in lines)
    return ONE_HOUR_TTL if one_hour_written else FIVE_MINUTE_TTL


def cold_start_cost(prices, messages, ttl):
    """Dollars to write the agent's last context into the cache again at the TTL's intake price, or None when the model is not listed."""
    if not messages:
        return 0.0
    last_turn = list(messages.values())[-1]
    context = sum(token_count(last_turn.usage, kind) for kind in PROMPT_KINDS)
    rates = rates_for(prices, last_turn.model, context)
    return None if rates is None else context * rates[INTAKE_RATE_BY_TTL[ttl]] / TOKENS_PER_PRICE_UNIT


def dollars_column(amount):
    """One dollar figure for a table column, or the unpriced mark."""
    return f'{UNKNOWN_MARK:>9}' if amount is None else f'{amount:9.2f}'


def inflight(window_minutes, subagents_directory, now, prices, lead_transcript):
    """Print one row per agent whose transcript changed within the window."""
    rows = []
    for transcript_path in subagents_directory.glob('agent-*.jsonl'):
        idle_minutes = (now - transcript_path.stat().st_mtime) / SECONDS_PER_MINUTE
        if idle_minutes > window_minutes:
            continue
        messages = assistant_turns(transcript_path)
        totals = {kind: sum(token_count(turn.usage, kind) for turn in messages.values()) for kind in TOKEN_KINDS}
        models = sorted({turn.model for turn in messages.values()})
        effort = list(messages.values())[-1].effort if messages else UNKNOWN_MARK
        fresh = totals['input_tokens'] + totals['output_tokens'] + totals['cache_creation_input_tokens']
        last_usage = list(messages.values())[-1].usage if messages else {}
        context = sum(token_count(last_usage, kind) for kind in PROMPT_KINDS)
        costs = cost_by_kind(prices, messages)
        ttl = transcript_ttl(transcript_path)
        rows.append((idle_minutes, fresh, totals['cache_read_input_tokens'], context, costs, cold_start_cost(prices, messages, ttl), ttl, ','.join(models), effort, agent_name(transcript_path)[:NAME_COLUMN_WIDTH]))
    print('idle_min | fresh_k | cache_read_k | context_k | usd_fresh | usd_write | usd_read | usd_out | usd_total | usd_cold_start | ttl | model | effort | agent')
    for idle_minutes, fresh, cache_read, context, costs, cold_start, ttl, models, effort, name in sorted(rows, key=lambda row: row[0]):
        by_kind = [dollars_column(None if costs is None else costs[kind]) for kind in COST_KINDS]
        total = dollars_column(None if costs is None else sum(costs.values()))
        print(f'{idle_minutes:7.0f} | {fresh // TOKENS_PER_THOUSAND:7d} | {cache_read // TOKENS_PER_THOUSAND:12d} | {context // TOKENS_PER_THOUSAND:9d} | ' + ' | '.join(by_kind) + f' | {total} | {dollars_column(cold_start)} | {ttl:>4} | {models} | {effort} | {name}')
    print(f'context_k of all rows: {sum(row[3] for row in rows) // TOKENS_PER_THOUSAND}')
    if lead_transcript is not None:
        print(f'lead transcript TTL: {transcript_ttl(lead_transcript)}')
    return 0


def token_totals_by_model_and_effort(transcript_paths):
    """Tokens by model with effort and by kind over the transcripts, each message counted once."""
    totals = {}
    for transcript_path in transcript_paths:
        for turn in assistant_turns(transcript_path).values():
            by_kind = totals.setdefault(f'{turn.model}{MODEL_EFFORT_SEPARATOR}{turn.effort}', dict.fromkeys(CHECKPOINT_KIND_FIELDS, 0))
            for kind, field in CHECKPOINT_KIND_FIELDS.items():
                by_kind[kind] += token_count(turn.usage, field)
    return totals


def checkpoint(label, now, limits_path, checkpoints_path, session_transcript):
    """Append one line holding the label, the limit figures last written and the session's tokens so far by model and kind."""
    limits_written = json.loads(limits_path.read_text()) if limits_path.exists() else None
    transcripts = [session_transcript, *subagents_directory_of(session_transcript).glob('agent-*.jsonl')]
    line = {'at': int(now), 'label': label, 'limits': limits_written, 'tokens': token_totals_by_model_and_effort(transcripts)}
    checkpoints_path.parent.mkdir(parents=True, exist_ok=True)
    with checkpoints_path.open('a') as checkpoints_file:
        checkpoints_file.write(json.dumps(line) + '\n')
    print(f'checkpoint {label!r} appended to {checkpoints_path}')
    return 0


def used_percentage(line, window):
    """The used percentage of a window in a checkpoint line, or None when the line holds none."""
    rate_limits = (line['limits'] or {}).get('rate_limits') or {}
    return (rate_limits.get(window) or {}).get('used_percentage')


def points_moved(window, before, after):
    """The change of a window's used percentage between two lines, or None when either lacks it."""
    first, second = used_percentage(before, window), used_percentage(after, window)
    return None if first is None or second is None else second - first


def percentage_points_text(window, before, after):
    """The change of a window's used percentage between two lines, or the unknown mark when either lacks it."""
    moved = points_moved(window, before, after)
    return UNKNOWN_MARK if moved is None else f'{moved:+.1f}'


def checkpoints(checkpoints_path):
    """Print the checkpoints as a table, each line after the first with its difference to the line before."""
    if not checkpoints_path.exists():
        print(f'no checkpoints written: {checkpoints_path} is missing', file=sys.stderr)
        return 1
    lines = [json.loads(text) for text in checkpoints_path.read_text().splitlines()]
    print('at | label | five_hour% | seven_day% | d_five_hour_points | d_seven_day_points')
    for index, line in enumerate(lines):
        shown = [str(used_percentage(line, window)) for window in LIMIT_WINDOWS]
        deltas = [UNKNOWN_MARK] * len(LIMIT_WINDOWS) if index == 0 else [percentage_points_text(window, lines[index - 1], line) for window in LIMIT_WINDOWS]
        print(' | '.join([str(line['at']), line['label'], *shown, *deltas]))
        if index == 0:
            continue
        before = lines[index - 1]['tokens']
        for model in sorted(set(before) | set(line['tokens'])):
            changes = {kind: line['tokens'].get(model, {}).get(kind, 0) - before.get(model, {}).get(kind, 0) for kind in CHECKPOINT_KIND_FIELDS}
            print(f'    {model}: ' + ' '.join(f'{kind} {change:+d}' for kind, change in changes.items()))
    return 0


def coldturns(session_transcript):
    """Print, per source, model with effort and TTL, the turns after a gap past the TTL and those within it, with their cache-write tokens and share."""
    agent_transcripts = list(subagents_directory_of(session_transcript).glob('agent-*.jsonl'))
    tallies = {}
    for source, transcript_paths in (('lead', [session_transcript]), ('agents', agent_transcripts)):
        for transcript_path in transcript_paths:
            ttl = transcript_ttl(transcript_path)
            for turn in assistant_turns(transcript_path).values():
                tally = tallies.setdefault((source, turn.model, turn.effort, ttl), dict.fromkeys(COLD_TURN_TALLY_FIELDS, 0))
                written = token_count(turn.usage, 'cache_creation_input_tokens')
                tally['all_written'] += written
                if turn.gap_seconds is None:
                    continue
                phase = 'cold' if turn.gap_seconds > SECONDS_BY_TTL[ttl] else 'warm'
                tally[f'{phase}_turns'] += 1
                tally[f'{phase}_written'] += written
    print('source | model | effort | ttl | cold_turns | cold_write_k | cold_share | warm_turns | warm_write_k | warm_share | all_write_k')
    for (source, model, effort, ttl), tally in sorted(tallies.items()):
        shares = [UNKNOWN_MARK if not tally['all_written'] else f'{100 * tally[f"{phase}_written"] / tally["all_written"]:.1f}%' for phase in ('cold', 'warm')]
        print(f'{source} | {model} | {effort} | {ttl} | {tally["cold_turns"]} | {tally["cold_written"] // TOKENS_PER_THOUSAND} | {shares[0]} | {tally["warm_turns"]} | {tally["warm_written"] // TOKENS_PER_THOUSAND} | {shares[1]} | {tally["all_written"] // TOKENS_PER_THOUSAND}')
    return 0


class Refusal(Exception):
    """An input the calculator refuses, whose message is printed alone."""


class Attempt(NamedTuple):
    """One attempt's inputs: model, effort, thousands of context carried, steps, cold starts, tool time in minutes, who runs it and its appetite in thousands of tokens."""

    model: str
    effort: str
    context_k: float
    steps: int
    cold_starts: int
    tool_time_min: float
    role: str
    appetite_k: float


class Line(NamedTuple):
    """One row of a calculator table: its label, its figure (None when unknown) and its unit."""

    label: str
    figure: float | None
    unit: str


def required_value(entry, description, remedy=''):
    """The value of a parameter entry, or a refusal naming the entry and the file when the value is null."""
    if entry['value'] is None:
        raise Refusal(f'{description} is null in {PARAMS_PATH.name}{remedy}')
    return entry['value']


def full_model_name(name):
    """The full model id of a short name, or the name itself when it is no short name."""
    return FULL_MODEL_BY_SHORT_NAME.get(name, name)


def checked_model_and_effort(prices, model, effort):
    """Refuse a model the price file does not list or an effort outside the three, naming the accepted set."""
    if model not in prices['models']:
        raise Refusal(f'unknown model {model!r}; accepted: {", ".join([*FULL_MODEL_BY_SHORT_NAME, *prices["models"]])}')
    if effort not in EFFORTS:
        raise Refusal(f'unknown effort {effort!r}; accepted: {", ".join(EFFORTS)}')


def attempt_from(prices, parameters, parsed):
    """The attempt a parsed command line describes, refused when model or effort is unknown or the appetite is null and not passed."""
    checked_model_and_effort(prices, parsed.model, parsed.effort)
    appetite_k = parsed.appetite_k
    if appetite_k is None:
        entry = parameters['per_attempt'][parsed.model][parsed.effort]['appetite_k']
        appetite_k = required_value(entry, f'appetite_k of {parsed.model} {parsed.effort}', ': pass --appetite-k')
    return Attempt(parsed.model, parsed.effort, parsed.context_k, parsed.steps, parsed.cold_starts, parsed.tool_time_min, parsed.role, appetite_k)


def component_tokens(attempt):
    """Tokens of each cost component: the output, the carry over the steps, the intake of the cold starts and the first intake of the context held at launch."""
    context = attempt.context_k * TOKENS_PER_THOUSAND
    return {'output': attempt.appetite_k * TOKENS_PER_THOUSAND, 'carry': context * attempt.steps, 'cold_start': context * attempt.cold_starts, 'first_intake': context}


def component_prices(prices, attempt):
    """Dollars per million tokens of each cost component, the intake price taken at the TTL of the attempt's role."""
    rates = rates_for(prices, attempt.model, attempt.context_k * TOKENS_PER_THOUSAND)
    intake_rate = rates[INTAKE_RATE_BY_TTL[ROLE_TTLS[attempt.role]]]
    return {'output': rates['output'], 'carry': rates['cache_read'], 'cold_start': intake_rate, 'first_intake': intake_rate}


def component_weights(weights):
    """The limit weight of each cost component, taken from the weights the parameter file holds for a model."""
    return {'output': weights['output'], 'carry': weights['carry'], 'cold_start': weights['intake_5m'], 'first_intake': weights['intake_5m']}


def tokens_at_rates(tokens, rates_per_million_tokens):
    """Each component's tokens times its rate per million tokens."""
    return {kind: tokens[kind] * rates_per_million_tokens[kind] / TOKENS_PER_PRICE_UNIT for kind in tokens}


def total_label(prefix):
    """The label of the line that sums a prefix's lines."""
    return f'{prefix} total'


def component_lines(prefix, unit, by_component):
    """The three components' lines and their total, every figure None when the figures are unknown."""
    lines = [Line(f'{prefix} {label}', None if by_component is None else by_component[kind], unit) for kind, label in COMPONENT_LABELS.items()]
    return [*lines, Line(total_label(prefix), None if by_component is None else sum(by_component.values()), unit)]


def generation_speed_of(parameters, attempt):
    """The generation speed of the attempt's variant, or of its model where no figure covers the variant, refused when both are null."""
    variant_generation_speed = parameters['per_attempt'][attempt.model][attempt.effort]['generation_speed_tokens_per_second']
    generation_speed = variant_generation_speed if variant_generation_speed['value'] is not None else parameters['generation_speed_tokens_per_second'][attempt.model]
    return required_value(generation_speed, f'generation speed of {attempt.model} {attempt.effort}')


def minute_lines(parameters, attempt):
    """Minutes of generation time, of tool time and their sum, refused when the generation speed is null."""
    generation_speed = generation_speed_of(parameters, attempt)
    generation_time = attempt.appetite_k * TOKENS_PER_THOUSAND / generation_speed / SECONDS_PER_MINUTE
    return [
        Line(f'{MINUTES_UNIT} generation time', generation_time, MINUTES_UNIT),
        Line(f'{MINUTES_UNIT} tool time', attempt.tool_time_min, MINUTES_UNIT),
        Line(total_label(MINUTES_UNIT), generation_time + attempt.tool_time_min, MINUTES_UNIT),
    ]


def attempt_lines(prices, parameters, attempt):
    """The TTL, dollars, limit weight and minutes of one attempt as table lines."""
    tokens = component_tokens(attempt)
    weights = parameters['limit_weight_percent_per_million_tokens'][attempt.model]['value']
    published_attempt_dollars = parameters['per_attempt'][attempt.model][attempt.effort]['attempt_dollars']['value']
    return [
        Line(TTL_LABEL, parameters['ttl_seconds'][attempt.role]['value'], SECONDS_UNIT),
        *component_lines(DOLLARS_UNIT, DOLLARS_UNIT, tokens_at_rates(tokens, component_prices(prices, attempt))),
        Line(PUBLISHED_ATTEMPT_LABEL, published_attempt_dollars, DOLLARS_UNIT),
        *component_lines(LIMIT_WEIGHT_PREFIX, LIMIT_WEIGHT_UNIT, None if weights is None else tokens_at_rates(tokens, component_weights(weights))),
        *minute_lines(parameters, attempt),
    ]


def figure_in_unit(figure, unit):
    """A figure in its unit's format, or the unknown mark."""
    return UNKNOWN_MARK if figure is None else UNIT_FORMATS[unit].format(figure)


def figure_text(line):
    """A line's figure in its unit's format, or the unknown mark."""
    return figure_in_unit(line.figure, line.unit)


def print_lines(lines):
    """Print each line as its label and its figure."""
    for line in lines:
        print(f'{line.label} | {figure_text(line)}')


def add_attempt_arguments(parser):
    """Add the arguments that describe one attempt to a parser."""
    parser.add_argument('model', type=full_model_name)
    parser.add_argument('effort')
    parser.add_argument('context_k', type=float)
    parser.add_argument('steps', type=int)
    parser.add_argument('cold_starts', type=int)
    parser.add_argument('tool_time_min', type=float)
    parser.add_argument('role', choices=tuple(ROLE_TTLS))
    parser.add_argument('--appetite-k', type=float)


def attempt_command(parsed, prices, parameters):
    """Print the table of one attempt."""
    print_lines(attempt_lines(prices, parameters, attempt_from(prices, parameters, parsed)))
    return 0


def figure_of(lines, label):
    """The figure of the line with this label."""
    return next(line.figure for line in lines if line.label == label)


def checked_capability(capability, description):
    """Refuse a capability outside 0 to 1 with 0 excluded, naming what it belongs to."""
    if not 0 < capability <= 1:
        raise Refusal(f'capability {capability} of {description} is outside 0 to 1, 0 excluded')
    return capability


def capability_from(parameters, parsed):
    """The capability a parsed command line gives or the parameter file holds, refused when null and not passed or outside 0 to 1 with 0 excluded."""
    capability = parsed.capability
    if capability is None:
        capability = required_value(parameters['per_attempt'][parsed.model][parsed.effort]['capability'], f'capability of {parsed.model} {parsed.effort}', ': pass --capability')
    return checked_capability(capability, f'{parsed.model} {parsed.effort}')


def work_unit_figure(attempt, check, rework, capability):
    """The attempt and the check, plus the rework on the share of attempts that fail, spread over the attempts that come back right."""
    return (attempt + check + (1 - capability) * rework) / capability


def unit_command(parsed, prices, parameters):
    """Print the attempt and the dollars and minutes per work unit it rests on."""
    attempt = attempt_from(prices, parameters, parsed)
    capability = capability_from(parameters, parsed)
    lines = attempt_lines(prices, parameters, attempt)
    per_unit = [
        Line(f'{DOLLARS_UNIT} per work unit', work_unit_figure(figure_of(lines, total_label(DOLLARS_UNIT)), parsed.check_usd, parsed.rework_usd, capability), DOLLARS_UNIT),
        Line(f'{MINUTES_UNIT} per work unit', work_unit_figure(figure_of(lines, total_label(MINUTES_UNIT)), parsed.check_min, parsed.rework_min, capability), MINUTES_UNIT),
    ]
    print_lines([*lines, *per_unit])
    return 0


def ratio_text(first, second):
    """The second figure over the first, or the unknown mark when either is unknown or the first is zero."""
    if first is None or second is None or first == 0:
        return UNKNOWN_MARK
    return f'{second / first:.2f}x'


def compare_command(parsed, prices, parameters):
    """Print two attempts side by side with the ratio of each line."""
    attempt_parser = argparse.ArgumentParser(prog='attempt')
    add_attempt_arguments(attempt_parser)
    both = [attempt_lines(prices, parameters, attempt_from(prices, parameters, attempt_parser.parse_args(shlex.split(text)))) for text in (parsed.first, parsed.second)]
    print('line | first | second | second over first')
    for first, second in zip(*both):
        print(f'{first.label} | {figure_text(first)} | {figure_text(second)} | {ratio_text(first.figure, second.figure)}')
    return 0


class LineupRequest(NamedTuple):
    """The task a lineup prices: an attempt's context, steps, cold starts and tool time, the check and rework dollars, and the factor on every capability."""

    context_k: float
    steps: int
    cold_starts: int
    tool_time_min: float
    check_usd: float
    rework_usd: float
    capability_scale: float


class LineupRow(NamedTuple):
    """One variant of the lineup: its figures, None where unknown, and the names of the figures it lacks."""

    model: str
    effort: str
    capability: float | None
    appetite_k: float | None
    attempt_usd: float | None
    minutes: float | None
    work_unit_usd: float | None
    missing: tuple[str, ...]


def missing_fields(parameters, model, effort):
    """The names of the figures no source gives for a variant: its capability, its appetite and its generation speed."""
    variant = parameters['per_attempt'][model][effort]
    model_speed = parameters['generation_speed_tokens_per_second'][model]
    lacking = {
        MISSING_CAPABILITY: variant['capability']['value'] is None,
        MISSING_APPETITE: variant['appetite_k']['value'] is None,
        MISSING_GENERATION_SPEED: variant['generation_speed_tokens_per_second']['value'] is None and model_speed['value'] is None,
    }
    return tuple(name for name, is_lacking in lacking.items() if is_lacking)


def lineup_row(prices, parameters, request, short_name, model, effort):
    """The row of one variant: attempt dollars and minutes where its appetite and generation speed are known, dollars per work unit where its capability is too."""
    variant = parameters['per_attempt'][model][effort]
    missing = missing_fields(parameters, model, effort)
    capability = None if MISSING_CAPABILITY in missing else checked_capability(variant['capability']['value'] * request.capability_scale, f'{short_name} {effort} scaled by {request.capability_scale}')
    appetite_k = variant['appetite_k']['value']
    if MISSING_APPETITE in missing or MISSING_GENERATION_SPEED in missing:
        return LineupRow(short_name, effort, capability, appetite_k, None, None, None, missing)
    lines = attempt_lines(prices, parameters, Attempt(model, effort, request.context_k, request.steps, request.cold_starts, request.tool_time_min, LINEUP_ROLE, appetite_k))
    attempt_usd = figure_of(lines, total_label(DOLLARS_UNIT))
    work_unit_usd = None if capability is None else work_unit_figure(attempt_usd, request.check_usd, request.rework_usd, capability)
    return LineupRow(short_name, effort, capability, appetite_k, attempt_usd, figure_of(lines, total_label(MINUTES_UNIT)), work_unit_usd, missing)


def lineup_sort_key(row):
    """The dollars per work unit of a row, infinite where unknown so that such rows come last."""
    return math.inf if row.work_unit_usd is None else row.work_unit_usd


def lineup_row_text(row):
    """A row's cells in their units, with the names of the missing figures after them."""
    cells = [
        row.model,
        row.effort,
        figure_in_unit(row.capability, CAPABILITY_UNIT),
        figure_in_unit(row.appetite_k, APPETITE_UNIT),
        figure_in_unit(row.attempt_usd, DOLLARS_UNIT),
        figure_in_unit(row.minutes, MINUTES_UNIT),
        figure_in_unit(row.work_unit_usd, DOLLARS_UNIT),
    ]
    return ' | '.join(cells) + (f' | missing: {", ".join(row.missing)}' if row.missing else '')


def lineup_command(parsed, prices, parameters):
    """Print one row per newest model and effort, the cheapest work unit first, then the note on the effort the harness records."""
    request = LineupRequest(parsed.context_k, parsed.steps, parsed.cold_starts, parsed.tool_time_min, parsed.check_usd, parsed.rework_usd, parsed.capability_scale)
    rows = [lineup_row(prices, parameters, request, short_name, model, effort) for short_name, model in FULL_MODEL_BY_SHORT_NAME.items() for effort in EFFORTS]
    print(LINEUP_HEADER)
    for row in sorted(rows, key=lineup_sort_key):
        print(lineup_row_text(row))
    note = parameters[HARNESS_EFFORT_NOTE_KEY]
    print(f'note: {note["value"]} ({note["source"]})')
    return 0


CALCULATOR_COMMANDS = {'attempt': attempt_command, 'unit': unit_command, 'compare': compare_command, 'lineup': lineup_command}


def run_refusing(command, *command_arguments):
    """Run a calculator command and return its exit code, printing a refusal alone on standard error and returning 1."""
    try:
        return command(*command_arguments)
    except Refusal as refusal:
        print(refusal, file=sys.stderr)
        return 1


def is_keyed_by_model_and_effort(line):
    """Whether every key of the line's tokens names a model and an effort, which the older format's model-only keys do not."""
    return bool(line['tokens']) and all(MODEL_EFFORT_SEPARATOR in key for key in line['tokens'])


def interval_cost(prices, before, after):
    """Dollars by kind spent between two checkpoint lines at list price, or None when a model is not listed."""
    totals = dict.fromkeys(COST_KINDS, 0.0)
    for key, tokens in after['tokens'].items():
        rates = rates_for(prices, key.rsplit(MODEL_EFFORT_SEPARATOR, 1)[0], 0)
        if rates is None:
            return None
        earlier = before['tokens'].get(key, {})
        usage = {field: tokens.get(kind, 0) - earlier.get(kind, 0) for kind, field in CHECKPOINT_KIND_FIELDS.items()}
        for kind, dollars in dollars_at_rates(rates, usage).items():
            totals[kind] += dollars
    return totals


def dollars_per_point(dollars, moved):
    """Dollars spent over the points a window rose, or None when either is unknown or the window did not rise."""
    if dollars is None or moved is None or moved <= 0:
        return None
    return dollars / moved


def median_text(values):
    """The median of the values to cents, or the unknown mark when there are none."""
    return UNKNOWN_MARK if not values else f'{statistics.median(values):.2f}'


def calibrate(checkpoints_path, prices):
    """Print the dollars spent between consecutive model-and-effort checkpoint lines against the limit points moved, with the median dollars per point; refuse with fewer than two such lines."""
    lines = [json.loads(text) for text in checkpoints_path.read_text().splitlines()] if checkpoints_path.exists() else []
    usable = [line for line in lines if is_keyed_by_model_and_effort(line)]
    skipped = len(lines) - len(usable)
    if len(usable) < 2:
        raise Refusal(f'calibrate needs two checkpoint lines keyed by model and effort; {checkpoints_path} holds {len(usable)} ({skipped} of the older format skipped)')
    per_point = {window: [] for window in LIMIT_WINDOWS}
    print(' | '.join(['from', 'to', *[f'usd_{kind}' for kind in COST_KINDS], 'usd_total', *[f'd_{window}_points' for window in LIMIT_WINDOWS], *[f'usd_per_{window}_point' for window in LIMIT_WINDOWS]]))
    for before, after in zip(usable, usable[1:]):
        costs = interval_cost(prices, before, after)
        total = None if costs is None else sum(costs.values())
        rates = {window: dollars_per_point(total, points_moved(window, before, after)) for window in LIMIT_WINDOWS}
        for window, rate in rates.items():
            if rate is not None:
                per_point[window].append(rate)
        print(' | '.join([before['label'], after['label'], *[dollars_column(None if costs is None else costs[kind]) for kind in COST_KINDS], dollars_column(total), *[percentage_points_text(window, before, after) for window in LIMIT_WINDOWS], *[dollars_column(rates[window]) for window in LIMIT_WINDOWS]]))
    print(f'lines of the older format skipped: {skipped}')
    for window, values in per_point.items():
        print(f'median usd per {window} point: {median_text(values)} over {len(values)} intervals')
    return 0


def main(arguments, standard_input, now, environment, home_directory):
    """Run the subcommand named in the arguments and return the process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest='subcommand', required=True)
    subcommands.add_parser('capture', help='status line command: write the limit figures from standard input, print the login status line')
    limits_parser = subcommands.add_parser('limits', help='print the last written limit figures; exit 1 when missing or too old')
    limits_parser.add_argument('max_age_minutes', type=float)
    inflight_parser = subcommands.add_parser('inflight', help='print the agents whose transcript changed within the window')
    inflight_parser.add_argument('window_minutes', type=int, nargs='?', default=DEFAULT_WINDOW_MINUTES)
    inflight_parser.add_argument('subagents_directory', nargs='?', default='')
    checkpoint_parser = subcommands.add_parser('checkpoint', help='append the limit figures and the session token totals by model and kind to the checkpoints file')
    checkpoint_parser.add_argument('label')
    subcommands.add_parser('checkpoints', help='print the checkpoints with the differences between lines')
    subcommands.add_parser('calibrate', help='print the dollars per limit point between consecutive model-and-effort checkpoint lines and their median')
    subcommands.add_parser('coldturns', help='print the turns after a gap past the TTL and the share of cache-write tokens they carry')
    attempt_parser = subcommands.add_parser('attempt', help='print the dollars, limit weight and minutes of one attempt')
    add_attempt_arguments(attempt_parser)
    unit_parser = subcommands.add_parser('unit', help='print one attempt and the dollars and minutes per work unit')
    add_attempt_arguments(unit_parser)
    unit_parser.add_argument('check_usd', type=float)
    unit_parser.add_argument('check_min', type=float)
    unit_parser.add_argument('rework_usd', type=float)
    unit_parser.add_argument('rework_min', type=float)
    unit_parser.add_argument('--capability', type=float)
    compare_parser = subcommands.add_parser('compare', help='print two attempts side by side with the ratio of each line')
    compare_parser.add_argument('first')
    compare_parser.add_argument('second')
    lineup_parser = subcommands.add_parser('lineup', help='print one row per newest model and effort with its capability, appetite, attempt dollars, minutes and dollars per work unit, cheapest work unit first')
    lineup_parser.add_argument('context_k', type=float)
    lineup_parser.add_argument('steps', type=int)
    lineup_parser.add_argument('cold_starts', type=int)
    lineup_parser.add_argument('tool_time_min', type=float)
    lineup_parser.add_argument('check_usd', type=float)
    lineup_parser.add_argument('rework_usd', type=float)
    lineup_parser.add_argument('--capability-scale', type=float, default=1.0)
    parsed = parser.parse_args(arguments)
    if parsed.subcommand in CALCULATOR_COMMANDS:
        return run_refusing(CALCULATOR_COMMANDS[parsed.subcommand], parsed, json.loads(PRICES_PATH.read_text()), json.loads(PARAMS_PATH.read_text()))
    login = login_directory(environment, home_directory)
    directory = scratch_directory(environment, REPOSITORY_ROOT)
    limits_path = directory / LIMITS_FILE_NAME
    checkpoints_path = directory / CHECKPOINTS_FILE_NAME
    if parsed.subcommand == 'capture':
        return capture(standard_input.buffer.read(), now, limits_path, login)
    if parsed.subcommand == 'limits':
        return limits(parsed.max_age_minutes, now, limits_path)
    if parsed.subcommand == 'checkpoint':
        return checkpoint(parsed.label, now, limits_path, checkpoints_path, own_session_transcript(login, root_checkout(REPOSITORY_ROOT), environment))
    if parsed.subcommand == 'checkpoints':
        return checkpoints(checkpoints_path)
    if parsed.subcommand == 'calibrate':
        return run_refusing(calibrate, checkpoints_path, json.loads(PRICES_PATH.read_text()))
    if parsed.subcommand == 'coldturns':
        return coldturns(own_session_transcript(login, root_checkout(REPOSITORY_ROOT), environment))
    lead_transcript = None if parsed.subagents_directory else own_session_transcript(login, root_checkout(REPOSITORY_ROOT), environment)
    subagents_directory = Path(parsed.subagents_directory) if parsed.subagents_directory else subagents_directory_of(lead_transcript)
    return inflight(parsed.window_minutes, subagents_directory, now, json.loads(PRICES_PATH.read_text()), lead_transcript)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:], sys.stdin, time.time(), os.environ, Path.home()))
