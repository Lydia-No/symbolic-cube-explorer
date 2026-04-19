"""
SQLite memory for cross-run learning + trends.

Stores:
- runs: run metadata + core metrics + signatures
- motifs: hashed motifs for symbol and axis motifs

No raw prompt required.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .schema import RunResult


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ensure_db(path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
              run_id TEXT PRIMARY KEY,
              created_at_utc TEXT NOT NULL,
              grammar TEXT NOT NULL,
              dim INTEGER NOT NULL,
              steps INTEGER NOT NULL,
              walker TEXT NOT NULL,
              objective TEXT NOT NULL,
              state_entropy REAL NOT NULL,
              symbol_entropy REAL NOT NULL,
              coverage_ratio REAL NOT NULL,
              avg_surprisal REAL NOT NULL,
              loop_found INTEGER NOT NULL,
              loop_len INTEGER,
              attractor_signature_json TEXT NOT NULL
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS motifs (
              run_id TEXT NOT NULL,
              motif_hash TEXT NOT NULL,
              motif_type TEXT NOT NULL,
              n INTEGER NOT NULL,
              count INTEGER NOT NULL,
              motif_json TEXT NOT NULL,
              PRIMARY KEY (run_id, motif_hash, motif_type, n),
              FOREIGN KEY (run_id) REFERENCES runs(run_id)
            )
            """
        )
        con.execute("CREATE INDEX IF NOT EXISTS idx_runs_grammar ON runs(grammar)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_motif_hash ON motifs(motif_hash)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_motifs_type ON motifs(motif_type)")
        con.commit()


def motif_hash(motif: Iterable[Any]) -> str:
    return _sha256_text(json.dumps(list(motif), ensure_ascii=False, separators=(",", ":")))


def upsert_run(path: str, result: RunResult) -> None:
    ensure_db(path)
    with sqlite3.connect(path) as con:
        con.execute(
            """
            INSERT OR REPLACE INTO runs (
              run_id, created_at_utc, grammar, dim, steps, walker, objective,
              state_entropy, symbol_entropy, coverage_ratio, avg_surprisal,
              loop_found, loop_len, attractor_signature_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.config.run_id,
                result.config.created_at_utc,
                result.config.grammar,
                int(result.config.dim),
                int(result.config.steps),
                result.config.walker,
                result.config.objective,
                float(result.metrics.state_entropy),
                float(result.metrics.symbol_entropy),
                float(result.metrics.coverage_ratio),
                float(result.metrics.avg_surprisal),
                1 if result.metrics.loop_found else 0,
                int(result.metrics.loop_len) if result.metrics.loop_len is not None else None,
                json.dumps(result.metrics.attractor_signature, separators=(",", ":")),
            ),
        )

        con.execute("DELETE FROM motifs WHERE run_id = ?", (result.config.run_id,))

        for item in result.motifs.symbol_ngrams:
            mh = motif_hash(item["motif"])
            con.execute(
                """
                INSERT INTO motifs (run_id, motif_hash, motif_type, n, count, motif_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    result.config.run_id,
                    mh,
                    "symbol",
                    int(item["n"]),
                    int(item["count"]),
                    json.dumps(item["motif"], ensure_ascii=False, separators=(",", ":")),
                ),
            )

        for item in result.motifs.axis_ngrams:
            mh = motif_hash(item["motif"])
            con.execute(
                """
                INSERT INTO motifs (run_id, motif_hash, motif_type, n, count, motif_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    result.config.run_id,
                    mh,
                    "axis",
                    int(item["n"]),
                    int(item["count"]),
                    json.dumps(item["motif"], ensure_ascii=False, separators=(",", ":")),
                ),
            )

        con.commit()


def known_motif_hits(path: str, motifs: List[Dict[str, Any]], motif_type: str) -> int:
    if not path:
        return 0
    ensure_db(path)
    hashes = [motif_hash(m["motif"]) for m in motifs]
    if not hashes:
        return 0
    qmarks = ",".join(["?"] * len(hashes))
    sql = f"SELECT COUNT(DISTINCT motif_hash) FROM motifs WHERE motif_type = ? AND motif_hash IN ({qmarks})"
    with sqlite3.connect(path) as con:
        cur = con.execute(sql, [motif_type, *hashes])
        row = cur.fetchone()
        return int(row[0] or 0)


def list_runs(
    path: str,
    *,
    grammar: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    ensure_db(path)
    sql = """
    SELECT run_id, created_at_utc, grammar, dim, steps, walker, objective,
           state_entropy, symbol_entropy, coverage_ratio, avg_surprisal,
           loop_found, loop_len, attractor_signature_json
    FROM runs
    """
    params: List[Any] = []
    if grammar:
        sql += " WHERE grammar = ?"
        params.append(grammar)
    sql += " ORDER BY created_at_utc DESC LIMIT ?"
    params.append(int(limit))

    out: List[Dict[str, Any]] = []
    with sqlite3.connect(path) as con:
        cur = con.execute(sql, params)
        for row in cur.fetchall():
            out.append(
                {
                    "run_id": row[0],
                    "created_at_utc": row[1],
                    "grammar": row[2],
                    "dim": row[3],
                    "steps": row[4],
                    "walker": row[5],
                    "objective": row[6],
                    "state_entropy": row[7],
                    "symbol_entropy": row[8],
                    "coverage_ratio": row[9],
                    "avg_surprisal": row[10],
                    "loop_found": bool(row[11]),
                    "loop_len": row[12],
                    "attractor_signature": json.loads(row[13]) if row[13] else {},
                }
            )
    return out


def motif_leaderboard(
    path: str,
    *,
    grammar: Optional[str] = None,
    motif_type: str = "symbol",
    n: Optional[int] = None,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    ensure_db(path)
    sql = """
    SELECT m.motif_hash, m.motif_type, m.n, m.motif_json,
           COUNT(DISTINCT m.run_id) AS run_count,
           SUM(m.count) AS total_count
    FROM motifs m
    JOIN runs r ON r.run_id = m.run_id
    WHERE m.motif_type = ?
    """
    params: List[Any] = [motif_type]
    if grammar:
        sql += " AND r.grammar = ?"
        params.append(grammar)
    if n is not None:
        sql += " AND m.n = ?"
        params.append(int(n))
    sql += """
    GROUP BY m.motif_hash, m.motif_type, m.n, m.motif_json
    ORDER BY run_count DESC, total_count DESC
    LIMIT ?
    """
    params.append(int(limit))

    out: List[Dict[str, Any]] = []
    with sqlite3.connect(path) as con:
        cur = con.execute(sql, params)
        for row in cur.fetchall():
            out.append(
                {
                    "motif_hash": row[0],
                    "motif_type": row[1],
                    "n": row[2],
                    "motif": json.loads(row[3]),
                    "run_count": int(row[4] or 0),
                    "total_count": int(row[5] or 0),
                }
            )
    return out
