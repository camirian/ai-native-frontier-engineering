# Independent Oracle

`reference.py` is a symbolic state-evolution model written directly from the
frozen mission requirements. It has no dependency on a candidate package and
does not import candidate code, invoke candidate transitions, or reproduce a
candidate's implementation architecture.

Trace convention: `DATA.direction` is `LOCAL` for locally transmitted data and
`PEER` for received data. This makes the distinct transmit/receive requirements
executable. `CLOSE_REQ` represents the local close request described by R19.

Frozen interpretation routing:

- A1: the third consecutive applicable timeout aborts immediately; the first
  two timeout events retransmit.
- A2: only `expected_recv - 1` is the idempotent received-data duplicate. Any
  older received sequence is explicit `INVALID`.
- C2: close is gated only by local transmitted outstanding data; inbound data
  has no separate acknowledgment-pending state in the requirements.
- R35 uses `IGNORED` for a duplicate matching close ACK in `CLOSED`; all other
  invalid events use `INVALID` without mutation.

Run a frozen trace corpus:

```bash
python3 oracle/run_oracle.py held_out_traces
```

The runner checks a trace's optional `oracle_expectations` list. Each entry is
the compact `{result, state, action}` projection emitted after an event.
