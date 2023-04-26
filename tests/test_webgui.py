import pytest
from icecream import ic

# Various dash testing utilities
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

from dash import dcc
from long.webgui.base import update_user_id_dropdown, get_tl_cmoc_checklist


@pytest.fixture
@pytest.mark.parametrize(
    "ds_random",
    "ds_gptchat",
)
def changed_datasource(ds_name):
    context_value.set(
        AttributeDict(**{"triggered_inputs": [{"datasource_name": ds_name}]})
    )


@pytest.fixture
def changed_user():
    pass


def test_callback_update_datasource():
    """
    Changing datasource should change
    - userlist
    - available cmocs
    """
    pass


def test_callback_update_user():
    """
    Changing user should change
    - timeline
    - table
    """
    pass


@pytest.mark.parametrize(
    "ds_name,user_prefix",
    [
        ("random_data", "random_user"),
        ("gptchat_by_thread", "gptchat_user"),
    ],
)
def test_update_user_id_dropdown(ds_name, user_prefix):
    """
    The user_id_dropdown should be updated when the datasource is changed
    """
    # Change datasource
    user_id_dropdown = update_user_id_dropdown(ds_name)

    # Check the prefix of the first username in the user_id_dropdown matches the new datasource
    assert isinstance(user_id_dropdown, dcc.Dropdown)
    actual_name = user_id_dropdown.value
    assert actual_name.startswith(user_prefix)


def test_callback_update_timeline():
    """
    timeline can be updated by any of these events
    -
    """
    pass


def test_callback_update_table():
    """
    table can be updated by any of these events
    -
    """
    pass


@pytest.mark.parametrize(
    "ds_name,cmoc_method_count,cmoc_method_prefix",
    [
        ("random_data", 6, "random"),
        ("gptchat_by_thread", 0, "GPTChat"),
    ],
)
def test_callback_update_cmoc_checklist_datasource(
    ds_name, cmoc_method_count, cmoc_method_prefix
):
    """
    The CMOC checklist can be updated by any of these events
    - new datasource (reset list of cmocs, and they should all be deselected)
    - when the selection changes. The item that has been selected/deselected will trigger the event, but we need to preserve the state of all of the other items in the list.

    This test checks the first case
    """
    # Change datasource
    # Ensure that we start with at least one item selected
    previous_selection = dcc.Checklist(
        options=["a,b,c"],
        value=["a"],
    )

    cmoc_checklist = get_tl_cmoc_checklist(None, ds_name, previous_selection)

    # Check that we have the right number of cmoc methods
    assert isinstance(cmoc_checklist, dcc.Checklist)
    assert len(cmoc_checklist.options) == cmoc_method_count

    # Check names of cmoc methods
    for cmoc_method in cmoc_checklist.options:
        assert cmoc_method["value"].startswith(cmoc_method_prefix)

    # Check that all of the items are deselected
    assert cmoc_checklist.value == []


def test_callback_update_cmoc_checklist_selection():
    """
    The CMOC checklist can be updated by any of these events
    - new datasource (reset list of cmocs, and they should all be deselected)
    - when the selection changes. The item that has been selected/deselected will trigger the event, but we need to preserve the state of all of the other items in the list.

    This test checks the second case
    """
    pytest.fail("Not implemented yet")
