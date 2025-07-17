import customtkinter

class ShopRefreshView(customtkinter.CTkFrame):
    def __init__(self, master, viewModel):
        super().__init__(master)
        self.viewModel = viewModel
        self.pack()

        skystoneInputRowFrame = customtkinter.CTkFrame(self)
        skystoneInputRowFrame.pack(pady=20, padx=20)

        skystoneAmountLabel = customtkinter.CTkLabel(skystoneInputRowFrame, text="Enter the number of skystones you want to burn: ", font=("Arial", 14))
        skystoneAmountLabel.pack(side="left", padx=(0,10))

        self.skystoneAmountEntry = customtkinter.CTkEntry(skystoneInputRowFrame, textvariable=self.viewModel.skystoneInputVar, validate="key", validatecommand=(self.register(self.isInputNumber), "%S"))
        self.skystoneAmountEntry.pack(side="left")

        resultsFrame = customtkinter.CTkFrame(self)
        resultsFrame.pack(pady=20)

        self.addRowToGrid(resultsFrame, "Esitmated Gold Cost:", self.viewModel.estimatedGoldMirrorVar, "yellow", 0)
        self.addRowToGrid(resultsFrame, "Estimated Covenants:", self.viewModel.estimatedCovenantsMirrorVar,"skyblue", 1)
        self.addRowToGrid(resultsFrame, "Estimated Mystics:", self.viewModel.estimatedMysticsMirrorVar,"red", 2)

        buttonsFrame = customtkinter.CTkFrame(self)
        buttonsFrame.pack(pady=20, padx=20)

        self.startButton = customtkinter.CTkButton(buttonsFrame, text="Start Refresh", command=self.startRefresh)
        self.startButton.pack(side="left", padx=(0,10))
        self.stopButton = customtkinter.CTkButton(buttonsFrame, text="Stop Refresh", command=self.stopRefresh)
        self.stopButton.pack(side="left")

        self.toggleWidgetState(self.stopButton)

    def toggleWidgetState(self, widget):
        currentWidgetState = widget.cget("state")
        newWidgetState = "disabled" if currentWidgetState == "normal" else "normal"
        widget.configure(state=newWidgetState)

    def startRefresh(self) -> None:
        self.toggleWidgetState(self.skystoneAmountEntry)
        self.toggleWidgetState(self.startButton)
        self.toggleWidgetState(self.stopButton)
        self.viewModel.startRefresh()

    def stopRefresh(self) -> None:
        self.toggleWidgetState(self.skystoneAmountEntry)
        self.toggleWidgetState(self.startButton)
        self.toggleWidgetState(self.stopButton)
        self.viewModel.stopRefresh()

    def isInputNumber(self, inputString: str) -> bool:
        return inputString.isdigit()
    
    def addRowToGrid(self, frame: customtkinter.CTkFrame, labelText: str, valueVariable, valueColour: str, rowNumber: int) -> None:
        customtkinter.CTkLabel(frame, text=labelText, font=("Arial", 14)).grid(row=rowNumber, column=0, sticky="w", padx=10, pady=5)
        customtkinter.CTkLabel(frame, textvariable=valueVariable, font=("Arial", 14), text_color=valueColour).grid(row=rowNumber, column=1, sticky="w", padx=10, pady=5)
