from UVATool.Structure import Structure


class StructFile:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def getStructure(self) -> Structure:
        file_name = self.file_name
        import sys
        from os.path import isfile, basename, dirname, abspath
        if not isfile(file_name):
            raise Exception('File not Exist!')
        path = abspath(dirname(file_name))
        sys.path.append(path)
        module_name = basename(file_name)[:-3]
        struct = __import__(module_name)
        for i in dir(struct):
            item = getattr(struct, i)
            if isinstance(item, Structure):
                return item
        raise Exception('This file not contains a Structure!')
