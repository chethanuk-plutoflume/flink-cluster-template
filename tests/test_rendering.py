from pathlib import Path

import copier
import pytest

from tests.conftest import PROJECT_TEMPLATE, DATA


# @pytest.fixture
def render(tmp_path, **kwargs):
    kwargs.setdefault("quiet", True)
    copier.copy(
        str(PROJECT_TEMPLATE),
        tmp_path,
        defaults=True,
        overwrite=True,
        vcs_ref="HEAD",
        **kwargs
    )


@pytest.mark.parametrize("file", ["flink_adhoc_production.yaml", "flink_adhoc_cluster.py"])
def test_copy_k8s_op(tmp_path, file):
    render(tmp_path)
    generated = (tmp_path / f"dags/{file}").read_text()
    control = (Path(__file__).parent / f"expected/{file}").read_text()
    assert generated == control
