from datetime import datetime, timedelta
from typing import List, Dict, Any

from application.use_cases.analytics.creating_analytics import (
    CreatingAnalyticsUseCase
)
from application.interfaces.mongo_repo import IMongoRepo


class CreatingAnalyticsInteractor(CreatingAnalyticsUseCase):
    def __init__(self, mongodb_repo: IMongoRepo):
        super().__init__(mongodb_repo)

    async def _get_user_projects(self, user_id: int):
        return await self.mongodb_repo.find(
            'projects',
            {'user_id': str(user_id)}
        )

    async def _get_task_status_stats(self, project_id: str):
        pipeline = [
            {'$match': {'project_id': project_id}},
            {'$group': {'_id': '$status', 'count': {'$sum': 1}}},
            {
                '$group': {
                    '_id': None,
                    'total': {'$sum': '$count'},
                    'statuses': {"$push": {"status": "$_id", "count": "$count"}},
                }
            },
            {
                "$project": {
                    "statuses": {
                        "$map": {
                            "input": "$statuses",
                            "as": "s",
                            "in": {
                                'status': '$$s.status',
                                'percentage': {
                                    "$multiply": [
                                        {"$divide": ["$$s.count", "$total"]},
                                        100,
                                    ]
                                },
                            },
                        }
                    }
                }
            },
        ]
        result = await self.mongodb_repo.aggregate("tasks", pipeline)
        return result[0]['statuses'] if result else []

    async def _get_total_status_count(self, project_id: int):
        pipeline = [
            {'$match': {'project_id': project_id}},
            {'$group': {'_id': '$status'}},
            {'$count"': 'total_statuses'}
        ]

        result = await self.mongodb_repo.aggregate('tasks', pipeline)
        return result[0]["total_statuses"] if result else 0

    async def _get_done_tasks_last_week(self, project_id: str) -> List[Dict[str, Any]]:
        last_week = datetime.now() - timedelta(days=7)

        pipeline = [
            {'$match': {
                'project_id': project_id,
                'status': 'DONE',
                "created_at": {"$gte": last_week}
            }},
            {'$sort': {'created_at': -1}}
        ]

        result = await self.mongodb_repo.aggregate('tasks', pipeline)
        return result

    async def _get_avg_completion_time(self, project_id: str) -> float | None:
        pipeline = [
            {'$match': {'project_id': project_id, 'due_date': {'$ne': None}}},
            {
                '$project': {
                    'completion_time': {
                        '$subtract': ['$due_date', '$created_at']
                    }
                }
            },
            {
                '$group': {
                    '_id': None,
                    'average_time': {'$avg': '$completion_time'}
                }
            }
        ]

        result = await self.mongodb_repo.aggregate('tasks', pipeline)
        return result[0]['average_time'] / (1000 * 60 * 60) if result else None

    async def create_analytics(self, user_id: int):
        projects = await self._get_user_projects(user_id)

        analytics = {
            'count_of_projects': len(projects),
            'tasks': [],
            'assignees': [],
            'statuses': []
        }

        for project in projects:
            project_id = project['id']

            tasks = await self.mongodb_repo.get_collection_count(
                'tasks',
                {'project_id': project_id}
            )
            assignees = await self.mongodb_repo.get_collection_count(
                'assignees',
                {'project_id': project_id}
            )
            statuses = await self._get_task_status_stats(project_id)

            analytics['tasks'].append(
                {'project_id': project_id, 'task_count': tasks}
            )
            analytics['assignees'].append(
                {'project_id': project_id, 'assignees': assignees}
            )
            analytics['statuses'].append(
                {'project_id': project_id, 'status': statuses}
            )

        return analytics

    async def create_tasks_statuses_analytics(self, user_id: int):
        projects = await self._get_user_projects(user_id)

        tasks_analytics = {
            'count_of_projects': len(projects),
            'tasks_statues': []
        }

        for project in projects:
            project_id = project['id']

            statuses = self._get_total_status_count(project_id)

            tasks_analytics['tasks_statues'].append(
                {'project_id': project_id, 'status': statuses}
            )

        return tasks_analytics

    async def count_ready_tasks_per_week_analytics(self, user_id: int):
        projects = await self._get_user_projects(user_id)

        ready_tasks_analytics = {
            'count_of_projects': len(projects),
            'ready_tasks': []
        }

        for project in projects:
            project_id = project['id']

            ready_tasks = await self._get_done_tasks_last_week(project_id)

            ready_tasks_analytics['ready_tasks'].append(
                {'project_id': project_id, 'status': ready_tasks}
            )

        return ready_tasks_analytics

    async def average_task_completion_time_analytics(self, user_id: int):
        projects = await self._get_user_projects(user_id)

        average_time_completion_analytics = {
            'count_of_projects': len(projects),
            'average_time': []
        }

        for project in projects:
            project_id = project['id']

            average_time = await self._get_avg_completion_time(project_id)

            average_time_completion_analytics['average_time'].append(
                {'project_id': project_id, 'average_time': average_time}
            )

        return average_time_completion_analytics