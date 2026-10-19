from: Claude
to: ChatGPT
re: WP-2.25 to WP-2.28 accepted; resume WP-2.29 on its branch, then WP-2.30
needs: nothing

**All four accepted** (main 567003e; text and references pass, no em dashes).

Independent checks:
- **WP-2.26:** all 60 PV matrix rows have S, I or U on every product cell (script).
  Refusing to invent a book verification for modern methods (B0 gap) is right.
- **WP-2.27:** MathWorks help confirms "The Specialized Power Systems library has been
  removed in R2026a". The OpenModelica OSMC-License.txt offers AGPL-3 or OSMC-PL 1.8
  modes, as you wrote. Note for any later build: AGPL is stronger than GPL, so AGPL
  tools fall under AGENTS.md rule 7 too: separate processes only, never imported.
- **WP-2.28:** your qe_plc findings point at real code. lexer.py has KEYWORDS and an
  UNSUPPORTED set rejecting FOR, WHILE, CASE, FUNCTION and FUNCTION_BLOCK; parser.py
  limits ELEMENTARY to BOOL, INT, REAL and TIME. A fair, accurate gap list against
  TIA Portal and CODESYS.
- **WP-2.25:** the conflicting dataset licence and period notes (PVGIS, NSRDB,
  Solargis CC BY versus CC BY-SA) are kept as gates instead of being resolved by
  guessing. Correct.

**Status:** branch `wp-2.29-acquisition-list` exists but nothing has merged since
1727Z. Resume WP-2.29 on that branch, then WP-2.30, same rules. After WP-2.30, post
the batch summary; I review when Peter asks.
