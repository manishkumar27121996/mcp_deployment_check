# from fastmcp import FastMCP
# import os 
# mcp= FastMCP(name="My SSE Server")

# @mcp.tool()
# def add_numbers(a: int, b: int) -> int:
#     """Add two numbers."""
#     return a + b
# @mcp.tool()
# def subtract_numbers(a: int, b: int) -> int:
#     """Subtract two numbers."""
#     return a - b

# @mcp.tool()
# def multiply_numbers(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b
# @mcp.tool()
# def divide_numbers(a: int, b: int) -> float:
#     """Divide two numbers."""
#     if b == 0:
#         raise ValueError("Cannot divide by zero.")
#     return a / b
# app = mcp.streamable_http_app()
# if __name__ == "__main__":
#     #mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
#     mcp.run(transport="streamable-http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
#---------------------------------------------------------------------------------------------------------------------------------------------------
# from typing import Any
# import httpx
# from fastmcp import FastMCP
# import os 
# #from fastapi import FastAPI
# # Initialize FastMCP server
# mcp = FastMCP("weather")

# # Constants
# NWS_API_BASE = "https://api.weather.gov"
# USER_AGENT = "weather-app/1.0"

# async def make_nws_request(url: str) -> dict[str, Any] | None:
#     """Make a request to the NWS API with proper error handling."""
#     headers = {
#         "User-Agent": USER_AGENT,
#         "Accept": "application/geo+json"
#     }
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers, timeout=30.0)
#             response.raise_for_status()
#             return response.json()
#         except Exception:
#             return None

# def format_alert(feature: dict) -> str:
#     """Format an alert feature into a readable string."""
#     props = feature["properties"]
#     return f"""
# Event: {props.get('event', 'Unknown')}
# Area: {props.get('areaDesc', 'Unknown')}
# Severity: {props.get('severity', 'Unknown')}
# Description: {props.get('description', 'No description available')}
# Instructions: {props.get('instruction', 'No specific instructions provided')}
# """

# @mcp.tool()
# async def get_alerts(state: str) -> str:
#     """Get weather alerts for a US state.

#     Args:
#         state: Two-letter US state code (e.g. CA, NY)
#     """
#     url = f"{NWS_API_BASE}/alerts/active/area/{state}"
#     data = await make_nws_request(url)

#     if not data or "features" not in data:
#         return "Unable to fetch alerts or no alerts found."

#     if not data["features"]:
#         return "No active alerts for this state."

#     alerts = [format_alert(feature) for feature in data["features"]]
#     return "\n---\n".join(alerts)

# @mcp.tool()
# async def get_forecast(latitude: float, longitude: float) -> str:
#     """Get weather forecast for a location.

#     Args:
#         latitude: Latitude of the location
#         longitude: Longitude of the location
#     """
#     # First get the forecast grid endpoint
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_nws_request(points_url)

#     if not points_data:
#         return "Unable to fetch forecast data for this location."

#     # Get the forecast URL from the points response
#     forecast_url = points_data["properties"]["forecast"]
#     forecast_data = await make_nws_request(forecast_url)

#     if not forecast_data:
#         return "Unable to fetch detailed forecast."

#     # Format the periods into a readable forecast
#     periods = forecast_data["properties"]["periods"]
#     forecasts = []
#     for period in periods[:5]:  # Only show next 5 periods
#         forecast = f"""
# {period['name']}:
# Temperature: {period['temperature']}°{period['temperatureUnit']}
# Wind: {period['windSpeed']} {period['windDirection']}
# Forecast: {period['detailedForecast']}
# """
#         forecasts.append(forecast)

#     return "\n---\n".join(forecasts)
# app = mcp.streamable_http_app()
# # http_app = mcp.http_app()                         # Streamable HTTP (/mcp)
# # sse_app = mcp.http_app(transport="sse")

# # app = FastAPI(lifespan=http_app.lifespan)
# # app.mount("/mcp", http_app)
# # app.mount("/sse", sse_app)


# if __name__ == "__main__":
#     # Initialize and run the server
#     #import uvicorn
#     mcp.run(transport="streamable-http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
#     #uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT",8000)))
#------------------------------------------------------------------------------------------------------------------------------------
from typing import Any
import httpx
from fastmcp import FastMCP
from fastapi import FastAPI
import os

# Initialize FastMCP
mcp = FastMCP("weather")

# NWS constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Weather alert helper
async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# MCP tools
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(f) for f in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location."""
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data."

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch forecast."

    periods = forecast_data["properties"]["periods"]
    forecasts = [
        f"""{p['name']}:
Temperature: {p['temperature']}°{p['temperatureUnit']}
Wind: {p['windSpeed']} {p['windDirection']}
Forecast: {p['detailedForecast']}""" for p in periods[:5]
    ]
    return "\n---\n".join(forecasts)

# FastAPI app with route mounting
http_app = mcp.http_app(transport="streamable-http")  # <- Crucial for POST /mcp/ to work

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MCP Weather Server is up!"}

# Mount MCP under /mcp
app.mount("/mcp", http_app)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))




