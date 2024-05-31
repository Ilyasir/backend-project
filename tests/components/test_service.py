import pytest
from unittest.mock import patch, AsyncMock
from app.components.service import ComponentService

@pytest.mark.asyncio
@patch('app.components.service.async_session_maker', new_callable=AsyncMock)
async def test_filter_components_by_characteristics(mock_session_maker):
    mock_session = mock_session_maker.return_value.__aenter__.return_value
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    components = await ComponentService.filter_components_by_characteristics(
        type_component="GPU",
        characteristics={"brand": "NVIDIA"},
        min_price=100,
        max_price=500,
        order="1"
    )
    assert components == []

@pytest.mark.asyncio
@patch('app.components.service.async_session_maker', new_callable=AsyncMock)
async def test_add_component(mock_session_maker):
    mock_session = mock_session_maker.return_value.__aenter__.return_value
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    component_data = {
        "type": "GPU",
        "name": "RTX 3080",
        "description": "High-end GPU",
        "price": 700,
        "image_path": "path/to/image"
    }
    characteristics_data = {"brand": "NVIDIA"}

    component = await ComponentService.add_component(component_data, characteristics_data)
    assert component is not None
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()