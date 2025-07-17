import customtkinter
import tkinter
from functools import partial
import ShopRefreshView
import ShopRefreshViewModel
import ShopRefreshService

if __name__ == '__main__':
    customtkinter.set_appearance_mode("System")
    app = customtkinter.CTk()
    app.geometry("1080x720")
    app.title("E7 ADB Shop Refresh")

    service = ShopRefreshService.ShopRefreshService()
    viewmodel = ShopRefreshViewModel.ShopRefreshViewModel(service)
    ShopRefreshView.ShopRefreshView(app, viewmodel)

    app.mainloop()
