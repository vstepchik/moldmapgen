import logging
import os
from typing import NewType, Tuple, Dict, Any

import imgui

log = logging.getLogger(__name__)

FontDef = NewType('FontDef', Tuple[str, int])
_CACHE: Dict[FontDef, Any] = {}

FNT_TERMINUS_24 = FontDef(("TerminusTTF-4.47.0.ttf", 24))
FNT_TERMINUS_B_24 = FontDef(("TerminusTTF-Bold-4.47.0.ttf", 24))
FNT_TERMINUS_I_24 = FontDef(("TerminusTTF-Italic-4.47.0.ttf", 24))
FNT_TERMINUS_BI_24 = FontDef(("TerminusTTF-Bold_Italic-4.47.0.ttf", 24))
FNT_3270_MED_28 = FontDef(("3270Medium.ttf", 28))
FNT_3270_NAR_28 = FontDef(("3270Narrow.ttf", 28))


def get_font(font_def: FontDef):
    return _CACHE[font_def]


def init_fonts():
    log.info("Initializing fonts...")
    _CACHE.update({
        FNT_TERMINUS_24: _load(FNT_TERMINUS_24),
        FNT_TERMINUS_B_24: _load(FNT_TERMINUS_B_24),
        FNT_TERMINUS_I_24: _load(FNT_TERMINUS_I_24),
        FNT_TERMINUS_BI_24: _load(FNT_TERMINUS_BI_24),
        FNT_3270_MED_28: _load(FNT_3270_MED_28),
        FNT_3270_NAR_28: _load(FNT_3270_NAR_28),
    })


def _load(font_def: FontDef):
    file, size = font_def
    path = os.path.join(os.path.dirname(__file__), file)
    log.info(f"Loading font {path}")
    io = imgui.get_io()
    loaded_font = io.fonts.add_font_from_file_ttf(path, size, glyph_ranges=io.fonts.get_glyph_ranges_cyrillic())
    return loaded_font
