import argparse
from pathlib import Path
import re
from dataclasses import dataclass
import shutil

class InvalidFilenameError(Exception):
    ...


GOLD_COLOR_VALUE_MAPPING = {
    'z': 2,
    'b': 3,
    'r': 7,
}


@dataclass()
class FileData:
    code: str
    main_shard: str
    secondary_shard: str
    color: str
    size: str
    number: str
    suffix: str

    @classmethod
    def from_file_name(cls, f_name: str):
        f_name = f_name.replace('-', '_')

        code = cls.get_code(f_name)
        main_shard, secondary_shard = cls.get_shards(f_name)
        color = cls.get_color(f_name)
        size = cls.get_size(f_name)
        number = cls.get_number(f_name)
        suffix = cls.get_suffix(f_name)

        return cls(code, main_shard, secondary_shard, color, size, number, suffix)

    def __str__(self) -> str:
        result = f'{self.code}_'

        if self.main_shard != '':
            result += f'{self.main_shard}_'

        if self.secondary_shard != '':
            result += f'{self.secondary_shard}_'

        result += f'{self.color}@{self.number}'

        if self.size != '':
            result += f'-{self.size}'

        result += f'.{self.suffix}'

        return result

    @classmethod
    def get_suffix(cls, f_name) -> str:
        return f_name.rsplit('.', 1)[1]

    @classmethod
    def get_code(cls, f_name) -> str:
        return f_name.rsplit('_')[0]

    @classmethod
    def get_color(cls, f_name) -> str:
        pattern = "\_[a-z]{1,3}[\_{1}|\.{1}]"
        result = re.findall(pattern, f_name)

        if len(result) != 1:
            raise InvalidFilenameError("Invalid color")

        color = result[0].replace('_', '').replace('.', '')

        if color not in ('z', 'b', 'r', 'zb', 'zr', 'bz', 'br', 'rz', 'rb', 'zbr'):
            raise InvalidFilenameError(f'Not valid value for color: {color}')

        return color

    @classmethod
    def get_shards(cls, f_name):
        primary = ''
        secondary = ''
        pattern = '[a-z]{7}'
        result = re.findall(pattern, f_name)

        if len(result) > 0:
            primary = result[0]

        if len(result) > 1:
            secondary = result[1]

        if len(result) >= 3:
            raise InvalidFilenameError(f"Too many shards: {len(result)}")

        return primary, secondary

    @classmethod
    def get_number(cls, f_name) -> str:
        pattern = '_[0-9]{1,2}[\_|\.]{1}'
        result = re.findall(pattern, f_name)

        if len(result) < 1:
            raise InvalidFilenameError("Number not found")

        return result[0].replace('_', '').replace('.', '')

    @classmethod
    def get_size(cls, f_name) -> str:
        name_spit = f_name.rsplit('_')

        for name_part in name_spit:
            if 'x' in name_part:
                return name_part

        return ""

    def fix_code_by_color(self):
        """Update first digit based on gold color."""
        self.code = f"{GOLD_COLOR_VALUE_MAPPING[self.color[0]]}{self.code[1:]}"


def format_file(input_filename: str) -> str:
    parsed_data = FileData.from_file_name(input_filename)
    parsed_data.fix_code_by_color()

    return str(parsed_data)


def fix_files(input_folder: Path,  output_folder: Path, rename_files: bool, copy_files: bool) -> None:
    input_files: list[Path] = [path for path in input_folder.glob('**/*.png')]

    if not output_folder.exists():
        output_folder.mkdir(exist_ok=True, parents=True)

    for input_filename in input_files:
        try:
            formatted_name = format_file(input_filename.name)
            print(f'{input_filename} -> {formatted_name!r}')

            if copy_files:
                destination: Path = output_folder / formatted_name
                shutil.copy(input_filename, destination)

            if rename_files:
                input_filename.rename(input_folder / formatted_name)

        except InvalidFilenameError as exception:
            print(f'{input_filename} -> {exception} ERROR')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rename = False
    copy = False
    folder = Path('C:/Users/zuzka/Desktop/photos-all/photos1')
    folder_rename = Path('C:/Users/zuzka/Desktop/photos-all/photos1-rename')
    # fix_files(folder, folder_rename, rename, copy)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', default='.', help='Input folder with images to sort.')
    parser.add_argument('-d', '--dest', dest='dest', default='./renamed', help='Destination folder with updated images when copy is used.')
    parser.add_argument('-r', '--rename', dest='rename', default=False, action='store_true', help='Whether to rename files in place.')
    parser.add_argument('-c', '--copy', dest='copy', default=False, action='store_true', help='Whether to copy files to dest folder.')

    args = parser.parse_args()
    fix_files(Path(args.input), Path(args.dest), args.rename, args.copy)




