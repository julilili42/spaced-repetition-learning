from rich.console import Console
from srl.commands.list_ import get_due_problems
import argparse


def positive_int(value: str) -> int:
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "take",
        help="Output a problem by problem number",
    )
    parser.add_argument(
        "number",
        type=positive_int,
        help="Problem number from `srl list`",
    )
    parser.add_argument(
        "-u",
        "--url",
        action="store_true",
        help="Output the problem URL instead of the name",
    )
    parser.set_defaults(handler=handle)
    return parser


def handle(args, console: Console):
    url_requested: bool = getattr(args, "url", False)
    index: int = args.number
    if index <= 0:
        return
    due_problems = get_due_problems()

    if index > len(due_problems):
        console.print(f"[red]Invalid problem number:[/red] {index}")
        return

    problem, url = due_problems[index - 1]

    if url_requested and not url:
        console.print(f"[red]No URL found for '{problem}'.[/red]")
        return

    if url_requested:
        console.print(url)
    else:
        console.print(problem)
