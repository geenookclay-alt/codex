from __future__ import annotations

from datetime import datetime, timedelta


def next_slot(slot_times: list[str]) -> str:
    now = datetime.now()
    for s in slot_times:
        h, m = map(int, s.split(":"))
        cand = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if cand > now:
            return cand.isoformat(timespec="minutes")
    first_h, first_m = map(int, slot_times[0].split(":"))
    tmr = (now + timedelta(days=1)).replace(hour=first_h, minute=first_m, second=0, microsecond=0)
    return tmr.isoformat(timespec="minutes")
