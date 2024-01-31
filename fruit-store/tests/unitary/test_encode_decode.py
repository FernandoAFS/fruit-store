import datetime as dt

import hypothesis
import hypothesis.strategies as st

from fruit_store.grpc import factory as grpc_factory

grpc_dates_strategy = st.datetimes(
    min_value=grpc_factory.MIN_DATE,
    max_value=grpc_factory.MAX_DATE,
)

purchase_event_model_strategy = st.builds(
    grpc_factory.PurchaseEventModel,
    date=grpc_dates_strategy,
    quantity=st.integers(min_value=1, max_value=(2**32 - 1)),
    price=st.integers(
        #allow_nan=False, allow_infinity=False,
        min_value=1, max_value=(2**32 - 1) // 100
    ),
)


@hypothesis.given(grpc_dates_strategy)
def test_timestamp_encode_decode(dt_: "dt.datetime"):
    "Check if conversion and de-conversion to timestamp is working adequately"
    encoded_d = grpc_factory.dt_to_ts(dt_)
    decoded_d = grpc_factory.ts_to_dt(encoded_d)
    assert dt_ == decoded_d


@hypothesis.given(purchase_event_model_strategy)
def test_event_encode_decode(purchase_event_model: "grpc_factory.PurchaseEventModel"):
    grpc_model = purchase_event_model.to_grpc()
    back_convert = grpc_factory.PurchaseEventModel.from_grpc(grpc_model)
    assert back_convert == purchase_event_model
