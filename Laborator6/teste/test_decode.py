import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


from Laborator6.arsenal.forensics.decode import *

TEST_DATA = {
    "%2Fetc": "url",
    "48656c6c6f": "hex",
    "U2FsdXQ=": "base64",
    "FLAG{x}": "necunoscut",
}

@pytest.mark.parametrize("sir, strat_asteptat", TEST_DATA.items())
def test_ghici_strat(sir, strat_asteptat):
    assert ghici_strat(sir) == strat_asteptat



def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex():
    strat, b = desfa("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"


def test_url():
    strat, b = desfa("%2Fetc")
    assert strat == "url"
    assert b == b"/etc"

def test_strat_necunoscut_nu_se_desface():
    strat, b = desfa("FLAG{x}")
    assert strat == "necunoscut"
    assert b is None


def test_citibil_text_simplu():
    assert citibil(b"Salut") is True


def test_citibil_octeti_de_control():
    assert citibil(b"\x00\x01\x02") is False

