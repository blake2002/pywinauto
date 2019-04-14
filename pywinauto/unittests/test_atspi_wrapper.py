import os
import sys
import subprocess
import time
import unittest
import re

from ctypes import *

if sys.platform != 'win32':
    sys.path.append(".")
    from pywinauto.linux.atspi_element_info import AtspiElementInfo
    from pywinauto.linux.atspi_element_info import known_control_types
    from pywinauto.linux.application import Application
    from pywinauto.controls.atspiwrapper import AtspiWrapper

app_name = r"gtk_example.py"


def _test_app():
    test_folder = os.path.join(os.path.dirname
                               (os.path.dirname
                                (os.path.dirname
                                 (os.path.abspath(__file__)))),
                               r"apps/Gtk_samples")
    sys.path.append(test_folder)
    return os.path.join(test_folder, app_name)


def print_tree(start_el_info, level_shifter=""):
    if level_shifter == "":
        print(start_el_info.control_type, "  ", start_el_info.name, "!")
        level_shifter += "-"

    for children in start_el_info.children():
        print(level_shifter, "  ", children.control_type, "    ", children.name, "!")
        print_tree(children, level_shifter+"-")


if sys.platform != 'win32':
    class AtspiWrapperTests(unittest.TestCase):

        """Unit tests for the AtspiWrapper class"""

        def get_app(self, name):
            for children in self.desktop_info.children():
                if children.name == name:
                    return children
            else:
                raise Exception("Application not found")

        def setUp(self):
            self.desktop_info = AtspiElementInfo()
            self.desktop_wrapper = AtspiWrapper(self.desktop_info)
            self.app = Application()
            self.app.start("python3 " + _test_app())
            time.sleep(1)
            self.app_info = self.get_app(app_name)

            self.app_wrapper = AtspiWrapper(self.app_info)

        def tearDown(self):
            self.app.kill()

        def test_get_state_set(self):
            test = self.app_wrapper.get_states()

        def test_set_window_focus(self):
            self.app_wrapper.set_focus()

        def test_top_level_parent(self):
            assert self.app_wrapper.top_level_parent().element_info.control_type == "Application"

if __name__ == "__main__":
    unittest.main()
