from fastapi import FastAPI

from .http import items, users, events

app = FastAPI()


app.include_router(users.router)
app.include_router(items.router)
app.include_router(events.router)


@app.on_event("shutdown")
def shutdown_event():
    events.aio_producer.close()
