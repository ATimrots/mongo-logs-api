from enum import Enum

class Permission(str, Enum):
    READ = "r"
    READ_WRITE = "rw"
