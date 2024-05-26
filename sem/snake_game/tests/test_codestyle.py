"""imports"""
import inspect
import pytest
from pylint.lint import Run
from pylint.reporters import CollectingReporter

from src import game, config, game_objects, grid, helpers


@pytest.mark.parametrize("file_name", [game, config, game_objects, grid, helpers])
def test_codestyle(file_name):
    """ Evaluate codestyle """
    src_file = inspect.getfile(file_name)
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    # E1101 no-member (otherwise throws false positive errors because pygame members are created dynamically)
    # E0611 no-name-in-module (simillar as above, false positive error when importing Vector2)
    r = Run(['--disable=C0301,C0103,E1101,E0611', '-sn', src_file],
            reporter=rep, exit=False)
    linter = r.linter

    print('\nLinter output:')
    for m in linter.reporter.messages:
        print(f'{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}')
    score = linter.stats.global_note

    print(f'pylint score = {score}')
    assert score >= 10
