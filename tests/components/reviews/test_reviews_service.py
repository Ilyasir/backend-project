import pytest
from unittest.mock import patch, AsyncMock
from app.components.reviews.service import ReviewService

@pytest.mark.asyncio
@patch('app.components.reviews.service.async_session_maker', new_callable=AsyncMock)
async def test_create_review(mock_session_maker):
    mock_session = mock_session_maker.return_value.__aenter__.return_value
    mock_session.execute.return_value.scalar.return_value = None
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    review_data = {"rating": 5, "comment": "Great product!"}
    review = await ReviewService.create_review(1, 1, review_data)
    assert review is not None
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()