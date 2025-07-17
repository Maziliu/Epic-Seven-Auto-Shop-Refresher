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

        skystoneAmountEntry = customtkinter.CTkEntry(skystoneInputRowFrame, textvariable=self.viewModel.skystoneInputVar, validate="key", validatecommand=(self.register(self.isInputNumber), "%S"))
        skystoneAmountEntry.pack(side="left")

        resultsFrame = customtkinter.CTkFrame(self)
        resultsFrame.pack(pady=20)

        self.addRowToGrid(resultsFrame, "Esitmated Gold Cost:", self.viewModel.estimatedGoldMirrorVar, "yellow", 0)
        self.addRowToGrid(resultsFrame, "Estimated Covenants:", self.viewModel.estimatedCovenantsMirrorVar,"skyblue", 1)
        self.addRowToGrid(resultsFrame, "Estimated Mystics:", self.viewModel.estimatedMysticsMirrorVar,"red", 2)

        startButton = customtkinter.CTkButton(self, text="Start Refresh", command=self.viewModel.startRefresh)
        startButton.pack()

    def isInputNumber(self, inputString: str) -> bool:
        return inputString.isdigit()
    
    def addRowToGrid(self, frame: customtkinter.CTkFrame, labelText: str, valueVariable, valueColour: str, rowNumber: int) -> None:
        customtkinter.CTkLabel(frame, text=labelText, font=("Arial", 14)).grid(row=rowNumber, column=0, sticky="w", padx=10, pady=5)
        customtkinter.CTkLabel(frame, textvariable=valueVariable, font=("Arial", 14), text_color=valueColour).grid(row=rowNumber, column=1, sticky="w", padx=10, pady=5)
