version 18.0
use "$PANEL_FILE", clear
isid firm_id year
assert _N == 400
assert inrange(year, 2018, 2022)
assert missing(y) if outcome_status == "unknown"
assert !missing(y) if outcome_status == "observed"
count if missing(y)
assert r(N) == 8
