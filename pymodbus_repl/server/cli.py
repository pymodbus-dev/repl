"""Repl server cli."""
import functools
import inspect
import shutil
from collections import defaultdict
from typing import Dict, Optional

import click
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.shortcuts.progress_bar import formatters
from prompt_toolkit.styles import Style
from pymodbus import __version__ as pymodbus_version
from tabulate import tabulate

from pymodbus_repl import __VERSION__ as repl_version
from pymodbus_repl.lib.completer import CmdCompleter
from pymodbus_repl.lib.helper import Command, style
from pymodbus_repl.lib.reactive import (
    ReactiveServer,
)


TITLE = r"""
__________                          .______.                    _________
\______   \___.__. _____   ____   __| _/\_ |__  __ __  ______  /   _____/ ______________  __ ___________
 |     ___<   |  |/     \ /  _ \ / __ |  | __ \|  |  \/  ___/  \_____  \_/ __ \_  __ \  \/ // __ \_  __ \\
 |    |    \___  |  Y Y  (  <_> ) /_/ |  | \_\ \  |  /\___ \   /        \  ___/|  | \/\   /\  ___/|  | \/
 |____|    / ____|__|_|  /\____/\____ |  |___  /____//____  > /_______  /\___  >__|    \_/  \___  >__|
           \/          \/            \/      \/           \/          \/     \/                 \/
                                                                                                v{}-Pymodbus{}
"""

SMALL_TITLE = "Pymodbus server..."
BOTTOM_TOOLBAR = HTML(
    '(MODBUS SERVER) <b><style bg="ansired">Press Ctrl+C or '
    'type "exit" to quit</style></b> Type "help" '
    "for list of available commands"
)
COMMAND_ARGS = ["response_type", "error_code", "delay_by", "clear_after", "data_len"]
RESPONSE_TYPES = ["normal", "error", "delayed", "empty", "stray"]
COMMANDS: Dict[str, Optional[Dict | Command]] = {
    "manipulator": {
        "response_type": None,
        "error_code": None,
        "delay_by": None,
        "clear_after": None,
    },
    "config": None,
    "exit": None,
    "help": None,
    "clear": None,
}
USAGE = (
    "manipulator response_type=|normal|error|delayed|empty|stray \n"
    "\tAdditional parameters\n"
    "\t\terror_code=&lt;int&gt; \n\t\tdelay_by=&lt;in seconds&gt; \n\t\t"
    "clear_after=&lt;clear after n messages int&gt;"
    "\n\t\tdata_len=&lt;length of stray data (int)&gt;\n"
    "\n\tExample usage: \n\t"
    "1. Send error response 3 for 4 requests\n\t"
    "   <ansiblue>manipulator response_type=error error_code=3 clear_after=4</ansiblue>\n\t"
    "2. Delay outgoing response by 5 seconds indefinitely\n\t"
    "   <ansiblue>manipulator response_type=delayed delay_by=5</ansiblue>\n\t"
    "3. Send empty response\n\t"
    "   <ansiblue>manipulator response_type=empty</ansiblue>\n\t"
    "4. Send stray response of length 12 and revert to normal after 2 responses\n\t"
    "   <ansiblue>manipulator response_type=stray data_len=11 clear_after=2</ansiblue>\n\t"
    "5. To disable response manipulation\n\t"
    "   <ansiblue>manipulator response_type=normal</ansiblue>"
)
COMMAND_HELPS = {
    "manipulator": f"Manipulate response from server.\nUsage: {USAGE}",
    "config": "Print server config",
    "clear": "Clears screen",
    "exit": "Exits REPL Server",
}


def manipulator_to_dict(response_type: str = 'normal', error_code: Optional[int] = None,
                        delay_by: Optional[float] = None,
                        clear_after: Optional[int] = None) -> dict:
    """
    Manipulate response from the server.

    :param response_type: |normal|error|delayed|empty|stray|
    :param error_code: Modbus error code to return
    :param delay_by: Delay the response by given time (IN SECONDS)
    :param clear_after: Clear the manipulated response after a given time (IN SECONDS).

    """
    return {
        "response_type": response_type,
        "error_code": error_code,
        "delay_by": delay_by,
        "clear_after": clear_after
    }


def config_options_to_dict(show_server_context: bool = False):
    """
    Show server context.

    :param show_server_context: Show server context.
    """
    return {
        "context": show_server_context
    }


STYLE = Style.from_dict({"": "cyan"})
CUSTOM_FORMATTERS = [
    formatters.Label(suffix=": "),
    formatters.Bar(start="|", end="|", sym_a="#", sym_b="#", sym_c="-"),
    formatters.Text(" "),
    formatters.Text(" "),
    formatters.TimeElapsed(),
    formatters.Text("  "),
]

MANIP_COMMAND = Command("manipulator", inspect.signature(manipulator_to_dict), inspect.getdoc(manipulator_to_dict))
COMMANDS["manipulator"] = MANIP_COMMAND
COMMANDS["config"] = Command("config", inspect.signature(config_options_to_dict),
                             inspect.getdoc(config_options_to_dict))


