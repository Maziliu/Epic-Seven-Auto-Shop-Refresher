import customtkinter
import tkinter
from functools import partial

def isInputNumber(inputString: str) -> bool:
    return inputString.isdigit()

def onInputChange(inputStringVar, mirrorStringVar, convertCurrency, *args):
    currentValue = inputStringVar.get()
    if currentValue.isdigit():
        skystones = int(currentValue)
        result = convertCurrency(skystones)
        mirrorStringVar.set(f"{result:,}")
    else:
        mirrorStringVar.set("0")

def convertToGoldCost(skystoneAmount: int) -> int:
    return int(round(skystoneAmount * 1691.04536 * 2))

def convertToEstimatedCovenents(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * 0.006603509 * 2))

def convertToEstimatedMystics(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * 0.001700646 * 2))

if __name__ == '__main__':
    customtkinter.set_appearance_mode("System")
    app = customtkinter.CTk()
    app.geometry("1080x720")
    app.title("E7 ADB Shop Refresh")

    skystoneInputVar = tkinter.StringVar()
    estimatedGoldMirrorVar = tkinter.StringVar(value="0")
    estimatedCovenentsMirrorVar = tkinter.StringVar(value="0")
    estimatedMysticsMirrorVar = tkinter.StringVar(value="0")

    skystoneInputVar.trace_add("write", partial(onInputChange, skystoneInputVar, estimatedGoldMirrorVar, convertToGoldCost))
    skystoneInputVar.trace_add("write", partial(onInputChange, skystoneInputVar, estimatedCovenentsMirrorVar, convertToEstimatedCovenents))
    skystoneInputVar.trace_add("write", partial(onInputChange, skystoneInputVar, estimatedMysticsMirrorVar, convertToEstimatedMystics))

    skystoneInputRowFrame = customtkinter.CTkFrame(app)
    skystoneInputRowFrame.pack(pady=20, padx=20)

    skystoneAmountLabel = customtkinter.CTkLabel(skystoneInputRowFrame, text="Enter the number of skystones you want to burn: ", font=("Arial", 14))
    skystoneAmountLabel.pack(side="left", padx=(0,10))

    skystoneAmountEntry = customtkinter.CTkEntry(skystoneInputRowFrame, textvariable=skystoneInputVar, validate="key", validatecommand=(app.register(isInputNumber), "%S"))
    skystoneAmountEntry.pack(side="left")

    resultsFrame = customtkinter.CTkFrame(app)
    resultsFrame.pack(pady=20)

    estimatedGoldCostLabel = customtkinter.CTkLabel(resultsFrame, text="Estimated Gold Cost:", font=("Arial", 14))
    estimatedGoldCostLabel.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    estimatedGoldCostLabel = customtkinter.CTkLabel(resultsFrame, textvariable=estimatedGoldMirrorVar, font=("Arial", 14), text_color="yellow")
    estimatedGoldCostLabel.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    estimatedCovenantsLabel = customtkinter.CTkLabel(resultsFrame, text="Estimated Covenants:", font=("Arial", 14))
    estimatedCovenantsLabel.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    estimatedCovenantsValueLabel = customtkinter.CTkLabel(resultsFrame, textvariable=estimatedCovenentsMirrorVar, font=("Arial", 14), text_color="skyblue")
    estimatedCovenantsValueLabel.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    estimatedMysticsLabel = customtkinter.CTkLabel(resultsFrame, text="Estimated Mystics:", font=("Arial", 14))
    estimatedMysticsLabel.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    estimatedMysticValueLabel = customtkinter.CTkLabel(resultsFrame, textvariable=estimatedMysticsMirrorVar, font=("Arial", 14), text_color="red")
    estimatedMysticValueLabel.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    startButton = customtkinter.CTkButton(app, text="Start")
    startButton.pack()
    app.mainloop()
