import pytest
from unittest.mock import patch, AsyncMock
from app.components.characteristics.service import CharacteristicService

@pytest.mark.asyncio
@patch('app.components.characteristics.service.async_session_maker', new_callable=AsyncMock)
async def test_get_characteristics(mock_session_maker):
    mock_session = mock_session_maker.return_value.__aenter__.return_value
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    characteristics = await CharacteristicService.get_characteristics(component_id=1)
    assert characteristics == {}