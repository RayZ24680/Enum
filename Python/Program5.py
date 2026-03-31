from enum import Enum


class ACCESSTYPE(Enum):
    READ = "READ"
    WRITE = "WRITE"
    EXECUTE = "EXECUTE"
    READ_WRITE = "READ_WRITE"
    FULL_ACCESS = "FULL_ACCESS"

    def read(self):
        if self == ACCESSTYPE.READ:
            print("Read is allowed.")
        elif self == ACCESSTYPE.READ_WRITE:
            print("Reading is allowed.")
        elif self == ACCESSTYPE.FULL_ACCESS:
            print("Reading is allowed.")
        else:
            print("ERRO: Read not allowed!")

    def write(self):
        if self == ACCESSTYPE.WRITE:
            print("Writing allowed.")
        elif self == ACCESSTYPE.READ_WRITE:
            print("Writing is allowed.")
        elif self == ACCESSTYPE.FULL_ACCESS:
            print("Writing is allowed.")
        else:
            print("ERRO: writing not allowed!")

    def execute(self):
        if self == ACCESSTYPE.EXECUTE:
            print("Executing is allowed.")
        elif self == ACCESSTYPE.FULL_ACCESS:
            print("Executing is allowed.")
        else:
            print("ERRO: Execute not allowed!")


def main():
    a = ACCESSTYPE.READ
    b = ACCESSTYPE.READ_WRITE
    c = ACCESSTYPE.FULL_ACCESS

    a.read()       # Allowed
    a.write()      # denied
    b.write()      # allowed
    b.read()       # allowed
    c.read()       # allowed
    a.execute()    # denied
    b.execute()    # denied
    c.execute()    # allowed


if __name__ == "__main__":
    main()
