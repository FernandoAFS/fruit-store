import sqlalchemy as sqa

metadata = sqa.Metadata()


user = sqa.Table(
    "purchrases",
    metadata,
    sqa.Column("id", sqa.Integer, primary_key=True, autoincrement=True),
    sqa.Column("date", sqa.Date(), nullable=False),
    sqa.Column("item", sqa.String(50), nullable=False),
    sqa.Column("quantity", sqa.Integer(), nullable=False),
    sqa.Column("price", sqa.Integer(), nullable=False),
)
