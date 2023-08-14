from pathlib import Path
import re
from dataclasses import dataclass


class InvalidFilenameError(Exception):
    ...


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
        main_shard = cls.get_main_shard(f_name)
        secondary_shard = cls.get_secondary_shard(f_name)
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
        result += f'{self.color}#{self.number}'

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
        pattern = "\_[a-z]{1,2}[\_{1}|\.{1}]"
        result = re.findall(pattern, f_name)

        if len(result) != 1:
            raise InvalidFilenameError("Invalid color")

        return result[0].replace('_', '').replace('.', '')

    @classmethod
    def get_main_shard(cls, f_name):
        pattern = '[a-z]{7}'
        result = re.findall(pattern, f_name)
        if len(result) < 1:
            return ""
        else:
            return result[0]

    @classmethod
    def get_secondary_shard(cls, f_name):
        pattern = '[a-z]{7}'
        result = re.findall(pattern, f_name)

        if len(result) < 2:
            return ""
        elif len(result) > 3:
            raise InvalidFilenameError("Too many shards")
        else:
            return result[1]

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


def format_file(input_filename: str) -> str:
    parsed_data = FileData.from_file_name(input_filename)
    print(parsed_data)

    return str(parsed_data)


def fix_files(input_folder: Path,  output_folder: Path, rename_files: bool, copy_files: bool) -> None:
    input_files: list[Path] = [path for path in input_folder.glob('**/*.png')]

    for input_filename in input_files:
        try:
            formatted_name = format_file(input_filename)
            print(f'{input_filename} -> {formatted_name!r}')

            if rename_files:
                input_filename.rename(input_folder / formatted_name)

            if copy_files:
                destination: Path = output_folder / formatted_name
                destination.write_bytes(input_filename.read_bytes())

        except InvalidFilenameError as exception:
            print(f'{input_filename} -> {exception} ERROR')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rename = False
    copy = False
    folder = 'C:/Users/zuzka/Desktop/photos-all/photos1'
    folder_rename = 'C:/Users/zuzka/Desktop/photos-all/photos1-rename'

    fix_files(folder, folder_rename, rename, copy)




