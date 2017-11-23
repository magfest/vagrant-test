import pytest
from vagrant_utils import vagrant_env, vagrant_path
import os.path


@pytest.mark.usefixtures("vagrant_env")
class TestVagrant:
    @pytest.mark.parametrize("file", [
        'sideboard/plugins/uber/README.md',
        'sideboard/plugins/uber/development.ini',
        'sideboard/plugins/guests/development.ini',
        'puppet/hiera/nodes/README.md',
        '../install.log',
    ])
    def test_files_exist(self, file):
        assert os.path.isfile(vagrant_path + file)