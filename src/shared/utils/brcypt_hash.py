import bcrypt


class BcryptHash:
    @staticmethod
    def generate_hash(string: str, salt_rounds: int) -> str:
        salt = bcrypt.gensalt(salt_rounds)
        string_byte = string.encode("utf-8")
        return bcrypt.hashpw(string_byte, salt).decode("utf-8")
