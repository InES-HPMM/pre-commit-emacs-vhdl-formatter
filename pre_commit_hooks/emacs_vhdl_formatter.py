#!/usr/bin/env python
"""Format VHDL files with emacs.

Calls Emacs in batch mode as a subprocess and communicates via
stdin/stdout
"""

__author__ = "Thierry Delafontaine (deaa@zhaw.ch)"
__copyright__ = "2022 ZHAW Institute of Embedded Systems"
__date__ = "2022-12-20"

import argparse
import logging
import subprocess
import sys

from ._version import __version__


class Config:
    """Default configuration."""

    cmd = "emacs"
    base_args = ["--batch", "--eval"]
    lisp_code = '(let (vhdl-file-content next-line) (while (setq next-line (ignore-errors (read-from-minibuffer ""))) (setq vhdl-file-content (concat vhdl-file-content next-line "\n"))) (with-temp-buffer (vhdl-mode) {} (setq vhdl-basic-offset {}) (insert vhdl-file-content) (vhdl-beautify-region (point-min) (point-max)) (princ (buffer-string))))'  # noqa: E501


def main() -> int:
    """Call emacs as a subprocess."""
    parser = _build_parser()
    args = parser.parse_args(sys.argv[1:])

    lisp_code = construct_lisp_code(
        tab_width=args.tab_width, custom_eval=args.custom_eval
    )
    cmd = [Config.cmd]
    cmd += Config.base_args
    cmd.append(lisp_code)

    num_files_formatted = 0
    for filename in args.filenames:
        with open(filename, "r+") as f:
            with subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ) as proc:
                try:
                    file_content = f.read()
                    formatted_code, errs = proc.communicate(input=file_content)
                    if proc.returncode == 0:
                        logging.debug(formatted_code)
                        f.seek(0)
                        f.truncate()
                        f.write(formatted_code)
                        logging.info(f"{filename} successfully formatted")
                        if file_content != formatted_code:
                            num_files_formatted += 1
                    else:
                        logging.error(f"{errs}")

                except subprocess.TimeoutExpired:
                    proc.kill()
                    _, errs = proc.communicate()
                    logging.error(f"Subprocess timed out: {errs}")
                    return proc.returncode
    return num_files_formatted


def construct_lisp_code(tab_width: int, custom_eval: str) -> str:
    """Constructs the evaluated lisp code.

    Arguments:
        tab_width: number fo spaces per indentation level
        custom_eval: custom lisp code which gets evaluated before the formatting

    Returns: A string containing the lisp code.
    """
    return Config.lisp_code.format(custom_eval, tab_width)


def _build_parser() -> argparse.ArgumentParser:
    """Constructs the parser for the command line arguments.

    Returns: An ArgumentParser instant.
    """
    parser = argparse.ArgumentParser(
        prog="emacs-vhdl-formatter",
        description="Format your VHDL files with emacs.",
    )

    parser.add_argument(
        "filenames",
        metavar="<filename>",
        type=str,
        nargs="+",
        help="Files to process",
    )
    parser.add_argument(
        "--custom-eval",
        metavar="'(lisp-code)'",
        type=str,
        default="",
        help="Custom lisp code which gets evaluated before the formatting",
    )

    parser.add_argument(
        "--tab-width",
        metavar="4",
        type=int,
        default=4,
        help="Number of spaces per indentation level. Defaults to 4",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser


if __name__ == "__main__":
    main()
