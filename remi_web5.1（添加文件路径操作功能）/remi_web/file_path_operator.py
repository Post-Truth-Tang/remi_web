import os
from position_operator.position_operator import PositionJsonOperator as TQZJsonOperator


class FilePathOperator:

    @classmethod
    def current_file_path(cls):
        return os.path.abspath(__file__)

    @classmethod
    def current_file_father_path(cls):
        current_path = cls.current_file_path()
        return os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")

    @classmethod
    def current_file_grandfather_path(cls):
        current_path = cls.current_file_path()
        return os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")

    @classmethod
    def father_path(cls, source_path=None):
        return os.path.abspath(os.path.dirname(source_path) + os.path.sep + ".")

    @classmethod
    def grandfather_path(cls, source_path=None):
        return os.path.abspath(os.path.dirname(source_path) + os.path.sep + "..")


if __name__ == '__main__':
    """ FilePathOperator 测试
    print(FilePathOperator.current_file_path())
    print(FilePathOperator.current_file_father_path())
    print(FilePathOperator.current_file_grandfather_path())
    print(FilePathOperator.father_path(source_path=FilePathOperator.current_file_grandfather_path()))
    print(FilePathOperator.grandfather_path(source_path=FilePathOperator.current_file_grandfather_path()))
    """

    administrator_path = FilePathOperator.grandfather_path(source_path=FilePathOperator.current_file_grandfather_path())
    target_path = administrator_path + '\.vntrader\connect_ctp.json'

    jsonfile_content = TQZJsonOperator.tqz_load_jsonfile(jsonfile=target_path)
    print(jsonfile_content)
