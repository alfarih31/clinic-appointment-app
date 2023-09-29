from slugify import slugify


class DomainException(RuntimeError):
    def __init__(self, domain: str, code: str):
        super().__init__("%s/%s" % (slugify(domain), slugify(code)))
