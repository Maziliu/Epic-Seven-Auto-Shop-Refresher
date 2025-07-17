import customtkinter
import tkinter
from functools import partial
import ShopRefreshView
import ShopRefreshViewModel


if __name__ == '__main__':
    customtkinter.set_appearance_mode("System")
    app = customtkinter.CTk()
    app.geometry("1080x720")
    app.title("E7 ADB Shop Refresh")

    viewmodel = ShopRefreshViewModel.ShopRefreshViewModel()
    ShopRefreshView.ShopRefreshView(app, viewmodel)

    app.mainloop()
