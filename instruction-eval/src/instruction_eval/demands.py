"""The `demands check` command."""

from collections import Counter

from instruction_eval.records import DEMANDS_RECORD, Demand, Refusal, SeriesFolder, SeriesRecords


def demands_check(files: SeriesFolder) -> None:
    """Refuse a `2-demands.yaml` that breaks its schema or repeats a demand id."""
    _refuse_duplicate_ids(SeriesRecords(files).demands().demands)


def _refuse_duplicate_ids(demands: tuple[Demand, ...]) -> None:
    """Refuse the first demand id, in file order, that more than one demand holds."""
    counts = Counter(demand.id for demand in demands)
    repeated = next((demand_id for demand_id, count in counts.items() if count > 1), None)
    if repeated is not None:
        raise Refusal(f"duplicate demand id: {repeated} ({DEMANDS_RECORD})")
