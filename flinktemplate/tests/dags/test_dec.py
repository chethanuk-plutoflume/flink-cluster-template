import sys
from datetime import timedelta

from airflow.utils import timezone

DEFAULT_DATE = timezone.datetime(2016, 1, 1)
END_DATE = timezone.datetime(2016, 1, 2)
INTERVAL = timedelta(hours=12)
FROZEN_NOW = timezone.datetime(2016, 1, 2, 12, 1, 1)

TI_CONTEXT_ENV_VARS = [
    "AIRFLOW_CTX_DAG_ID",
    "AIRFLOW_CTX_TASK_ID",
    "AIRFLOW_CTX_EXECUTION_DATE",
    "AIRFLOW_CTX_DAG_RUN_ID",
]


PYTHON_VERSION = sys.version_info[0]

# Technically Not a separate virtualenv but should be good enough for unit tests
PYTHON = sys.executable


# class TestExternalPythonDecorator:
#     def test_add_dill(self, dag_maker):
#         @task.external_python(python=PYTHON, use_dill=True)
#         def f():
#             """Ensure dill is correctly installed."""
#             import dill  # noqa: F401
#
#         with dag_maker():
#             ret = f()
#
#         ret.operator.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE)
#
#     def test_fail(self, dag_maker):
#         @task.external_python(python=PYTHON)
#         def f():
#             raise Exception
#
#         with dag_maker():
#             ret = f()
#
#         with pytest.raises(CalledProcessError):
#             ret.operator.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE)
#
#     def test_with_args(self, dag_maker):
#         @task.external_python(python=PYTHON)
#         def f(a, b, c=False, d=False):
#             if a == 0 and b == 1 and c and not d:
#                 return True
#             else:
#                 raise Exception
#
#         with dag_maker():
#             ret = f(0, 1, c=True)
#
#         ret.operator.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE)
#
#     def test_return_none(self, dag_maker):
#         @task.external_python(python=PYTHON)
#         def f():
#             return None
#
#         with dag_maker():
#             ret = f()
#
#         ret.operator.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE)
#
#     def test_nonimported_as_arg(self, dag_maker):
#         @task.external_python(python=PYTHON)
#         def f(_):
#             return None
#
#         with dag_maker():
#             ret = f(datetime.datetime.utcnow())
#
#         ret.operator.run(start_date=DEFAULT_DATE, end_date=DEFAULT_DATE)
