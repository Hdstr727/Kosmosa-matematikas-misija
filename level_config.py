"""
Līmeņu konfigurācija / Level configuration
Katrs līmenis kļūst grūtāks: vairāk asteroīdu, grūtāki uzdevumi,
mazāk laika atbildei.
"""

# === LĪMEŅU DATI / Level data ===
# Katra vārdnīca apraksta viena līmeņa parametrus.
# Laiks = sekundes līdz finiša līnijai (40-90s diapazonā).
# Pasaules augstums = scroll_speed * laiks (pikseļi).

LEVEL_CONFIGS = [
    # --- Līmenis 1 ---
    {
        "level":            1,
        "duration":         65,      # sekundes
        "world_height":     9100,    # 65 * 140 px/s
        "scroll_speed":     140,     # px/s
        "asteroid_count":   4,
        "asteroid_speed":   70,      # px/s (maks asteroīdam šajā līmenī)
        "math_interval":    (10, 14),
        "math_time":        22,      # sekundes atbildei
        "breakdown_interval": (35, 55),
        "difficulty":       1,       # Grūtības pakāpe uzdevumiem (1-5)
        "pickups_health":   3,
        "pickups_fuel":     3,
    },
    # --- Līmenis 2 ---
    {
        "level":            2,
        "duration":         62,
        "world_height":     9300,
        "scroll_speed":     150,
        "asteroid_count":   5,
        "asteroid_speed":   85,
        "math_interval":    (10, 13),
        "math_time":        20,
        "breakdown_interval": (32, 50),
        "difficulty":       1,
        "pickups_health":   3,
        "pickups_fuel":     3,
    },
    # --- Līmenis 3 ---
    {
        "level":            3,
        "duration":         60,
        "world_height":     9600,
        "scroll_speed":     160,
        "asteroid_count":   6,
        "asteroid_speed":   95,
        "math_interval":    (9, 13),
        "math_time":        20,
        "breakdown_interval": (30, 48),
        "difficulty":       2,
        "pickups_health":   2,
        "pickups_fuel":     3,
    },
    # --- Līmenis 4 ---
    {
        "level":            4,
        "duration":         58,
        "world_height":     9860,
        "scroll_speed":     170,
        "asteroid_count":   7,
        "asteroid_speed":   105,
        "math_interval":    (9, 12),
        "math_time":        18,
        "breakdown_interval": (28, 45),
        "difficulty":       2,
        "pickups_health":   2,
        "pickups_fuel":     2,
    },
    # --- Līmenis 5 ---
    {
        "level":            5,
        "duration":         56,
        "world_height":     10080,
        "scroll_speed":     180,
        "asteroid_count":   8,
        "asteroid_speed":   115,
        "math_interval":    (8, 12),
        "math_time":        17,
        "breakdown_interval": (26, 42),
        "difficulty":       3,
        "pickups_health":   2,
        "pickups_fuel":     2,
    },
    # --- Līmenis 6 ---
    {
        "level":            6,
        "duration":         54,
        "world_height":     10260,
        "scroll_speed":     190,
        "asteroid_count":   9,
        "asteroid_speed":   125,
        "math_interval":    (8, 11),
        "math_time":        16,
        "breakdown_interval": (24, 40),
        "difficulty":       3,
        "pickups_health":   2,
        "pickups_fuel":     2,
    },
    # --- Līmenis 7 ---
    {
        "level":            7,
        "duration":         52,
        "world_height":     10400,
        "scroll_speed":     200,
        "asteroid_count":   10,
        "asteroid_speed":   135,
        "math_interval":    (8, 11),
        "math_time":        15,
        "breakdown_interval": (22, 38),
        "difficulty":       4,
        "pickups_health":   2,
        "pickups_fuel":     2,
    },
    # --- Līmenis 8 ---
    {
        "level":            8,
        "duration":         50,
        "world_height":     10500,
        "scroll_speed":     210,
        "asteroid_count":   11,
        "asteroid_speed":   145,
        "math_interval":    (8, 10),
        "math_time":        14,
        "breakdown_interval": (20, 35),
        "difficulty":       4,
        "pickups_health":   1,
        "pickups_fuel":     2,
    },
    # --- Līmenis 9 ---
    {
        "level":            9,
        "duration":         47,
        "world_height":     10575,
        "scroll_speed":     225,
        "asteroid_count":   12,
        "asteroid_speed":   155,
        "math_interval":    (7, 10),
        "math_time":        13,
        "breakdown_interval": (18, 32),
        "difficulty":       5,
        "pickups_health":   1,
        "pickups_fuel":     2,
    },
    # --- Līmenis 10 ---
    {
        "level":            10,
        "duration":         44,
        "world_height":     10560,
        "scroll_speed":     240,
        "asteroid_count":   14,
        "asteroid_speed":   165,
        "math_interval":    (7, 10),
        "math_time":        12,
        "breakdown_interval": (16, 30),
        "difficulty":       5,
        "pickups_health":   1,
        "pickups_fuel":     1,
    },
]


def get_level_config(level_num: int) -> dict:
    """
    Atgriež līmeņa konfigurācijas vārdnīcu.
    level_num: 1 līdz 10
    """
    if 1 <= level_num <= len(LEVEL_CONFIGS):
        return LEVEL_CONFIGS[level_num - 1]
    raise ValueError(f"Nepareizs līmeņa numurs: {level_num}")


TOTAL_LEVELS = len(LEVEL_CONFIGS)