def info(message):
    """Show info."""
    if not isinstance(message, str):
        message = str(message)
    click.secho(message, fg="green")


def warning(message):
    """Show warning."""
    click.secho(str(message), fg="yellow")


def error(message):
    """Show error."""
    click.secho(str(message), fg="red")


def get_terminal_width():
    """Get terminal width."""
    return shutil.get_terminal_size()[0]


def print_help(command: Optional[str] = None):
    """Print help."""

    def _print_formatted(cmd: str, hlp: str):
        print_formatted_text(
            HTML(f"<skyblue>{cmd:45s}</skyblue><seagreen>{hlp:100s}</seagreen>")
        )

    def _print_help():
        print_formatted_text(HTML("<u>Available commands:</u>"))
        for cmd, hlp in sorted(COMMAND_HELPS.items()):
            _print_formatted(cmd, hlp)

    if command:
        hlp = COMMAND_HELPS.get(command)
        if not hlp:
            _print_help()
        else:
            _print_formatted(command, hlp)
    else:
        _print_help()


def print_server_config(server: ReactiveServer, print_server_context: bool = False, *extra):
    """Print server config."""
    print_formatted_text()
    print_formatted_text(HTML("<u>Server Configs:</u>"))
    server_configs = {
        "web_ip": server._host,
        "web_port": server._port,
    }
    server_configs.update(server.manipulator_config)
    for config, val in server_configs.items():
        print_formatted_text(
            HTML(f"<skyblue>{config:45s}</skyblue><seagreen>{val!s:100s}</seagreen>")
        )

    if print_server_context:
        context = server._modbus_server.context._slaves
        configs = defaultdict(list)

        for slave, ctx in context.items():
            configs["units"].append(slave)
            for t, s in ctx.store.items():
                configs[t].append(f"{s.address} - {len(s.values)}")

        print_formatted_text()
        print_formatted_text(HTML("<u>Slave/Unit Info:</u>"))
        print_formatted_text(
            HTML(
                f"<seagreen>{tabulate(configs, headers='keys')}</seagreen>"
            )
        )


def print_title():
    """Print title - large if there are sufficient columns, otherwise small."""
    col = get_terminal_width()
    max_len = max(  # pylint: disable=consider-using-generator
        [len(t) for t in TITLE.split("\n")]
    )
    title = TITLE.format(repl_version, pymodbus_version)
    if col > max_len:
        info(title)
    else:
        print_formatted_text(
            HTML(f'<u><b><style color="green">{SMALL_TITLE}</style></b></u>')
        )


def handle_manipulator_command(server, *args):
    """Handle manipulator repl command."""
    if len(args) == 1:
        print_help("manipulator")
    else:
        val_dict = _process_args(args)
        if val_dict:  # pylint: disable=consider-using-assignment-expr
            server.update_manipulator_config(val_dict)


async def interactive_shell(server):
    """Run CLI interactive shell."""
    print_title()
    info("")
    completer = CmdCompleter(commands=COMMANDS)
    command_map = {
        "help": print_help,
        "clear": clear,
        "config": functools.partial(print_server_config, server),
        "exit": server.web_app.shutdown,
        "manipulator": functools.partial(handle_manipulator_command, server)
    }
    session = PromptSession(
        "SERVER > ", completer=completer, bottom_toolbar=BOTTOM_TOOLBAR, style=style
    )

    # Run echo loop. Read text from stdin, and reply it back.
    while True:
        try:
            result = await session.prompt_async()
            command = result.split()
            if command:
                if command[0] not in COMMANDS:
                    warning(f"Invalid command or invalid usage of command - {command}")
                    continue
                fn = command_map[command[0]]
                if command[0] == "exit":
                    await fn()
                    break
                else:
                    fn(*command[1:])
                    continue
        except (EOFError, KeyboardInterrupt):
            return


def _process_args(args) -> dict:
    """Process arguments passed to CLI."""
    val_dict = {}
    for index, arg in enumerate(args):
        if "=" in arg:
            key, value = arg.split("=")
        elif index + 1 < len(args) and arg in COMMAND_ARGS:
            key = arg
            value = args[index + 1]
        else:
            continue

        if key == "response_type" and value not in RESPONSE_TYPES:
            warning(f"Invalid response type request - {value}")
            warning(f"Choose from {RESPONSE_TYPES}")
            continue
        try:
            if key in ["clear_after", "data_len", "error_code"]:
                value = int(value)
            elif key == "delay_by":
                value = float(value)
        except ValueError:
            warning(f"Expected integer value for {key}")
            continue

        val_dict[key] = value
    return val_dict


async def main(server):
    """Run main."""
    # with patch_stdout():
    try:
        await interactive_shell(server)
    finally:
        pass
    warning("Bye Bye!!!")


async def run_repl(server):
    """Run repl server."""
    await main(server)
