import time
from datetime import timedelta

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from operators.flink_kubernetes import FlinkKubernetesOperator
from pendulum import datetime
from sensors.flink_kubernetes import FlinkKubernetesSensor


@task(task_id="sleep_5min")
def wait_5min(seconds, ds=None, **kwargs) -> None:
    print(f"Sleeping for 5 minutes and ds: {ds}")
    time.sleep(seconds)
    return None


# When using the DAG decorator, the "dag" argument doesn't need to be specified for each task.
# The "dag_id" value defaults to the name of the function it is decorating if not explicitly set.
# In this example, the "dag_id" value would be "example_dag_advanced".
@dag(
    # This DAG is set to run for the first time on June 11, 2021. Best practice is to use a static start_date.
    # Subsequent DAG runs are instantiated based on scheduler_interval below.
    start_date=datetime(2022, 6, 7),
    # This defines how many instantiations of this DAG (DAG Runs) can execute concurrently. In this case,
    # we're only allowing 1 DAG run at any given time, as opposed to allowing multiple overlapping DAG runs.
    max_active_runs=1,
    # This defines how often your DAG will run, or the schedule by which DAG runs are created. It can be
    # defined as a cron expression or custom timetable. This DAG will run daily.
    schedule_interval=None,
    # Default settings applied to all tasks within the DAG; can be overwritten at the task level.
    default_args={
        "owner": "chethanuk",  # This defines the value of the "owner" column in the DAG view of the Airflow UI
        "retries": 3,  # If a task fails, it will retry 2 times.
        "retry_delay": timedelta(minutes=3),  # A task that fails will wait 3 minutes to retry.
    },
    default_view="graph",  # This defines the default view for this DAG in the Airflow UI
    # When catchup=False, your DAG will only run for the latest schedule interval. In this case, this means
    # that tasks will not be run between June 11, 2021 and 1 day ago. When turned on, this DAG's first run
    # will be for today, per the @daily schedule interval
    catchup=False,
    # If set, this tag is shown in the DAG view of the Airflow UI
    tags=["flink_cluster", 'flink_adhoc_cluster'],
)
def flink_adhoc_cluster_workflow():
    """
    ### Flink Cluster DAG
    Flink Dag to manage Flink Cluster
    """

    print_date = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    create_flink_cluster = FlinkKubernetesOperator(
        task_id="create_flink_cluster",
        # kubernetes_conn_id="kube_conn_id",
        namespace="default",
        application_file="flink_adhoc_production.yaml",
        do_xcom_push=True,
    )

    flink_cluster_sensor = FlinkKubernetesSensor(
        task_id="flink_cluster_sensor",
        application_name=flink-adhoc-cluster,
    )

    notify = EmptyOperator(task_id="send_notifications")

    print_date >> create_flink_cluster >> wait_5min(300) >> flink_cluster_sensor >> notify


flink_workflow_dag = flink_adhoc_cluster_workflow()
