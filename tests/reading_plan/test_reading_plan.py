from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501
from tests.reading_plan.mocked_news import (
    mocked_news,
    expected_result_for_15_min,
    expected_empty_unreadable,
)  # type: ignore
from unittest.mock import Mock
import pytest


def test_reading_plan_group_news():
    reading_plan = ReadingPlanService()
    ReadingPlanService._db_news_proxy = Mock(return_value=mocked_news)
    response = reading_plan.group_news_for_available_time(15)
    assert response == expected_result_for_15_min

    response_empty_unreadable = reading_plan.group_news_for_available_time(5)
    assert response_empty_unreadable == expected_empty_unreadable

    with pytest.raises(ValueError):
        reading_plan.group_news_for_available_time(-10)
