import datetime as dt
import functools as ft
import itertools as it
import operator as op
import typing as t

import pytest

from fruit_store.grpc import factory as grpc_factory
from fruit_store.mem_storage import mem_storage

if t.TYPE_CHECKING:
    from fruit_store.annot import (
        data_input as di_annot,
    )


# TODO: CREATE BETTER FIXTURE THAT SUPPORTS DRY
@pytest.fixture
def purchase_event_iter() -> (
    "t.Callable[[], t.Iterable[di_annot.PurchraseEventProtocol]]"
):
    def _():
        # INTIAL DATE AND
        d0 = dt.datetime(year=2023, month=1, day=1)

        # ADDING A BUNCH OF STEPS TO GET YEARS AND MONTHS VARIETY
        days = map(dt.timedelta, range(0, 400, 15))

        # DEFINE A BUNCH OF INFINITE ITERABLES
        dates = it.cycle(map(ft.partial(op.add, d0), days))
        items = it.cycle(["papaya", "banana", "pineapple"])
        quantities = it.cycle(range(1, 10))
        prices = it.cycle(map(op.truediv, range(1, 100), it.repeat(10)))

        while True:
            yield grpc_factory.PurchaseEventModel(
                date=next(dates),
                item=next(items),
                quantity=next(quantities),
                price=next(prices),
            )

    return _


@pytest.fixture
def default_mem_store() -> "mem_storage.MemoryStorage":
    return mem_storage.MemoryStorage()


# TODO: IMPROVE, USE PARAMETERS TO TEST A VARIABLE NUMBER OF EVENTS
@pytest.mark.unit
async def test_mem_store_input_events(
    default_mem_store: "mem_storage.MemoryStorage",
    purchase_event_iter: "t.Callable[[], t.Iterable[di_annot.PurchraseEventProtocol]]",
):
    """
    Input N events to memory storage and check if internal state is consistent
    """
    N_EVENTS = 10
    events = list(it.islice(purchase_event_iter(), N_EVENTS))

    # SIMPLY FEED ALL THE EVENTS ONE BY ONE. IT'S FINE SINCE THE METHOD IS
    # SYNCHRONOUS, USE ASYNCIO.GATHER OTHERWISE
    for ev in events:
        await default_mem_store.put_purchrase_event(ev)

    # EMULATE INTERNAL STATE OPERATIONS BUT INSTEAD OF USING MUTABLE STATE USE
    # FUNCTIONAL METHODS THAT ARE MUCH EASIER TO PREDICT

    # TODO: SLICE ALL THIS ASSERTIONS IN MULTIPLE UNIT TESTS

    def flat_state_data():
        return it.chain.from_iterable(
            map(op.methodcaller("values"), default_mem_store.accum_.values())
        )

    # - UNIQUE ITEMS
    event_unique_items = set(map(op.attrgetter("item"), events))
    state_unique_items = set(default_mem_store.accum_.keys())
    assert event_unique_items == state_unique_items, "Items not present in state"

    # - TOTAL QUANTITY
    ev_total_quantity = sum(map(op.attrgetter("quantity"), events))
    st_total_quantity = sum(map(op.attrgetter("quantity"), flat_state_data()))
    assert ev_total_quantity == st_total_quantity, "Total quantity mismatch"

    # - REVENUE,
    ev_quantity = map(op.attrgetter("quantity"), events)
    ev_price = map(op.attrgetter("price"), events)
    ev_total_revenue = sum(map(op.mul, ev_quantity, ev_price))
    st_total_revenue = sum(map(op.attrgetter("revenue"), flat_state_data()))
    assert ev_total_revenue == st_total_revenue, "Total revenue mismatch"

    # - SALES
    n_sales = len(events)
    st_sales = sum(map(op.attrgetter("sales"), flat_state_data()))
    assert n_sales == st_sales, "Count sales mismatch"

    # - UNIQUE MONTHS,

    # - PER ITEM QUANTITY
    # - PER ITEM REVENUE


@pytest.mark.unit
async def test_mem_store_report(
    default_mem_store: "mem_storage.MemoryStorage",
    purchase_event_iter: "t.Callable[[], t.Iterable[di_annot.PurchraseEventProtocol]]",
):
    """
    Input N events to memory storage and check if report is consistent
    """

    N_EVENTS = 10
    events = list(it.islice(purchase_event_iter(), N_EVENTS))

    # SIMPLY FEED ALL THE EVENTS ONE BY ONE. IT'S FINE SINCE THE METHOD IS
    # SYNCHRONOUS, USE ASYNCIO.GATHER OTHERWISE
    for ev in events:
        await default_mem_store.put_purchrase_event(ev)

    report = await default_mem_store.generate_report()

    # CONVERTING GROUPED INTO A FUNCTION SINCE IT'S A COMPLEX ITERABLE.
    # IT'S EASIER THIS WAY...
    def group_items():
        s_ev = sorted(events, key=op.attrgetter("item"))
        return it.groupby(s_ev, key=op.attrgetter("item"))

    # ITEMS CHECK
    ev_unique_items = set(map(op.itemgetter(0), group_items()))
    report_unique_items = set(report.keys())
    assert ev_unique_items == report_unique_items, "Items mismatch"

    # QUANTITY CHECK
    for item, item_events in group_items():
        total_quantity = sum(map(op.attrgetter("quantity"), item_events))
        report_quantity = report[item]["total_quantity"]
        assert total_quantity == report_quantity, f"Item {item}, quantity mismatch"

    # TOTAL REVENUE CHECK AND AVERAGE PER SALE
    for item, item_events in group_items():
        items = list(item_events)  # ITEM LIST IS AN ITERABLE
        prices = map(op.attrgetter("price"), items)
        quantities = list(map(op.attrgetter("quantity"), items))
        events_revenue = sum(map(op.mul, prices, quantities))
        report_revenue = report[item]["total_revenue"]
        assert events_revenue == report_revenue, f"Item {item}, revenue mismatch"

        avg_rev_ev = sum(quantities) // len(items)
        avg_rev_report = report[item]["average_per_sale"]

        assert avg_rev_ev == avg_rev_report, f"Item {item}, average mismatch"
