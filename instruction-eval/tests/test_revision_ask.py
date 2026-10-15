from collections.abc import Sequence
from datetime import timedelta

import pytest
import yaml

from instruction_eval.reader import ReaderRun, reader_fingerprint, revision_ask
from instruction_eval.records import Refusal, SeriesFolder, write_file
from test_reply_collect import COMMAND_READER, CONDITION_NAMES, CONVERSATION_TASKS, OPEN_MESSAGE, START, load, prepared_series, stamp, tree, write_yaml

COVERAGE = {"demands": {"d-one": [1]}, "sentences": {1: ["d-one"]}}
FINGERPRINT_OUTPUT = "model: gpt-5-mini\nbuild: b1\ntemperature: 0.7\n"
READER_SECONDS = 0.5


class StubReader:
    """A command reader that answers every call with the stdin it received, recording each call."""

    def __init__(self):
        self.calls: list[tuple[list[str], str, int]] = []

    def __call__(self, command: Sequence[str], stdin: str, timeout_seconds: int) -> ReaderRun:
        self.calls.append((list(command), stdin, timeout_seconds))
        started = START + timedelta(minutes=len(self.calls))
        return ReaderRun(started=started, seconds=READER_SECONDS, exit_code=0, stdout=stdin)


def stub_fingerprint(command: Sequence[str]) -> str:
    return FINGERPRINT_OUTPUT


def command_series(tmp_path) -> SeriesFolder:
    files = prepared_series(tmp_path, reader=COMMAND_READER)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    return files


def agent_series(tmp_path) -> SeriesFolder:
    files = prepared_series(tmp_path)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    return files


def expected_reads() -> set[str]:
    return {
        "series.yaml",
        "2-demands.yaml#demands",
        "3-tasks.yaml#tasks",
        "3-tasks.yaml#conversations",
        *(f"4-conditions.yaml#{key}" for key in ("controls", "aim", "placebo_source", "omissions")),
        "4-placebo-source.md",
        *(f"5-reader.yaml#{key}" for key in ("kind", "model", "command", "fingerprint", "sampling")),
        "7-gate.yaml#repeats",
        "r1/2-instruction.md",
        "r1/3-coverage.yaml#demands",
        "r1/3-coverage.yaml#sentences",
        *(f"r1/4-conditions/{condition}.md" for condition in CONDITION_NAMES),
    }


