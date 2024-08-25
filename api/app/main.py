import logging
from fastapi import FastAPI
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from app.api.endpoints import hotels, hotel
from app.core.config import settings

# Configure Sentry logging integration
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

# Initialize Sentry
sentry_sdk.init(
    dsn="https://48bec4405f68878549c10c1dba4bec7d@sentry.bitbook.run/5",
    integrations=[sentry_logging],
    traces_sample_rate=1.0,  # Capture 100% of transactions for performance monitoring
)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Add Sentry middleware
app.add_middleware(SentryAsgiMiddleware)

# Include routers
app.include_router(hotels.router, prefix="/api")
app.include_router(hotel.router, prefix="/api")

# Test route for Sentry (optional)
@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    # We recommend adjusting this value in production
    traces_sample_rate=1.0,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)