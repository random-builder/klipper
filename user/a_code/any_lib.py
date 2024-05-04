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


def print_report(message:str) -> None:
    print(f"### {message} ###".upper())


def invoke_plain(command:str) -> None:
    assert os.system(command) == 0


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

    Local_Verify = "Local build: Verify"
    Local_Firmware = "Local update:Firmware"
    Local_Printer = "Local update: Printer Config"

    Remote_Firmware = "Remote update:Firmware"
    Remote_Printer = "Remote update: Printer Config"
    Remote_Total_Setup = "Remote update: Firmware & Printer"

    @classmethod
    def from_value_text(self, value:str) -> "WorkType":
        return WorkType(value)

    @classmethod
    def make_value_list(self, work_type_list:list["WorkType"]) -> list[str]:
        return list(map(lambda x: x.value, work_type_list))


@dataclass
class KlipperBean:

    profile_dir:str
    profile_name:str
    flash_device_id:str

    firmware_file:str = "firmware.cfg"
    printer_file:str = "printer.cfg"
    logster_file:str = "service.log"

    @property
    def flash_device_path(self) -> str:
        return f"/dev/serial/by-id/{self.flash_device_id}"

    @property
    def local_repo_root(self) -> str:
        return os.popen("git rev-parse --show-toplevel").readline().strip()

    @property
    def klipper_service_unit(self) -> str:
        return f"make_klipper-{self.profile_name}.service"

    @property
    def klipper_data_dir(self) -> str:
        return f"/home/make_print/{self.profile_name}/klip/data"

    @property
    def klipper_repo_dir(self) -> str:
        return f"/home/make_print/{self.profile_name}/klip/repo"

    @property
    def source_firmware_cfg(self) -> str:
        return f"{self.profile_dir}/{self.firmware_file}"

    @property
    def target_firmware_cfg(self) -> str:
        return f"{self.klipper_repo_dir}/user/{self.profile_name}/{self.firmware_file}"

    @property
    def source_printer_cfg(self) -> str:
        return  f"{self.profile_dir}/{self.printer_file}"

    @property
    def target_printer_cfg(self) -> str:
        return f"{self.klipper_repo_dir}/user/{self.profile_name}/{self.printer_file}"

    @property
    def source_service_log(self) -> str:
        return f"{self.profile_dir}/{self.logster_file}"

    @property
    def target_service_log(self) -> str:
        return f"{self.klipper_data_dir}/{self.logster_file}"

    def run_local_build_clean(self) -> None:
        print_report("run_local_build_clean")
        os.chdir(self.local_repo_root)
        invoke_plain(f"make KCONFIG_CONFIG={self.source_firmware_cfg} distclean")

    def run_local_build_config(self) -> None:
        print_report("run_local_build_config")
        os.chdir(self.local_repo_root)
        invoke_xterm(f"make KCONFIG_CONFIG={self.source_firmware_cfg} menuconfig")

    def run_local_build_make(self) -> None:
        print_report("run_local_build_make")
        os.chdir(self.local_repo_root)
        invoke_plain(f"make KCONFIG_CONFIG={self.source_firmware_cfg}")

    def run_local_build_flash(self) -> None:
        print_report("run_local_build_flash")
        os.chdir(self.local_repo_root)
        invoke_plain(f"make flash KCONFIG_CONFIG={self.source_firmware_cfg} FLASH_DEVICE={self.flash_device_path}")

    def remote_unit_restart(self) -> None:
        print_report("remote_unit_restart")
        invoke_ssh_exec(f"sudo systemctl stop {self.klipper_service_unit}")
        invoke_ssh_exec(f"rm -rf {self.target_service_log}")
        invoke_ssh_exec(f"sudo systemctl start {self.klipper_service_unit}")

    def remote_unit_start(self) -> None:
        print_report("remote_unit_start")
        invoke_ssh_exec(f"sudo systemctl start {self.klipper_service_unit}")

    def remote_unit_stop(self) -> None:
        print_report("remote_unit_stop")
        invoke_ssh_exec(f"sudo systemctl stop {self.klipper_service_unit}")

    def remote_repo_update(self) -> None:
        print_report("remote_repo_update")
        invoke_ssh_exec(f"cd {self.klipper_repo_dir} ; git reset --hard")
        invoke_ssh_exec(f"cd {self.klipper_repo_dir} ; git clean -f -d")
        invoke_ssh_exec(f"cd {self.klipper_repo_dir} ; git pull")

    def run_remote_build_clean(self) -> None:
        print_report("run_remote_build_clean")
        invoke_ssh_exec(f"cd {self.klipper_repo_dir} ; make KCONFIG_CONFIG={self.target_firmware_cfg} distclean")

    def publish_build_config(self) -> None:
        print_report("publish publish_build_config")
        invoke_ssh_copy(f"{self.source_firmware_cfg}", f"{make_host}:{self.target_firmware_cfg}")

    def publish_printer_config(self) -> None:
        print_report("publish_printer_config")
        invoke_ssh_exec(f"dirname {self.target_printer_cfg} | xargs mkdir -p")
        invoke_ssh_copy(f"{self.source_printer_cfg}", f"{make_host}:{self.target_printer_cfg}")

    def run_remote_build_make(self) -> None:
        print_report("run_remote_build_make")
        invoke_ssh_exec(f"cd {self.klipper_repo_dir} ; make KCONFIG_CONFIG={self.target_firmware_cfg}")

    def run_remote_build_flash(self) -> None:
        print_report("run_remote_build_flash")
        invoke_ssh_exec(f"cd {self.klipper_repo_dir} ; make flash KCONFIG_CONFIG={self.target_firmware_cfg} FLASH_DEVICE={self.flash_device_path}")

    def perform_local_build_verify(self) -> None:
        self.run_local_build_clean()
        self.run_local_build_config()
        self.run_local_build_make()

    def perform_local_firmware_update(self) -> None:
        self.run_local_build_clean()
        self.run_local_build_make()
        self.run_local_build_flash()

    def perform_local_printer_verify(self) -> None:
        printer_cfg = self.source_printer_cfg
        logger_file = f"{self.profile_dir}/printer-verify.log"
        socket_file = f"{self.profile_dir}/printer-verify.tty"
        repo_root = self.local_repo_root
        if os.path.exists(logger_file): os.remove(logger_file)
        klipper_command = f"\
            /usr/bin/python \
            {repo_root}/klippy/klippy.py {printer_cfg} \
            --logfile    {logger_file} \
            --input-tty  {socket_file} \
        "
        invoke_plain(klipper_command)

    def perform_remote_firmware_update(self) -> None:
        self.remote_unit_stop()
        self.remote_repo_update()
        self.run_remote_build_clean()
        self.publish_build_config()
        self.run_remote_build_make()
        self.run_remote_build_flash()
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

    def select_work_type(self, work_type_list:list[WorkType]) -> WorkType:
        option_list = WorkType.make_value_list(work_type_list)
        select_dialog = SelectDialog(
            title=self.profile_name,
            request="Select Work Type",
            option_list=option_list,
        )
        select_value = select_dialog.response
        work_type = WorkType.from_value_text(select_value)
        return work_type

    def perform_main_work(self) -> None:
        print_report("perform_main_work")
        option_list = [
            WorkType.Local_Verify,
            WorkType.Remote_Firmware,
            WorkType.Remote_Printer,
            WorkType.Remote_Total_Setup
        ]
        work_type = self.select_work_type(option_list)
        match work_type:
            case WorkType.Local_Verify:
                self.perform_local_build_verify()
            case WorkType.Remote_Firmware:
                self.perform_remote_firmware_update()
            case WorkType.Remote_Printer:
                self.perform_remote_printer_update()
            case WorkType.Remote_Total_Setup:
                with suppress(Exception):
                    self.perform_remote_firmware_update()
                with suppress(Exception):
                    self.perform_remote_printer_update()
            case _:
                pass

    def perform_test_work(self) -> None:
        print_report("perform_test_work")
        option_list = [
            WorkType.Local_Verify,
            WorkType.Local_Firmware,
            WorkType.Local_Printer,
        ]
        work_type = self.select_work_type(option_list)
        match work_type:
            case WorkType.Local_Verify:
                self.perform_local_build_verify()
            case WorkType.Local_Firmware:
                self.perform_local_firmware_update()
            case WorkType.Local_Printer:
                self.perform_local_printer_verify()
            case _:
                pass

#
#
#
