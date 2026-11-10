"""xG analysis, step 1: download StatsBomb open data for 2015/16 and extract open-play shots.

Source: https://github.com/statsbomb/open-data, pinned to one commit so the download is reproducible.

Writes
  Attachments/statsbomb-open-data-2015-16/
      raw/matches/<competition_id>_<season_id>.json.gz   original bytes, gzip-compressed
      raw/events/<match_id>.json.gz                      original bytes, gzip-compressed
      doc/  LICENSE.pdf, README.md                       StatsBomb documentation and terms
      SHA256SUMS_raw.txt   SHA-256 of the *uncompressed* original bytes of every raw file
  Code/outputs/xg/
      shots_open_play.csv          one row per open-play shot (shot.type == "Open Play")
      freeze_frames_open_play.csv  one row per player in each open-play shot's freeze frame
      download_log.txt             counts of every shot type, kept and excluded

Run:  cd Code && uv run python xg/01_download_shots.py
No randomness. Network access to raw.githubusercontent.com is needed the first time only;
afterwards the cached raw files are read.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

COMMIT = "4b73468fc5b0f1950f9f66fada70ad3a4f9327cb"  # statsbomb/open-data HEAD on 9 November 2026
BASE = f"https://raw.githubusercontent.com/statsbomb/open-data/{COMMIT}"

LEAGUES = {  # code -> (competition_id, season_id); season 2015/16 is season_id 27
    "ENG": (2, 27),
    "ESP": (11, 27),
    "ITA": (12, 27),
    "FRA": (7, 27),
    "GER": (9, 27),
}
KEEP_SHOT_TYPE = "Open Play"  # excludes Penalty, Free Kick, Corner, Kick Off
EXCLUDE_KEY_PASS_TYPES = {"Corner", "Free Kick", "Throw-in", "Goal Kick", "Kick Off"}  # also excludes open-play shots whose key pass (assist) is a restart

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "Attachments", "statsbomb-open-data-2015-16")
RAW = os.path.join(DATA, "raw")
OUT = os.path.join(ROOT, "Code", "outputs", "xg")


def fetch(url: str, tries: int = 5) -> bytes:
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def cached(rel: str, url: str) -> bytes:
    """Return the original bytes of a source file, downloading and storing them gzip-compressed once."""
    path = os.path.join(RAW, rel + ".gz")
    if os.path.exists(path):
        with gzip.open(path, "rb") as f:
            return f.read()
    data = fetch(url)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with gzip.open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)
    return data


def name(d, key):
    v = d.get(key)
    return v.get("name") if isinstance(v, dict) else None


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(DATA, "doc"), exist_ok=True)
    for f in ["LICENSE.pdf", "README.md", "doc/Open Data Events v4.0.0.pdf", "doc/Open Data Matches v3.0.0.pdf"]:
        dest = os.path.join(DATA, "doc", os.path.basename(f))
        if not os.path.exists(dest):
            with open(dest, "wb") as fh:
                fh.write(fetch(f"{BASE}/{urllib.parse.quote(f)}"))

    sums: dict[str, str] = {}
    games = []  # (league, match dict)
    for lg, (cid, sid) in LEAGUES.items():
        rel = f"matches/{cid}_{sid}.json"
        b = cached(rel, f"{BASE}/data/matches/{cid}/{sid}.json")
        sums[rel] = hashlib.sha256(b).hexdigest()
        games += [(lg, m) for m in json.loads(b)]

    def get_events(mid):
        rel = f"events/{mid}.json"
        return rel, cached(rel, f"{BASE}/data/events/{mid}.json")

    shot_rows, ff_rows = [], []
    type_counts = Counter()
    type_by_league = Counter()
    keypass_counts = Counter()  # key-pass type of open-play shots
    excl_by_league = Counter()
    corner_in_possession = 0  # kept shots whose possession contains an earlier corner (reported only)
    by_match = {m["match_id"]: (lg, m) for lg, m in games}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, (rel, b) in enumerate(ex.map(get_events, by_match), 1):
            sums[rel] = hashlib.sha256(b).hexdigest()
            mid = int(os.path.basename(rel).split(".")[0])
            lg, m = by_match[mid]
            evs = json.loads(b)
            pass_type = {e["id"]: (name(e.get("pass", {}), "type") or "Regular") for e in evs if name(e, "type") == "Pass"}
            corner_idx = {}  # (period, possession) -> index of first corner
            for e in evs:
                if name(e, "type") == "Pass" and name(e["pass"], "type") == "Corner":
                    corner_idx.setdefault((e["period"], e["possession"]), e["index"])
            for e in evs:
                if name(e, "type") != "Shot":
                    continue
                s = e["shot"]
                st = name(s, "type")
                type_counts[st] += 1
                type_by_league[(lg, st)] += 1
                if st != KEEP_SHOT_TYPE:
                    continue
                kp = s.get("key_pass_id")
                kpt = pass_type.get(kp) if kp else None
                keypass_counts[kpt or "(no key pass)"] += 1
                if kpt in EXCLUDE_KEY_PASS_TYPES:
                    excl_by_league[(lg, kpt)] += 1
                    continue
                ci = corner_idx.get((e["period"], e["possession"]))
                if ci is not None and ci < e["index"]:
                    corner_in_possession += 1
                loc = e.get("location") or [None, None]
                end = (s.get("end_location") or []) + [None, None, None]
                shot_rows.append({
                    "shot_id": e["id"],
                    "match_id": mid,
                    "league": lg,
                    "match_date": m.get("match_date"),
                    "home_team": name(m, "home_team") or m["home_team"].get("home_team_name"),
                    "away_team": name(m, "away_team") or m["away_team"].get("away_team_name"),
                    "team": name(e, "team"),
                    "player_id": (e.get("player") or {}).get("id"),
                    "player": name(e, "player"),
                    "position": name(e, "position"),
                    "period": e.get("period"),
                    "minute": e.get("minute"),
                    "second": e.get("second"),
                    "possession": e.get("possession"),
                    "play_pattern": name(e, "play_pattern"),
                    "x": loc[0],
                    "y": loc[1],
                    "end_x": end[0],
                    "end_y": end[1],
                    "end_z": end[2],
                    "duration": e.get("duration"),
                    "under_pressure": bool(e.get("under_pressure", False)),
                    "shot_type": st,
                    "body_part": name(s, "body_part"),
                    "technique": name(s, "technique"),
                    "first_time": bool(s.get("first_time", False)),
                    "follows_dribble": bool(s.get("follows_dribble", False)),
                    "open_goal": bool(s.get("open_goal", False)),
                    "one_on_one": bool(s.get("one_on_one", False)),
                    "aerial_won": bool(s.get("aerial_won", False)),
                    "deflected": bool(s.get("deflected", False)),
                    "redirect": bool(s.get("redirect", False)),
                    "key_pass_id": kp,
                    "key_pass_type": kpt,
                    "freeze_frame_players": len(s.get("freeze_frame") or []),
                    "statsbomb_xg": s.get("statsbomb_xg"),
                    "outcome": name(s, "outcome"),
                    "goal": int(name(s, "outcome") == "Goal"),
                })
                for p in s.get("freeze_frame") or []:
                    pl = p.get("location") or [None, None]
                    ff_rows.append({
                        "shot_id": e["id"],
                        "player_id": (p.get("player") or {}).get("id"),
                        "position": name(p, "position"),
                        "teammate": bool(p.get("teammate")),
                        "x": pl[0],
                        "y": pl[1],
                    })
            if i % 200 == 0:
                print(f"  {i}/{len(by_match)} matches", flush=True)

    with open(os.path.join(DATA, "SHA256SUMS_raw.txt"), "w", newline="\n") as f:
        for rel in sorted(sums):
            f.write(f"{sums[rel]}  raw/{rel}\n")

    for fname, rows in [("shots_open_play.csv", shot_rows), ("freeze_frames_open_play.csv", ff_rows)]:
        rows.sort(key=lambda r: (r["shot_id"],) if fname.startswith("freeze") else (r["league"], r["match_date"], r["match_id"], r["period"], r["minute"], r["second"]))
        with open(os.path.join(OUT, fname), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)

    lines = [f"StatsBomb open-data commit {COMMIT}", ""]
    lines.append("Matches per league: " + ", ".join(f"{lg} {sum(1 for g in games if g[0] == lg)}" for lg in LEAGUES))
    lines.append(f"Event files read: {sum(1 for r in sums if r.startswith('events/'))}")
    lines.append("")
    lines.append("All shots by shot type: " + ", ".join(f"{k} {v}" for k, v in type_counts.most_common()))
    lines.append(f"Total shots: {sum(type_counts.values())}")
    lines.append("")
    for lg in LEAGUES:
        lines.append(f"{lg}: " + ", ".join(f"{t} {type_by_league[(lg, t)]}" for t in type_counts if type_by_league[(lg, t)]))
    lines.append("")
    lines.append("Open-play shots by key-pass type: " + ", ".join(f"{k} {v}" for k, v in keypass_counts.most_common()))
    for t in sorted(EXCLUDE_KEY_PASS_TYPES):
        lines.append(f"Open-play shots excluded because the key pass is a {t}: " + ", ".join(f"{lg} {excl_by_league[(lg, t)]}" for lg in LEAGUES) + f"; total {sum(v for (l, k), v in excl_by_league.items() if k == t)}")
    lines.append(f"Kept shots whose possession contains an earlier corner (not excluded, reported only): {corner_in_possession}")
    lines.append("")
    lines.append(f"Open-play shots kept: {len(shot_rows)}; goals among them: {sum(r['goal'] for r in shot_rows)}")
    lines.append(f"Freeze-frame player rows: {len(ff_rows)}")
    for fname in ["shots_open_play.csv", "freeze_frames_open_play.csv"]:
        with open(os.path.join(OUT, fname), "rb") as f:
            lines.append(f"SHA-256 {fname}: {hashlib.sha256(f.read()).hexdigest()}")
    with open(os.path.join(DATA, "SHA256SUMS_raw.txt"), "rb") as f:
        lines.append(f"SHA-256 SHA256SUMS_raw.txt: {hashlib.sha256(f.read()).hexdigest()}")
    text = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "download_log.txt"), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
