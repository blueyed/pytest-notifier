"""pytest-notifier - A pytest plugin to notify test result"""
from time import time

import pytest
from _pytest.main import EXIT_INTERRUPTED

from .notifier import notify


def pytest_addoption(parser):
    """
    Adds options to control notifications.
    """
    group = parser.getgroup('terminal reporting')
    group.addoption(
        '--notifier',
        dest='notifier',
        default=True,
        help='Enable test result notifications.',
    )
    group.addoption(
        '--notifier-onzero-title',
        dest='notifier_onzero_title',
        default='py.test',
        help='Notifier title when no tests were run.',
    )
    group.addoption(
        '--notifier-onpass-title',
        dest='notifier_onpass_title',
        default='py.test',
        help='Notifier title when tests pass.',
    )
    group.addoption(
        '--notifier-onfail-title',
        dest='notifier_onfail_title',
        default='py.test',
        help='Notifier title when tests fail.',
    )
    group.addoption(
        '--notifier-oninterrupt-title',
        dest='notifier_oninterrupt_title',
        default='py.test - interrupted',
        help='Notifier title when tests are interrupted (e.g. Ctrl-C).',
    )


def get_msg_part(count, group):
    if not count:
        return None
    if group in ('passed', 'failed'):
        suffix = group.title()
    elif group == 'deselected':
        suffix = 'Skipped'
    elif group == 'error':
        suffix = 'Error(s)'
    return '{} {}'.format(count, suffix)


class Notifier:
    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        self.exitstatus = exitstatus

    @pytest.hookimpl(trylast=True)
    def pytest_terminal_summary(self, terminalreporter):
        if not terminalreporter.config.option.notifier:
            return

        tr = terminalreporter
        duration = time() - tr._sessionstarttime
        keys = ('passed', 'failed', 'error', 'deselected')
        counts = {
            k: len(list(filter(lambda r: getattr(r, 'when', '') == 'call', tr.stats.get(k, []))))
            for k in keys
        }

        if self.exitstatus == EXIT_INTERRUPTED:
            title = terminalreporter.config.option.notifier_oninterrupt_title
            # TODO: same as with last "else", refactor?
            msg = ' '.join(filter(None, (
                get_msg_part(count=counts[k], group=k) for k in keys)))
        elif sum(counts.values()) == 0:
            title = terminalreporter.config.option.notifier_onzero_title
            msg = 'No tests ran'
        elif counts['passed'] and not (counts['failed'] or counts['error']):
            title = terminalreporter.config.option.notifier_onpass_title
            msg = 'Success - {passed} Passed'.format(**counts)
        else:
            title = terminalreporter.config.option.notifier_onfail_title
            msg = ' '.join(filter(None, (
                get_msg_part(count=counts[k], group=k) for k in keys)))

        msg += ' in {:.2f}s'.format(duration)
        notify(title, msg)


def pytest_configure(config):
    notifier = Notifier()
    config.pluginmanager.register(notifier, '_notifier')
