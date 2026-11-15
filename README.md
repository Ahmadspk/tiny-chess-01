# tiny-chess-01

A chess engine in 4,096 bytes of Python (see `main.py`; readable source
in `engine.py`). 0x88 board, negamax + alpha-beta + quiescence, transposition
table, killer moves, MVV-LVA ordering, iterative deepening to a fixed node
budget (deterministic, no clock). Evaluation: material + piece-square tables
+ bishop pair, phased king safety.

Plays the house gauntlet through the make.fun env (`MAKEFUN_ENV_URL`).
