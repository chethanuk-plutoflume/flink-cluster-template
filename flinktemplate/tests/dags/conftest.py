import pytest
from airflow.exceptions import BackfillUnfinished
from airflow.executors.debug_executor import DebugExecutor
from airflow.models.dag import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.utils.db import create_default_connections
from airflow.utils.session import provide_session
from airflow.utils.state import State
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from tests.conftest import DEFAULT_DATE


def run_dag(dag: DAG, account_for_cleanup_failure=False):
    """

    :param dag: DAG
    :param account_for_cleanup_failure: Since our cleanup task fails on purpose when running in 'single thread mode'
    we account for this by running the backfill one more time if the cleanup task is the ONLY failed task. Otherwise
    we just passthrough the exception.
    :return:
    """
    dag.clear(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, dag_run_state=State.NONE)
    try:
        dag.run(
            executor=DebugExecutor(),
            start_date=DEFAULT_DATE,
            end_date=DEFAULT_DATE,
            run_at_least_once=True,
        )
    except BackfillUnfinished as b:
        if not account_for_cleanup_failure:
            raise b
        failed_tasks = b.ti_status.failed

        if len(failed_tasks) != 1 or list(failed_tasks)[0].task_id != "cleanup":
            raise b
        ti_key = list(failed_tasks)[0]

        # Cleanup now that everything is done
        ti = TaskInstance(task=dag.get_task("cleanup"), run_id=ti_key.run_id)
        ti = ti.task.execute({"ti": ti, "dag_run": ti.get_dagrun()})


RETRY_ON_EXCEPTIONS = []


@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(RETRY_ON_EXCEPTIONS),
    wait=wait_exponential(multiplier=10, min=10, max=60),  # values in seconds
)
def wrapper_run_dag(dag):
    run_dag(dag, account_for_cleanup_failure=True)


@provide_session
def get_session(session=None):
    create_default_connections(session)
    return session


@pytest.fixture()
def session():
    return get_session()
