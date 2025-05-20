from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
import yfinance as yf
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    symbol = entry.data["symbol"].upper()
    async_add_entities([StockPriceSensor(symbol)])

class StockPriceSensor(SensorEntity):
    def __init__(self, symbol):
        self._symbol = symbol
        self._attr_name = f"{symbol} Stock Price"
        self._attr_unique_id = f"stock_price_{symbol.lower()}"
        self._attr_native_unit_of_measurement = "USD"
        self._attr_icon = "mdi:chart-line"
        self._attr_native_value = None

    async def async_update(self):
        try:
            stock = yf.Ticker(self._symbol)
            price = stock.fast_info["last_price"]
            self._attr_native_value = round(price, 2)
        except Exception as e:
            _LOGGER.warning(f"Failed to fetch stock price for {self._symbol}: {e}")
            self._attr_native_value = None