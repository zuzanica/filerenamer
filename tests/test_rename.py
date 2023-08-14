
import pytest

from main import FileData, InvalidFilenameError, format_file

testdata = [
    ("236041275_opabltl-zirblgu_z_11x29_00.psd", "236041275_opabltl_zirblgu_z#00-11x29.psd"),
    ("244040004_brlblgu_7x15_00_z.png", "244040004_brlblgu_z#00-7x15.png"),
    ("244040012_brlblgu_8x28_01_z.psd", "244040012_brlblgu_z#01-8x28.psd"),
    ("226041093_zirrugu_zirblgu_02_b.png", "326041093_zirrugu_zirblgu_b#02.png"),
    ("236041275_opabltl_zirblgu_z_11x29_00.psd", "236041275_opabltl_zirblgu_z#00-11x29.psd"),
    ("236041132_zirblgu_z_12x8_00.psd", "236041132_zirblgu_z#00-12x8.psd"),
    ("231040545_zr_9x20_03.png", "231040545_zr#03-9x20.png"),
    ("224040022_brlblgu_02_b.png", "324040022_brlblgu_b#02.png"),
    ("224040022_brlblgu_02_r.png", "724040022_brlblgu_r#02.png"),
    ("231040937_br_11x40_00.png", "331040937_br#00-11x40.png"),
    ("231040937_zr_11x40_03.png", "231040937_zr#03-11x40.png"),
]


@pytest.mark.parametrize("input_file_name,expected", testdata)
def test_valid(input_file_name, expected):
    assert format_file(input_file_name) == expected


@pytest.mark.parametrize("input_file_name", [
    "246040859_zirblgu_7x12x4_01.png",
    "246040855_zirblgu-15x15_2d_0001.png",
    "236041275_z_opabltl_zirblgu_z_11x29_03.png",
    "236041275_b_opabltl_zirblgu_z_11x29_01.png",
    "236041132_b_zirblgu_z_12x8_01.png",
])
def test_invalid(input_file_name):
    with pytest.raises(InvalidFilenameError):
        format_file(input_file_name)
