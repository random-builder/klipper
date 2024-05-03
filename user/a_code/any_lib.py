#
#
#

import enum
import os
import time
import tkinter
from contextlib import suppress
from dataclasses import dataclass
from tkinter import Label, simpledialog, ttk

make_host = "make_print@make1"


def invoke_xterm(plain_command:str) -> None:
    xterm_command = f"xterm -fa Monospace -fs 16 -e {plain_command}"
    assert os.system(xterm_command) == 0


def invoke_ssh_exec(remote_command:str) -> None:
    assert os.system(f"ssh '{make_host}' '{remote_command}'") == 0


def invoke_ssh_copy(source:str, target:str) -> None:
    assert os.system(f"scp '{source}' '{target}'") == 0


# override by Dialog._place_window()
def center_window(window, window_width, window_height, offset_x=0, offset_y=0):
    window.wm_attributes('-alpha', 0)  # hide window
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, 0, 0))  # 0,0 primary Screen
    window.update_idletasks()  # make sure the properties are updated
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    place_x = int((screen_width / 2) - (window_width / 2))
    place_y = int((screen_height / 2) - (window_height / 2))
    window.geometry(
        "{}x{}+{}+{}".format(
            window_width, window_height,
            place_x + offset_x,
            place_y + offset_y)
    )
    window.wm_attributes('-alpha', 1)  # show window


class SelectDialog(simpledialog.Dialog):

    def __init__(self,
            title,
            request,
            option_list,
        ):
        self.request = request
        self.option_list = option_list
        self.response = option_list[0]
        self.parent = tkinter._get_temp_root()  # @UndefinedVariable
        super().__init__(parent=self.parent, title=title)

    # override
    def body(self, frame):

        self.combo_label = Label(
            frame,
            text=self.request
        )
        self.combo_label.grid(row=0, column=0)

        self.combo_box = ttk.Combobox(
            frame,
            value=self.option_list,
            state="readonly",
            width=30,  # chars?
        )
        self.combo_box.current(0)
        self.combo_box.grid(row=1, column=0)
        self.combo_box.bind("<<ComboboxSelected>>", self.on_combo_select)

        return frame

    def on_combo_select(self, event):  # @UnusedVariable
        self.response = self.combo_box.get()


class WorkType(enum.Enum):
    Work_Verify = "Verify Local Build"
    Work_Firmware = "Update Remote Firmware"
    Work_Printer = "Update Remote Printer Config"
    Work_Totalitar = "Update Remote Firmware & Printer"

    @classmethod
    def from_value_text(self, value:str) -> "WorkType":
        return WorkType(value)

    @classmethod
    def make_value_list(self) -> list[str]:
        return list(map(lambda x: x.value, WorkType))


