"""
Which question to ask next.

Every scheme is a rule over the person's profile. Instead of a fixed list of questions, the engine looks at the rules:
for each scheme it works out whether the answer is already certain, and if not, which unanswered details could still
change it. It then asks about the detail that the most undecided schemes depend on, and stops when nothing a person
could say would change the list (or after MAX_FOLLOWUPS questions, so nobody gets an interview).

So adding schemes does not add questions for people they can't apply to: a farmer is never asked about PF, a man is
never asked about maternity benefit, and someone outside a state is never asked what only that state's schemes need.
"""

# The first three are asked of everyone: almost every rule depends on them.
CORE = ["age", "occupation", "state"]

# Values to try for a detail we don't know yet. Numbers are sample points on both sides of every limit used in a rule.
YES_NO = [True, False]
DOMAIN = {
    "land_ha": [0.0, 0.4, 1.5, 3.0, 8.0],
    "income_month": [0, 4000, 8000, 10000, 12000, 15000, 16000, 20000, 22000, 25000, 30000, 45000, 60000, 80000,
                     200000],
    "itax": YES_NO, "epf": YES_NO, "daughter_u10": YES_NO, "biz": YES_NO,
    "gender": ["f", "m"],
    "rural": YES_NO,            # lives in a village (True) or a town / city (False)
    "bpl": YES_NO,              # has a BPL / Antyodaya / priority ration card
    "pucca": YES_NO,            # the family owns a pucca house
    "lpg": YES_NO,              # the home has an LPG gas connection
    "maternity": YES_NO,        # pregnant, or had a baby recently
    "widow": YES_NO,
    "disabled": YES_NO,         # has a disability certificate (40% or more)
    "category": ["sc", "st", "obc", "gen"],
    "study": ["school", "college", "none"],   # what a student is studying
}

# When several details tie, ask in this order: what people expect to be asked first, personal questions last.
PRIORITY = ["land_ha", "income_month", "itax", "epf", "gender", "rural", "study", "bpl", "daughter_u10", "pucca", "lpg",
            "maternity", "widow", "disabled", "category", "biz"]

MAX_FOLLOWUPS = 9               # questions after age / work / state
MAX_DEPTH = 7                   # unknown details explored per rule


# PF / ESIC only makes sense for people who work for a wage or for themselves
WAGE_OR_SELF = {"labourer", "street_vendor", "artisan", "other_self_employed", "shopkeeper", "salaried_private",
                "fisher", "construction_worker", "gig_worker", "domestic_worker"}


def _age_between(p, lo, hi):
    a = p.get("age")
    return a is None or lo <= a <= hi


# A question is only worth asking when this holds; otherwise the detail is recorded as "not applicable" (None).
GATES = {
    "daughter_u10": lambda p: _age_between(p, 18, 60),
    "biz": lambda p: p.get("occupation") not in ("govt_employee", "farmer") and _age_between(p, 18, 60),
    "epf": lambda p: _age_between(p, 16, 59) and p.get("occupation") in WAGE_OR_SELF,
    "maternity": lambda p: p.get("gender") == "f" and _age_between(p, 18, 45),
    "widow": lambda p: p.get("gender") == "f" and _age_between(p, 18, 200),
    "study": lambda p: p.get("occupation") == "student",
    "land_ha": lambda p: p.get("occupation") == "farmer",
}


class _Trace(dict):
    """A profile that remembers which details a rule looked at."""

    def __init__(self, data):
        super().__init__(data)
        self.seen = []

    def _note(self, k):
        if k not in self.seen:
            self.seen.append(k)

    def get(self, k, default=None):
        self._note(k)
        return super().get(k, default)

    def __getitem__(self, k):
        self._note(k)
        return super().get(k)

    def __contains__(self, k):
        self._note(k)
        return super().__contains__(k)


def infer(p: dict) -> dict:
    """Facts that follow from other answers (changes p in place and returns it)."""
    inc = p.get("income_month")
    if "itax" not in p and inc is not None and inc * 12 <= 500000:
        p["itax"] = False                       # up to ₹5 lakh a year owes no income tax under either regime
    occ = p.get("occupation")
    if occ == "govt_employee":
        p.setdefault("epf", True)
    if occ == "homemaker":
        p.setdefault("gender", "f")
    if occ == "farmer":
        p.setdefault("rural", True)
    for slot, gate in GATES.items():
        if slot not in p and not _open_gate(gate, p):
            p[slot] = None
    return p


def _open_gate(gate, p):
    try:
        return bool(gate(p))
    except Exception:
        return True


def _run(rule, p):
    t = _Trace(p)
    try:
        r = bool(rule(t))
    except Exception:
        r = False
    return r, t.seen


def explore(rule, p: dict, depth: int = 0):
    """(possible outcomes, details that could still matter) for one rule, given what we know."""
    r, seen = _run(rule, p)
    unknown = [k for k in seen if k not in p and k in DOMAIN]
    if not unknown or depth >= MAX_DEPTH:
        return {r}, set()
    k = unknown[0]
    outs, deps, per_value = set(), set(), []
    for v in DOMAIN[k]:
        q = infer({**p, k: v})
        o, d = explore(rule, q, depth + 1)
        outs |= o
        deps |= d
        per_value.append(frozenset(o))
    if len(set(per_value)) > 1:                 # the answer changes with this detail itself
        deps.add(k)
    return outs, deps


def status(rules: dict, p: dict):
    """rules: {scheme id: rule}. Returns ({id: True/False for decided schemes}, {id: set of details} for open ones)."""
    decided, open_ = {}, {}
    for sid, rule in rules.items():
        outs, deps = explore(rule, p)
        if len(outs) == 1:
            decided[sid] = next(iter(outs))
        else:
            open_[sid] = deps
    return decided, open_


def next_slot(rules: dict, p: dict, asked_followups: int = 0):
    """The next detail to ask about, or None when we can show results."""
    for s in CORE:
        if s not in p:
            return s
    if asked_followups >= MAX_FOLLOWUPS:
        return None
    _, open_ = status(rules, p)
    score = {}
    for deps in open_.values():
        for s in deps:
            if s not in p:
                score[s] = score.get(s, 0) + 1
    if not score:
        return None
    rank = {s: i for i, s in enumerate(PRIORITY)}
    if len(score) <= MAX_FOLLOWUPS - asked_followups:
        return min(score, key=lambda s: rank.get(s, 99))        # room for all of them: ask in a natural order
    return max(score, key=lambda s: (score[s], -rank.get(s, 99)))   # short on questions: the most useful one first
