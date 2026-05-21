import customtkinter
from Style import APP_APPEARANCE_MODE, APP_TITLE
from ShopRefreshView import ShopRefreshView
from ShopRefreshService import ShopRefreshService
from ShopRefreshViewModel import ShopRefreshViewModel
from DeviceSelectorView import DeviceSelectorView

if __name__ == "__main__":
    customtkinter.set_appearance_mode(APP_APPEARANCE_MODE)
    app = customtkinter.CTk()
    app.title(APP_TITLE)

    device = None

    def onDeviceSelected(id):
        global device
        device = id

    selector = DeviceSelectorView(app, on_select=onDeviceSelected)
    app.wait_window(selector)

    if not device:
        app.destroy()
        raise SystemExit

    service = ShopRefreshService(device)
    viewmodel = ShopRefreshViewModel(service)

    def onClose():
        service.stop()
        app.destroy()

    ShopRefreshView(app, viewmodel)
    app.protocol("WM_DELETE_WINDOW", onClose)
    app.mainloop()
