from dependency_injector import containers, providers

from application.interactors.projects.crud_projects_interactor import (
    CRUDProjectsInteractor
)
from application.interactors.tasks.crud_tasks_interactor import (
    CRUDTasksInteractor
)
from application.interactors.assignees.crud_assignees_interactor import (
    CRUDAssigneesInteractor
)
from application.interactors.analytics.creating_analytics_interactor import CreatingAnalyticsInteractor
from application.events.check_events import CheckEventsDriver
from infra.repos.mongo.mongo_repo_impl import MongoRepoImpl
from infra.repos.motor.db import MongoDBClient
from config import Config, MongoDBConfig
from infra.services.kafka.consumer import KafkaConsumer


class MongoDBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=MongoDBConfig)
    mongodb = providers.Singleton(MongoDBClient, config=config)


class Container(containers.DeclarativeContainer):
    config = providers.Factory(Config)
    mongodb = providers.Container(MongoDBContainer, config=config.provided.MONGO_CONFIG)

    mongo_repo = providers.Factory(MongoRepoImpl, db=mongodb.mongodb)

    analytic_service = providers.Factory(CreatingAnalyticsInteractor, mongodb_repo=mongo_repo)

    crud_projects_interactor = providers.Factory(
        CRUDProjectsInteractor,
        mongodb_repo=mongo_repo,
        analytic_service=analytic_service,
    )
    crud_tasks_interactor = providers.Factory(
        CRUDTasksInteractor,
        mongodb_repo=mongo_repo,
        analytic_service=analytic_service
    )
    crud_assignees_interactor = providers.Factory(
        CRUDAssigneesInteractor,
        mongodb_repo=mongo_repo
    )
    analytics_interactor = providers.Factory(
        CreatingAnalyticsInteractor,
        mongodb_repo=mongo_repo
    )
    check_events_driver = providers.Factory(
        CheckEventsDriver,
        crud_tasks_use_case=crud_tasks_interactor,
        crud_projects_use_case=crud_projects_interactor,
        crud_assignees_use_case=crud_assignees_interactor
    )

    kafka_consumer = providers.Factory(
        KafkaConsumer,
        config=config.provided.KAFKA_CONFIG,
        check_events_driver=check_events_driver
    )


container = Container()
container.init_resources()
