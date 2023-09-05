from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501
from tests.reading_plan.mocked_news import (
    mocked_news,
    expected_result_for_15_min,
)  # type: ignore
from unittest.mock import Mock
import pytest


def test_reading_plan_group_news():
    reading_plan = ReadingPlanService()
    reading_plan._db_news_proxy = Mock(return_value=mocked_news)
    result = reading_plan.group_news_for_available_time(15)
    assert result == expected_result_for_15_min

    reading_plan2 = ReadingPlanService()
    with pytest.raises(ValueError):
        reading_plan2.group_news_for_available_time(-10)
