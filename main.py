import re
import os
import shutil
from dataclasses import dataclass


class InvalidFilenameError(Exception):
    ...


@dataclass()
class FileName:
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

    def to_string(self):
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

    def __repr__(self):
        return self.to_string()

    @classmethod
    def get_suffix(cls, f_name):
        return f_name.rsplit('.', 1)[1]

    @classmethod
    def get_code(cls, f_name):
        return f_name.rsplit('_')[0]

    @classmethod
    def get_color(cls, f_name):
        pattern = "\_[a-z]{1,2}[\_{1}|\.{1}]"
        result = re.findall(pattern, f_name)

        if len(result) != 1:
            raise InvalidFilenameError("Invalid color"
                                       "")

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
    def get_number(cls, f_name):
        pattern = '_[0-9]{1,2}[\_|\.]{1}'
        result = re.findall(pattern, f_name)
        if len(result) < 1:
            raise InvalidFilenameError("Too many shards")
        return result[0].replace('_', '').replace('.', '')

    @classmethod
    def get_size(cls, f_name):
        name_spit = f_name.rsplit('_')
        for name_part in name_spit:
            if 'x' in name_part:
                return name_part
        return ""


def format_file(f_name_in: str):
    return FileName.from_file_name(f_name_in).to_string()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rename = False
    copy = False
    folder = 'C:/Users/zuzka/Desktop/photos-all/photos1'
    folder_rename = 'C:/Users/zuzka/Desktop/photos-all/photos1-rename'

    for f_name_in in os.listdir(folder):
        try:
            formatted_name = format_file(f_name_in)
            print(f'{f_name_in} -> {formatted_name!r}')
            if rename:
                old_file = os.path.join(folder, f_name_in)
                new_file = os.path.join(folder, formatted_name)
                os.rename(old_file, new_file)
            if copy:
                old_file = os.path.join(folder, f_name_in)
                new_file = os.path.join(folder_rename, formatted_name)
                shutil.copy2(old_file, new_file)

        except InvalidFilenameError as exception:
            print(f'{f_name_in} -> {exception}')



