"""
Modulo de Sefirot - Las emanaciones del sistema Tikun

Cada Sefira representa un aspecto funcional del sistema de IA alineada.
"""

# Importar solo las Sefirot que no tienen dependencias rotas
try:
    from .keter import Keter
except ImportError:
    Keter = None

try:
    from .chochmah_gemini import ChochmahGemini
except ImportError:
    ChochmahGemini = None

try:
    from .binah import Binah
except ImportError:
    Binah = None

# Otras Sefirot - intentar importar pero no fallar si hay problemas
try:
    from .chesed import Chesed
except ImportError:
    Chesed = None

try:
    from .gevurah import Gevurah
except ImportError:
    Gevurah = None

try:
    from .tiferet import Tiferet
except ImportError:
    Tiferet = None

try:
    from .netzach import Netzach
except ImportError:
    Netzach = None

try:
    from .hod import Hod
except ImportError:
    Hod = None

try:
    from .yesod import Yesod
except ImportError:
    Yesod = None

try:
    from .malchut import Malchut
except ImportError:
    Malchut = None

__all__ = [
    'Keter',
    'ChochmahGemini',
    'Binah',
    'Chesed',
    'Gevurah',
    'Tiferet',
    'Netzach',
    'Hod',
    'Yesod',
    'Malchut'
]
