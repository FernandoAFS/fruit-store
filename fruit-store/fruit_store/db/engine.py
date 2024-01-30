import sqlalchemy as sqa

engine = sqa.create_engine("sqlite://", check_same_thread=True)
