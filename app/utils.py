from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"],deprecated = "auto")


def hash(plainpass):
    return context.hash(plainpass)

def verify(plainpass,hashpass):
    return context.verify(plainpass,hashpass)