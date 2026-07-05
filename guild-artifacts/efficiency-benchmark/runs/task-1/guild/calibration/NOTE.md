# Task 1 — GUILD path — CALIBRATION NOT YET RUN

The GUILD-path side of the calibration is intentionally left unrun here, for an honesty reason worth
recording:

Running the GUILD critique path (Mage / `guild-critique`) autonomously from this pane would produce an
artifact, but it would NOT produce a valid **operator-attention** number — the headline metric — because
an autonomous agent driving itself registers ~0 operator attention. Pairing that against the baseline's
~0 would falsely read as a tie on the one metric that decides the benchmark.

The GUILD side must be run by a **human operator** following the fixed protocol (README → Operator
protocol), logging every prompt/steer as an intervention. That is the real data point.

What the calibration DID prove: the harness (folders, briefs, rubric, templates) yields a real,
gradeable artifact end-to-end (see `../baseline/calibration/output.md`).
