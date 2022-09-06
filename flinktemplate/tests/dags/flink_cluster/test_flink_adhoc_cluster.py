from os.path import exists

import pytest

from tests.conftest import AIRFLOW_HOME, DAGTestFactory

CUSTOM_OBJECTS_API_CLASS = "kubernetes.client.api.custom_objects_api.CustomObjectsApi"
CREATE_NAMESPACE_CLASS = f"{CUSTOM_OBJECTS_API_CLASS}.create_namespaced_custom_object"
DELETE_NAMESPACE_CLASS = f"{CUSTOM_OBJECTS_API_CLASS}.delete_namespaced_custom_object"
FLINK_CLUSTER_NAME = "bbasic-example"


class TestFlinkAdhocCluster(DAGTestFactory):
    @property
    def dag_id(self) -> str:
        return "flink_adhoc_workflow"

    @property
    def num_tasks(self) -> int:
        return 5

    @property
    def crd_plural(self) -> str:
        return "flinkdeployments"

    @pytest.mark.parametrize("task", ["create_flink_cluster", "flink_cluster_sensor"])
    def test_flink_crd_plural(self, task):
        assert self.dag.get_task(task).plural == self.crd_plural

    def test_create_flink_cluster(self):
        task = self.dag.get_task("create_flink_cluster")
        assert task.plural == self.crd_plural
        assert task.application_name == FLINK_CLUSTER_NAME
        if isinstance(task.application_file, str):
            exists(f"{AIRFLOW_HOME}/dags/{task.application_file}")

    def test_flink_cluster_sensor(self):
        task = self.dag.get_task("flink_cluster_sensor")

        assert task.plural == self.crd_plural

        assert task.application_name == FLINK_CLUSTER_NAME
