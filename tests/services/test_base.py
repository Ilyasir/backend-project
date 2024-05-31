import pytest
from unittest.mock import patch, AsyncMock
from app.services.base import BaseService
from app.components.models import Component

class TestService(BaseService):
    model = Component

@pytest.mark.asyncio
@patch('app.services.base.async_session_maker', new_callable=AsyncMock)
async def test_find_one_or_none(mock_session_maker):
    mock_session = mock_session_maker.return_value.__aenter__.return_value
    mock_session.execute.return_value.scalar.return_value = None
    
    result = await TestService.find_one_or_none(id=1)
    assert result is None