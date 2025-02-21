# SPDX-License-Identifier: GPL-2.0

import os
import subprocess
import time
from pathlib import Path


def base_path():
    """Returns the base path for the project"""
    return Path(__file__).parent.parent.parent


def test_path():
    """Returns the path to the tests directory"""
    return os.path.join(base_path(), "tests/integration")


def podman_compose_path():
    """Returns the path to the podman compose script"""
    return os.path.join(base_path(), "podman_compose.py")


class RunSubprocessMixin:
    def is_debug_enabled(self):
        return "TESTS_DEBUG" in os.environ

    def run_subprocess(self, args):
        begin = time.time()
        if self.is_debug_enabled():
            print("TEST_CALL", args)
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        if self.is_debug_enabled():
            print("TEST_CALL completed", time.time() - begin)
            print("STDOUT:", out.decode('utf-8'))
            print("STDERR:", err.decode('utf-8'))
        return out, err, proc.returncode

    def run_subprocess_assert_returncode(self, args, expected_returncode=0):
        out, err, returncode = self.run_subprocess(args)
        decoded_out = out.decode('utf-8')
        decoded_err = err.decode('utf-8')
        self.assertEqual(
            returncode,
            expected_returncode,
            f"Invalid return code of process {returncode} != {expected_returncode}\n"
            f"stdout: {decoded_out}\nstderr: {decoded_err}\n",
        )
        return out, err
