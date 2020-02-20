import pathlib

import pytest

BASE_PATH = pathlib.Path('docssrc/source/')


def plot(path):
    _path = BASE_PATH / path
    name = _path.name
    _path = _path.parent

    def wraps(fn):
        @pytest.mark.skipif(
            (_path / (name + '.png')).exists()
            and (_path / (name + '.svg')).exists(),
            reason=f'Output plot already exists, {_path / name}'
        )
        def inner(*args, **kwargs):
            fig = fn(*args, **kwargs)
            _path.mkdir(exist_ok=True, parents=True)
            fig.savefig(str(_path / (name + '.png')))
            fig.savefig(str(_path / (name + '.svg')))
        return inner
    return wraps
