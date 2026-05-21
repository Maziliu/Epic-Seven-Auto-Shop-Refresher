import customtkinter
import subprocess
import sys

if sys.platform == "win32":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE


def getConnectedDevices():
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True,
        startupinfo=startupinfo,
    )
    devices = []
    for line in result.stdout.strip().splitlines()[1:]:
        if "\tdevice" in line:
            devices.append(line.split("\t")[0])
    return devices


class DeviceSelectorView(customtkinter.CTkToplevel):
    def __init__(self, parent, on_select):
        super().__init__(parent)
        self.on_select = on_select
        self.title("Select Emulator")
        self.resizable(False, False)
        self.grab_set()

        devices = getConnectedDevices()

        customtkinter.CTkLabel(self, text="Select a device:", font=("Arial", 14)).pack(
            padx=20, pady=(20, 8)
        )

        if not devices:
            customtkinter.CTkLabel(
                self, text="No devices found. Is ADB running?", text_color="red"
            ).pack(padx=20, pady=8)
            customtkinter.CTkButton(self, text="Close", command=self.destroy).pack(
                padx=20, pady=(0, 20)
            )
            return

        self.selected = customtkinter.StringVar(value=devices[0])

        for device in devices:
            customtkinter.CTkRadioButton(
                self,
                text=device,
                variable=self.selected,
                value=device,
            ).pack(anchor="w", padx=30, pady=4)

        customtkinter.CTkButton(self, text="Confirm", command=self._confirm).pack(
            padx=20, pady=(12, 20)
        )

    def _confirm(self):
        self.on_select(self.selected.get())
        self.destroy()
