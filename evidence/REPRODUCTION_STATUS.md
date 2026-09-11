# Reproduction status

Source artifacts were inspected in their original mission-output locations and sanitized into this standalone proposal. A fresh disposable package reproduction is required before publication.

`scripts/reproduce_fresh.sh` copies this package to a disposable directory, runs both clean-room experiments, renders figures, and checks that no forbidden absolute-path or private-reference patterns remain. Its result is the required pre-publication evidence.

At package assembly, no original repository was modified and no public repository was created.
