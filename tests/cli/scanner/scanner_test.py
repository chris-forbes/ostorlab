"""Unit tests for the ostorlab scanner subcommand."""
import sys

import pytest
from click import testing as click_testing
from pytest_mock import plugin

from ostorlab.cli import rootcli


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def testScannerCommandInvocation_whenDaemonCommandIsProvided_runsBackground(
    mocker: plugin.MockerFixture,
) -> None:
    """Run CLI with daemon command."""
    daemon_context_open = mocker.patch("daemon.DaemonContext.open", return_value=None)
    mocker.patch("ostorlab.cli.scanner.scanner", return_value=None)
    runner = click_testing.CliRunner()
    runner.invoke(
        rootcli.rootcli,
        ["--api-key", "test", "scanner", "--daemon", "--scanner-id", "11226"],
    )

    assert daemon_context_open.call_count == 1


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def testScannerCommandInvocation_whenDaemonCommandIsDisabled_runsConnection(
    mocker: plugin.MockerFixture,
) -> None:
    """Run CLI with --no-daemon command."""
    mocker.patch(
        "ostorlab.cli.scanner.scanner.start_scanner",
        return_value=None,
    )
    create_scan_process_mock = mocker.patch("multiprocessing.Process")

    runner = click_testing.CliRunner()
    runner.invoke(
        rootcli.rootcli,
        ["scanner", "--no-daemon", "--scanner-id", "11226DS"],
    )

    assert create_scan_process_mock.call_count == 1


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def testScannerCommandInvocation_whenParallelScanNumberIsGiven_shouldCreateCorrespondingProcesses(
    mocker: plugin.MockerFixture,
) -> None:
    """Ensure the correct number of scan processes are created."""
    create_process_mock = mocker.patch("multiprocessing.Process")

    runner = click_testing.CliRunner()
    runner.invoke(
        rootcli.rootcli,
        ["scanner", "--no-daemon", "--scanner-id", "11226DS", "--parallel", 42],
    )

    assert create_process_mock.call_count == 42


@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
def testScannerCommandInvocation_whenParallelScanNumberIsNegative_shouldExistAndShowHelpMessage(
    mocker: plugin.MockerFixture,
) -> None:
    """Ensure scanner sub-command handles the case where the number of parallel scans is negative."""
    create_process_mock = mocker.patch("multiprocessing.Process")

    runner = click_testing.CliRunner()
    result = runner.invoke(
        rootcli.rootcli,
        ["scanner", "--no-daemon", "--scanner-id", "11226DS", "--parallel", -42],
    )

    assert create_process_mock.call_count == 0
    assert result.exit_code == 2
    assert (
        "Invalid value for '--parallel': -42 is not in the range x>=1" in result.output
    )