def test_a_command_reader_answers_every_missing_reply_serially_each_reply_recording_its_reader_run_and_fingerprint(tmp_path):
    files = command_series(tmp_path)
    reader = StubReader()

    printed = revision_ask(files, "r1", [], reader, stub_fingerprint)

    assert printed == ""
    assert len(reader.calls) == 4 * 2 * 2
    command, stdin, timeout_seconds = reader.calls[0]
    assert command == ["llm-reply", "--system-file", str(files.root / "r1/4-conditions/aim.md")]
    assert yaml.safe_load(stdin) == {"messages": [{"role": "user", "text": OPEN_MESSAGE}]}
    assert timeout_seconds == 600
    record = load(files, "r1/5-replies/aim/t-open/repeat-1.yaml")
    inputs = record.pop("inputs")
    assert set(inputs) == expected_reads()
    assert record == {
        "condition": "aim",
        "task": "t-open",
        "split": "open",
        "repeat": 1,
        "message": OPEN_MESSAGE,
        "text": stdin,
        "model": "gpt-5-mini",
        "reader_kind": "command",
        "started": stamp(START + timedelta(minutes=1)),
        "seconds": READER_SECONDS,
        "fingerprint_hash": reader_fingerprint(files, stub_fingerprint).fingerprint_hash,
        "cost": dict.fromkeys(("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "spent_input_tokens")),
    }
    second = load(files, "r1/5-replies/aim/t-open/repeat-2.yaml")
    assert "r1/5-replies/aim/t-open/repeat-1.yaml" in second["inputs"]


def test_each_conversation_turn_is_asked_with_the_repeats_earlier_turns_and_replies(tmp_path):
    files = prepared_series(tmp_path, CONVERSATION_TASKS, reader=COMMAND_READER)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    reader = StubReader()

    revision_ask(files, "r1", ["instruction"], reader, stub_fingerprint)

    stdins = [yaml.safe_load(stdin) for _, stdin, _ in reader.calls]
    first_turn = next(stdin for stdin in stdins if stdin["messages"][-1]["text"] == "Plan a trip.")
    second_turn = next(stdin for stdin in stdins if stdin["messages"][-1]["text"] == "Which week?")
    assert first_turn == {"messages": [{"role": "user", "text": "Plan a trip."}]}
    assert second_turn["messages"][:2] == [{"role": "user", "text": "Plan a trip."}, {"role": "assistant", "text": yaml.safe_dump(first_turn, allow_unicode=True)}]
    assert len(second_turn["messages"]) == 3
    assert len(reader.calls) == 2 * (2 + 2)


class FailingReader(StubReader):
    """A command reader that fails its second call with the given run."""

    def __init__(self, failure: ReaderRun):
        super().__init__()
        self.failure = failure

    def __call__(self, command: Sequence[str], stdin: str, timeout_seconds: int) -> ReaderRun:
        run = super().__call__(command, stdin, timeout_seconds)
        return self.failure if len(self.calls) == 2 else run


FAILURES = {
    "nonzero exit": (ReaderRun(START, 0.5, 3, "partial"), "exit 3"),
    "empty output": (ReaderRun(START, 0.5, 0, ""), "empty output"),
    "timeout": (ReaderRun(START, 600.0, None, "partial"), "over 600 seconds"),
    "overlong run": (ReaderRun(START, 601.0, 0, "late"), "over 600 seconds"),
}


@pytest.mark.parametrize("failure, cause", FAILURES.values(), ids=FAILURES.keys())
def test_a_failed_reader_run_stops_the_ask_writing_nothing_for_that_reply_and_a_rerun_resumes_at_it(tmp_path, failure, cause):
    files = command_series(tmp_path)

    with pytest.raises(Refusal, match=rf"^reader failed: r1/5-replies/aim/t-open/repeat-2\.yaml \({cause}\)$"):
        revision_ask(files, "r1", [], FailingReader(failure), stub_fingerprint)

    assert files.holds("r1/5-replies/aim/t-open/repeat-1.yaml")
    assert not files.holds("r1/5-replies/aim/t-open/repeat-2.yaml")
    resumed = StubReader()
    revision_ask(files, "r1", [], resumed, stub_fingerprint)
    assert len(resumed.calls) == 4 * 2 * 2 - 1
    assert files.holds("r1/5-replies/aim/t-open/repeat-2.yaml")


def test_a_reader_build_differing_from_the_r1_replies_so_far_refuses_while_reordered_keys_do_not(tmp_path):
    files = command_series(tmp_path)
    with pytest.raises(Refusal):
        revision_ask(files, "r1", [], FailingReader(FAILURES["nonzero exit"][0]), stub_fingerprint)

    with pytest.raises(Refusal, match=r"^reader fingerprint changed since r1/5-replies/aim/t-open/repeat-1\.yaml$"):
        revision_ask(files, "r1", [], StubReader(), lambda command: "model: gpt-5-mini\nbuild: b2\ntemperature: 0.7\n")

    reordered = StubReader()
    revision_ask(files, "r1", [], reordered, lambda command: "temperature: 0.7\nbuild: b1\nmodel: gpt-5-mini\n")
    assert len(reordered.calls) == 4 * 2 * 2 - 1


def forbidden_run(command: Sequence[str], stdin: str = "", timeout_seconds: int = 0) -> ReaderRun:
    raise AssertionError(f"ran {command}")


def test_an_agent_reader_prints_the_launch_list_of_the_named_conditions_and_runs_nothing(tmp_path):
    files = agent_series(tmp_path)
    before = tree(files.root)

    printed = revision_ask(files, "r1", ["instruction"], forbidden_run, forbidden_run)

    launches = yaml.safe_load(printed)["launches"]
    assert [(launch["agent_type"], launch["task"], launch["repeat"]) for launch in launches] == [
        ("ie-reader-r1-instruction", task, repeat) for task in ("t-open", "t-sealed") for repeat in (1, 2)
    ]
    assert tree(files.root) == before


def test_a_coverage_failing_its_check_refuses_the_ask_before_any_reader_runs(tmp_path):
    files = command_series(tmp_path)
    (files.root / "r1/3-coverage.yaml").write_text(yaml.safe_dump({"demands": {"d-one": [1]}, "sentences": {}}))

    with pytest.raises(Refusal):
        revision_ask(files, "r1", [], forbidden_run, forbidden_run)

    assert not (files.root / "r1/5-replies").exists()


@pytest.mark.parametrize(
    "series_kind, edited",
    [("command", "r1/4-conditions/aim.md"), ("agent", "r1/4-conditions/aim.md"), ("agent", ".claude/agents/ie-reader-r1-aim.md")],
)
def test_an_edited_condition_text_or_reader_definition_refuses_the_ask_before_any_reader_runs(tmp_path, series_kind, edited):
    files = command_series(tmp_path) if series_kind == "command" else agent_series(tmp_path)
    (files.root / edited).write_bytes(b"edited")

    with pytest.raises(Refusal, match=rf"^{edited.replace('.', '[.]')} differs from its recomputation$"):
        revision_ask(files, "r1", [], forbidden_run, forbidden_run)


@pytest.mark.parametrize("build_series", [command_series, agent_series], ids=["command", "agent"])
def test_a_collected_revision_is_never_asked_again_whatever_the_gate_repeats_now_say(tmp_path, build_series):
    files = build_series(tmp_path)
    write_file(files, "r1/7-collected.yaml", b"packets: {}\n")
    (files.root / "7-gate.yaml").write_text(yaml.safe_dump({"repeats": 3}))

    with pytest.raises(Refusal, match=r"^r1 already collected: no reply is added$"):
        revision_ask(files, "r1", [], forbidden_run, forbidden_run)

    assert not (files.root / "r1/5-replies").exists()
