"""
Matemātikas uzdevumu ģenerators / Math task generator

Ģenerē uzdevumus atkarībā no grūtības pakāpes (1-5).
Grūtības pakāpes:
  1 — saskaitīšana, atņemšana, reizināšana (līdz 20)
  2 — dalīšana, procenti, viegli vienādojumi
  3 — daudzciparu darbības, dažādas darbības, dažādas daļskaitļi
  4 — vienādojumi ar nezināmo, procentu uzdevumi
  5 — sarežģīti vienādojumi, daļskaitļi, daudzsoļu uzdevumi
"""

from __future__ import annotations
import random
import math


class MathTask:
    """
    Viens matemātikas uzdevums.

    === Iekapsulesana ===
    Jautājuma teksts un atbilde glabātas privāti.
    Piekļuve caur property.
    """

    def __init__(self, question: str, answer: float, tolerance: float = 0.01) -> None:
        self._question:  str   = question
        self._answer:    float = answer
        self._tolerance: float = tolerance   # Pieļaujamā kļūda (veseliem skaitļiem = 0)

    @property
    def question(self) -> str:
        return self._question

    @property
    def answer(self) -> float:
        return self._answer

    def check(self, user_input: str) -> bool:
        """
        Pārbauda lietotāja atbildi.
        Pieņem veselu skaitli vai decimāldaļu.
        """
        try:
            val = float(user_input.replace(",", "."))
            return abs(val - self._answer) <= self._tolerance
        except ValueError:
            return False

    def __repr__(self) -> str:
        return f"MathTask({self._question!r} = {self._answer})"


# ======================================================================= #
#  Uzdevumu ģenerēšanas funkcijas pa grūtības pakāpēm
# ======================================================================= #

def _d1() -> MathTask:
    """Grūtība 1 — vienkāršas darbības ar maziem skaitļiem."""
    op = random.choice(["+", "-", "*"])
    if op == "+":
        a, b = random.randint(1, 20), random.randint(1, 20)
        return MathTask(f"{a} + {b} = ?", a + b)
    elif op == "-":
        a, b = random.randint(1, 20), random.randint(1, 20)
        a, b = max(a, b), min(a, b)
        return MathTask(f"{a} - {b} = ?", a - b)
    else:
        a, b = random.randint(1, 10), random.randint(1, 10)
        return MathTask(f"{a} × {b} = ?", a * b)


def _d2() -> MathTask:
    """Grūtība 2 — dalīšana, procenti, vienkārši vienādojumi."""
    kind = random.choice(["div", "pct", "eq"])
    if kind == "div":
        b = random.randint(2, 12)
        q = random.randint(1, 12)
        a = b * q
        return MathTask(f"{a} ÷ {b} = ?", q)
    elif kind == "pct":
        pct = random.choice([10, 20, 25, 50])
        base = random.choice([40, 60, 80, 100, 120, 200])
        ans = base * pct // 100
        return MathTask(f"{pct}% no {base} = ?", ans)
    else:
        x = random.randint(1, 20)
        b = random.randint(1, 15)
        a = x + b
        return MathTask(f"x + {b} = {a},  x = ?", x)


def _d3() -> MathTask:
    """Grūtība 3 — lielāki skaitļi, daļskaitļi, jauktas darbības."""
    kind = random.choice(["big", "frac", "mixed"])
    if kind == "big":
        op = random.choice(["+", "-", "*"])
        if op == "*":
            a, b = random.randint(10, 25), random.randint(2, 12)
            return MathTask(f"{a} × {b} = ?", a * b)
        a, b = random.randint(50, 200), random.randint(10, 80)
        if op == "+":
            return MathTask(f"{a} + {b} = ?", a + b)
        a, b = max(a, b), min(a, b)
        return MathTask(f"{a} - {b} = ?", a - b)
    elif kind == "frac":
        denoms = [2, 4, 5, 10]
        d = random.choice(denoms)
        n1 = random.randint(1, d - 1)
        n2 = random.randint(1, d - 1)
        ans = round((n1 + n2) / d, 2)
        return MathTask(f"{n1}/{d} + {n2}/{d} = ?", ans, tolerance=0.05)
    else:
        a = random.randint(2, 9)
        b = random.randint(10, 30)
        c = random.randint(1, 20)
        ans = a * b + c
        return MathTask(f"{a} × {b} + {c} = ?", ans)


def _d4() -> MathTask:
    """Grūtība 4 — vienādojumi, procentu uzdevumi."""
    kind = random.choice(["eq2", "pct2", "power"])
    if kind == "eq2":
        x = random.randint(2, 15)
        k = random.randint(2, 6)
        b = random.randint(1, 20)
        rhs = k * x + b
        return MathTask(f"{k}x + {b} = {rhs},  x = ?", x)
    elif kind == "pct2":
        pct = random.choice([15, 30, 35, 40, 60, 75])
        base = random.choice([80, 120, 160, 200, 240])
        ans = round(base * pct / 100, 1)
        return MathTask(f"{pct}% no {base} = ?", ans, tolerance=0.15)
    else:
        base = random.randint(2, 9)
        exp  = random.randint(2, 3)
        return MathTask(f"{base}² = ?" if exp == 2 else f"{base}³ = ?",
                        base ** exp)


def _d5() -> MathTask:
    """Grūtība 5 — sarežģīti vienādojumi, daudzsoļu uzdevumi."""
    kind = random.choice(["eq3", "frac2", "combined"])
    if kind == "eq3":
        x = random.randint(1, 12)
        a = random.randint(2, 8)
        b = random.randint(1, 15)
        c = random.randint(1, 10)
        rhs = a * x - b + c
        return MathTask(f"{a}x - {b} + {c} = {rhs},  x = ?", x)
    elif kind == "frac2":
        d1, d2 = random.choice([(2, 3), (3, 4), (2, 5), (4, 5)])
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        ans = round(n1 / d1 + n2 / d2, 3)
        return MathTask(f"{n1}/{d1} + {n2}/{d2} = ?", ans, tolerance=0.05)
    else:
        a = random.randint(3, 9)
        b = random.randint(2, 7)
        c = random.randint(10, 30)
        d = random.randint(1, 10)
        ans = a * b + c - d
        return MathTask(f"{a} × {b} + {c} - {d} = ?", ans)


_GENERATORS = {1: _d1, 2: _d2, 3: _d3, 4: _d4, 5: _d5}


def generate_task(difficulty: int) -> MathTask:
    """
    Ģenerē uzdevumu norādītās grūtības pakāpei.
    difficulty: 1..5
    """
    difficulty = max(1, min(5, difficulty))
    return _GENERATORS[difficulty]()
