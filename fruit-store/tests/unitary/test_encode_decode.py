import datetime as dt
import pendulum as pend

import hypothesis
import hypothesis.strategies as st

from fruit_store.annot import reporting as report_annot
from fruit_store.grpc import factory as grpc_factory

grpc_dates_strategy = st.floats(
    min_value=grpc_factory.MIN_DATE.timestamp(),
    max_value=grpc_factory.MAX_DATE.timestamp(),
).map(pend.from_timestamp)


grpc_quantity = st.integers(
    min_value=grpc_factory.MIN_QUANTITY + 1,
    max_value=grpc_factory.MAX_QUANTITY - 1,
)

grpc_price = st.integers(
    min_value=grpc_factory.MIN_PRICE + 1,
    max_value=grpc_factory.MAX_PRICE - 1,
)

purchase_event_model_strategy = st.builds(
    grpc_factory.PurchaseEventModel,
    date=grpc_dates_strategy,
    quantity=grpc_quantity,
    price=grpc_price,
)


@hypothesis.given(grpc_dates_strategy)
def test_timestamp_encode_decode(dt_: "pend.DateTime"):
    "Check if conversion and de-conversion to timestamp is working adequately"
    encoded_d = grpc_factory.dt_to_ts(dt_)
    decoded_d = grpc_factory.ts_to_dt(encoded_d)
    assert dt_ == decoded_d


@hypothesis.given(purchase_event_model_strategy)
def test_event_encode_decode(purchase_event_model: "grpc_factory.PurchaseEventModel"):
    grpc_model = purchase_event_model.to_grpc()
    back_convert = grpc_factory.PurchaseEventModel.from_grpc(grpc_model)
    assert back_convert == purchase_event_model

