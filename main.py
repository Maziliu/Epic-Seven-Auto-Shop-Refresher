import customtkinter
from Style import APP_APPEARANCE_MODE, APP_TITLE
from ShopRefreshView import ShopRefreshView
from ShopRefreshService import ShopRefreshService
from ShopRefreshViewModel import ShopRefreshViewModel

if __name__ == "__main__":
    customtkinter.set_appearance_mode(APP_APPEARANCE_MODE)
    app = customtkinter.CTk()
    app.title(APP_TITLE)

    service = ShopRefreshService()
    viewmodel = ShopRefreshViewModel(service)
    ShopRefreshView(app, viewmodel)

    def onClose():
        service.stop()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", onClose)
    app.mainloop()
