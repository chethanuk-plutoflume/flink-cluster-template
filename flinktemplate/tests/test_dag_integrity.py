"""Test the validity of all DAGs. This test ensures that all Dags have tags,
retries set to two, and no import errors. Feel free to add and remove tests."""


import pytest
from airflow.utils.dag_cycle_tester import check_cycle as cycle_dag

from tests.conftest import APPROVED_TAGS, get_import_errors, strip_path_prefix


@pytest.mark.parametrize("rel_path,rv", get_import_errors(), ids=[x[0] for x in get_import_errors()])
def test_file_imports(rel_path, rv):
    """Test for import errors on a file"""
    if rel_path and rv:
        raise Exception(f"{rel_path} failed to import with message \n {rv}")


class TestDAGIntegrity:
    @pytest.fixture(autouse=True)
    def _set_test_run_vars(self, dag_items, environment):
        (self.dag_id, self.dag) = dag_items
        self.dag_path = strip_path_prefix(self.dag.fileloc)
        self.environment = environment

    def test_dag_tags(self):
        """
        test if a DAG is tagged and if those TAGs are in the approved list
        """
        assert self.dag.tags, f"{self.dag_id} in {self.dag_path} has no tags"
        if APPROVED_TAGS:
            assert not set(self.dag.tags) - APPROVED_TAGS

    def test_dag_retries(self):
        """
        test if a DAG has retries set
        """
        assert (
            self.dag.default_args.get("retries", None) >= 3
        ), f"{self.dag_id} in {self.dag_path} does not have retries not set to 3."

    def test_dag_cycle(self):
        """
        test if a DAG has no cycles - Check to see if there are any cycles in the DAG
        NOTE: test_cycle Returns False if no cycle found
        """
        assert not cycle_dag(
            self.dag
        ), f"{self.dag_id} in {self.dag_path} has cycles in the DAG. Check all tasks names"

    def test_dag_quality(self):
        assert self.dag.tags is not None, f"{self.dag_id} in {self.dag_path} has no tags"

        assert (
            self.dag.tags != "" or self.dag.doc_md is not None
        ), f"{self.dag_id} in {self.dag_path} has no doc"
