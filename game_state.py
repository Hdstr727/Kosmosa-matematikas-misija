"""
Spēles stāvokļa saglabāšana / Game state persistence
Saglabā atbloķētos un pabiegtos līmeņus JSON failā.

=== Iekapsulesana (Encapsulation) ===
GameState klase pārvaldī visus saglabātos datus iekšēji.
Ārējs kods izmanto tikai publiskās metodes.
"""

import json
import os


class GameState:
    """
    Glabā spēlētāja progresu starp sesijām.
    Izmanto JSON failu kā vienkāršu datu bāzi.
    """

    SAVE_FILE = "save_data.json"

    def __init__(self):
        # === Datu slēpsana (Data hiding) ===
        # Privāti atribūti — ārējs kods nedrīkst tieši mainīt
        self._unlocked: set[int] = {1}   # 1. līmenis vienmēr atvērts
        self._completed: set[int] = set()

        self._load()

    # ------------------------------------------------------------------ #
    #  Privātās metodes / Private methods
    # ------------------------------------------------------------------ #

    def _load(self) -> None:
        """Ielādē saglabāto progresu no faila (ja tāds eksistē)."""
        if not os.path.exists(self.SAVE_FILE):
            return
        try:
            with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._unlocked  = set(data.get("unlocked",  [1]))
            self._completed = set(data.get("completed", []))
        except (json.JSONDecodeError, KeyError):
            # Ja fails bojāts — sāk no sākuma
            self._unlocked  = {1}
            self._completed = set()

    def _save(self) -> None:
        """Saglabā progresu JSON failā."""
        data = {
            "unlocked":  list(self._unlocked),
            "completed": list(self._completed),
        }
        with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------------------ #
    #  Publiskās metodes / Public interface
    # ------------------------------------------------------------------ #

    def complete_level(self, level_num: int) -> None:
        """Atzīmē līmeni kā pabeigtu un atbloķē nākamo."""
        self._completed.add(level_num)
        self._unlocked.add(level_num + 1)  # Atbloķē nākamo
        self._save()

    def is_unlocked(self, level_num: int) -> bool:
        """Atgriež True, ja līmenis ir spēlētājam pieejams."""
        return level_num in self._unlocked

    def is_completed(self, level_num: int) -> bool:
        """Atgriež True, ja līmenis jau pabeigts."""
        return level_num in self._completed

    def reset(self) -> None:
        """Atiestata visu progresu (tikai atkļūdošanai)."""
        self._unlocked  = {1}
        self._completed = set()
        self._save()

    @property
    def unlocked_levels(self) -> set:
        """Atgriež atbloķēto līmeņu kopu (kopija, lai droši)."""
        return set(self._unlocked)

    @property
    def completed_levels(self) -> set:
        """Atgriež pabeigto līmeņu kopu (kopija)."""
        return set(self._completed)
