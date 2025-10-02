from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from containers import Container
from base_exception import BaseAppException
from infra.services.kafka.consumer import KafkaConsumer
from .projects import router as project_router
from .tasks import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_consumer: KafkaConsumer = (
        app.container.kafka_consumer()
    )
    await kafka_consumer.start()
    yield
    await kafka_consumer.stop()


def create_app(container: Container) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.container = container
    container.wire(modules=['api.projects', 'api.tasks'])
    app.include_router(project_router, prefix='/api')
    app.include_router(task_router, prefix='/api')

    return app


app = create_app(Container())


@app.exception_handler(BaseAppException)
async def base_exception_handler(request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.message
    )