@dataclass
class KlipperBean:

    profile_dir:str
    profile_name:str
    flash_device_id:str

    @property
    def flash_device_path(self) -> str:
        return f"/dev/serial/by-id/{self.flash_device_id}"

    @property
    def local_repo_root(self) -> str:
        return os.popen("git rev-parse --show-toplevel").readline().strip()

    @property
    def klipper_unit(self) -> str:
        return f"make_klipper-{self.profile_name}.service"

    @property
    def klipper_data(self) -> str:
        return f"/home/make_print/{self.profile_name}/klip/data"

    @property
    def klipper_repo(self) -> str:
        return f"/home/make_print/{self.profile_name}/klip/repo"

    @property
    def source_config(self) -> str:
        return f"{self.profile_dir}/firmware.cfg"

    @property
    def target_config(self) -> str:
        return f"{self.klipper_repo}/user/{self.profile_name}/firmware.cfg"

    @property
    def source_printer(self) -> str:
        return  f"{self.profile_dir}/printer.cfg"

    @property
    def target_printer(self) -> str:
        return f"{self.klipper_repo}/user/{self.profile_name}/printer.cfg"

    @property
    def source_service_log(self) -> str:
        return f"{self.profile_dir}/service.log"

    @property
    def target_service_log(self) -> str:
        return f"{self.klipper_data}/service.log"

    def local_build_clean(self) -> None:
        print_report("local_build_clean")
        os.chdir(self.local_repo_root)
        invoke_plain(f"make KCONFIG_CONFIG={self.source_config} distclean")

    def local_build_config(self) -> None:
        print_report("local_build_config")
        os.chdir(self.local_repo_root)
        invoke_xterm(f"make KCONFIG_CONFIG={self.source_config} menuconfig")

    def local_build_make(self) -> None:
        print_report("local_build_make")
        os.chdir(self.local_repo_root)
        invoke_plain(f"make KCONFIG_CONFIG={self.source_config}")

    def remote_unit_restart(self) -> None:
        print_report("remote_unit_restart")
        invoke_ssh_exec(f"sudo systemctl stop {self.klipper_unit}")
        invoke_ssh_exec(f"rm -rf {self.target_service_log}")
        invoke_ssh_exec(f"sudo systemctl start {self.klipper_unit}")

    def remote_unit_start(self) -> None:
        print_report("remote_unit_start")
        invoke_ssh_exec(f"sudo systemctl start {self.klipper_unit}")

    def remote_unit_stop(self) -> None:
        print_report("remote_unit_stop")
        invoke_ssh_exec(f"sudo systemctl stop {self.klipper_unit}")

    def remote_repo_update(self) -> None:
        print_report("remote_repo_update")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; git reset --hard")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; git clean -f -d")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; git pull")

    def remote_build_clean(self) -> None:
        print_report("remote_build_clean")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; make KCONFIG_CONFIG={self.target_config} distclean")

    def publish_build_config(self) -> None:
        print_report("publish publish_build_config")
        invoke_ssh_copy(f"{self.source_config}", f"{make_host}:{self.target_config}")

    def publish_printer_config(self) -> None:
        print_report("publish_printer_config")
        invoke_ssh_exec(f"dirname {self.target_printer} | xargs mkdir -p")
        invoke_ssh_copy(f"{self.source_printer}", f"{make_host}:{self.target_printer}")

    def remote_build_make(self) -> None:
        print_report("remote_build_make")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; make KCONFIG_CONFIG={self.target_config}")

    def remote_build_flash(self) -> None:
        print_report("remote_build_flash")
        invoke_ssh_exec(f"cd {self.klipper_repo} ; make flash KCONFIG_CONFIG={self.target_config} FLASH_DEVICE={self.flash_device_path}")

    def perform_local_config_verify(self) -> None:
        self.local_build_clean()
        self.local_build_config()
        self.local_build_make()

    def perform_remote_build_update(self) -> None:
        self.remote_unit_stop()
        self.remote_repo_update()
        self.remote_build_clean()
        self.publish_build_config()
        self.remote_build_make()
        self.remote_build_flash()
        self.remote_unit_start()

    def perform_remote_printer_update(self) -> None:
        self.publish_printer_config()
        self.remote_unit_restart()
        self.produce_remote_printer_status()

    def produce_remote_printer_status(self) -> None:
        print_report("produce_remote_printer_status")
        time.sleep(1.5)
        invoke_ssh_copy(f"{make_host}:{self.target_service_log}", f"{self.source_service_log}")
        invoke_plain(f"cat {self.source_service_log} | grep 'Loaded MCU'")

    def perform_build_work(self) -> None:
        print_report("perform_build_work")

        select_dialog = SelectDialog(
            title=self.profile_name,
            request="Select Work Type",
            option_list=WorkType.make_value_list(),
        )

        select_value = select_dialog.response
        work_type = WorkType.from_value_text(select_value)

        match work_type:
            case WorkType.Work_Verify:
                self.perform_local_config_verify()
            case WorkType.Work_Firmware:
                self.perform_remote_build_update()
            case WorkType.Work_Printer:
                self.perform_remote_printer_update()
            case WorkType.Work_Totalitar:
                with suppress(Exception):
                    self.perform_remote_build_update()
                with suppress(Exception):
                    self.perform_remote_printer_update()
            case _:
                pass


def print_report(message:str) -> None:
    print(f"### {message} ###".upper())


def invoke_plain(command:str) -> None:
    assert os.system(command) == 0

#
#
#
