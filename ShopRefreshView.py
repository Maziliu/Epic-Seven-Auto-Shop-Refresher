from Style import *
from tkinter import StringVar
from customtkinter import CTk, CTkBaseClass, CTkFrame, CTkLabel, CTkEntry, CTkButton
from ShopRefreshViewModel import ShopRefreshViewModel


class ShopRefreshView(CTkFrame):
    def __init__(self, master: CTk, viewModel: ShopRefreshViewModel):
        super().__init__(master)
        self.viewModel = viewModel
        self.viewModel.setServiceCompletionCallback(self.toggleLockableWidgets)
        self.pack()

        self.createSkystoneInputSection()
        self.createCounterSection()
        self.createButtonsSection()

    def createSkystoneInputSection(self) -> None:
        skystoneInputRowFrame = CTkFrame(self)
        skystoneInputRowFrame.pack(pady=PADDING_Y, padx=PADDING_X)

        skystoneAmountLabel = CTkLabel(
            skystoneInputRowFrame,
            text="Enter the number of skystones you want to burn: ",
            font=APP_FONT,
        )
        skystoneAmountLabel.pack(side="left", padx=PADDING_X, pady=PADDING_Y)

        self.skystoneAmountEntry = CTkEntry(
            skystoneInputRowFrame,
            textvariable=self.viewModel.skystoneInputVariable,
            validate="key",
            validatecommand=(self.register(self.isInputNumber), "%S"),
        )
        self.skystoneAmountEntry.pack(side="left", padx=PADDING_X, pady=PADDING_Y)

    def createCounterSection(self) -> None:
        countersframe = CTkFrame(self)
        countersframe.pack(pady=PADDING_Y, padx=PADDING_X)

        estimationsFrame = CTkFrame(countersframe)
        estimationsFrame.pack(side="left", padx=PADDING_X, pady=PADDING_Y)

        self.addRowToGrid(
            estimationsFrame,
            "Estimated Gold Cost:",
            self.viewModel.estimatedGold,
            COLOR_GOLD,
            0,
        )
        self.addRowToGrid(
            estimationsFrame,
            "Estimated Covenants:",
            self.viewModel.estimatedCovenants,
            COLOR_COVENANTS,
            1,
        )
        self.addRowToGrid(
            estimationsFrame,
            "Estimated Mystics:",
            self.viewModel.estimatedMystics,
            COLOR_MYSTICS,
            2,
        )

        purchasedFrame = CTkFrame(countersframe)
        purchasedFrame.pack(side="left", padx=PADDING_X, pady=PADDING_Y)

        self.addRowToGrid(
            purchasedFrame,
            "Skystones Spent:",
            self.viewModel.skystonesSpent,
            COLOR_SKYSTONES,
            0,
        )
        self.addRowToGrid(
            purchasedFrame,
            "Covenants:",
            self.viewModel.covanentsPurchased,
            COLOR_COVENANTS,
            1,
        )
        self.addRowToGrid(
            purchasedFrame,
            "Mystics:",
            self.viewModel.mysticsPurchased,
            COLOR_MYSTICS,
            2,
        )

    def createButtonsSection(self) -> None:
        buttonsFrame = CTkFrame(self)
        buttonsFrame.pack(pady=PADDING_Y, padx=PADDING_X)

        self.startButton = CTkButton(
            buttonsFrame, text="Start Refresh", command=self.startRefresh, font=APP_FONT
        )
        self.startButton.pack(side="left", padx=PADDING_X, pady=PADDING_Y)
        self.stopButton = CTkButton(
            buttonsFrame, text="Stop Refresh", command=self.stopRefresh, font=APP_FONT
        )
        self.stopButton.pack(side="left", padx=PADDING_X, pady=PADDING_Y)

        self.toggleWidgetState(self.stopButton)

    def toggleWidgetState(self, widget: CTkBaseClass) -> None:
        currentWidgetState = widget.cget("state")
        newWidgetState = "disabled" if currentWidgetState == "normal" else "normal"
        widget.configure(state=newWidgetState)

    def toggleLockableWidgets(self) -> None:
        self.toggleWidgetState(self.skystoneAmountEntry)
        self.toggleWidgetState(self.startButton)
        self.toggleWidgetState(self.stopButton)

    def startRefresh(self) -> None:
        if self.viewModel.isValidSkystoneAmount():
            self.toggleLockableWidgets()
            self.viewModel.startRefresh()

    def stopRefresh(self) -> None:
        self.toggleLockableWidgets()
        self.viewModel.stopRefresh()

    def isInputNumber(self, inputString: str) -> bool:
        return inputString.isdigit()

    def addRowToGrid(
        self,
        parentFrame: CTkFrame,
        labelText: str,
        value: StringVar,
        valueColour: str,
        gridRowIndex: int,
    ) -> None:
        CTkLabel(parentFrame, text=labelText, font=APP_FONT).grid(
            row=gridRowIndex,
            column=0,
            sticky="w",
            padx=GRID_PADDING_X,
            pady=GRID_PADDING_Y,
        )
        CTkLabel(
            parentFrame, textvariable=value, font=APP_FONT, text_color=valueColour
        ).grid(
            row=gridRowIndex,
            column=1,
            sticky="w",
            padx=GRID_PADDING_X,
            pady=GRID_PADDING_Y,
        )
