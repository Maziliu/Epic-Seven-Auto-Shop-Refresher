# Epic Seven ADB Shop Refresher

<div align="center">
  <img src="adb-assets/E7%20Shop%20Refresh%20Demo.gif" alt="E7 ADB Shop Refresher Demo" width="700">
</div>

## Important Notice

This project is **Windows only** and works **exclusively with Android emulators** that have ADB enabled. It will not work with the official Epic Seven client on PC or mobile devices. If you need a shop refresher for the official PC client, visit the original project by [Solunium](https://github.com/Solunium/Epic-Seven-E7-Secret-Shop-Refresh):

**[Epic Seven E7 Secret Shop Refresh - Original Project](https://github.com/Solunium/Epic-Seven-E7-Secret-Shop-Refresh)**

Also, use at your own risk. I am not responsible for any account penalties or bans that may result from using this tool. Always follow the game's Terms of Service.

## What is this project?

This is a GUI wrapper around the ADB shop refresh functionality from the original project. It provides an easy-to-use interface for automating shop refreshes in Epic Seven when running the game on Android emulators.

## Requirements

- **Android Emulator** (BlueStacks, LDPlayer, etc.)
- **ADB (Android Debug Bridge)** enabled on your emulator
- **1920x1080** emulator resolution

## Download & Run

1. **Download the E7ADBShopRefresher.exe** from the [Releases Page](https://github.com/Maziliu/Epic-Seven-Auto-Shop-Refresher/releases)
2. **Have Epic Seven open** at either the lobby or already in the secret shop
3. **Make sure ADB (Android debug bridge)** is enabled on your emulator
4. **Make sure the enumalor resolution** is 1920x1080
5. **Run the executable**

## Known Issue

If your emulator or PC is slow or if the emulator freezes randomly then, the shop refresher's actions may be executed faster than the emulator can respond to. When this happens the shop refresher will take multiple attempts to buy a summon or refresh and for each time it does it will increment the counters even if it only actually buys it once. It is important to note that I have not seen the program skip a summon because of this but it is not entirely impossible. Personally, all I've seen this do is make the refresher terminate early (it will say it spent the target amount and terminate even if in reality it spent less due to lag). The original project helps the user mitigate this by allowing the user to change the speed of the refresher but my GUI does not since I do not see this very often. This may or may not change in the future.

## Manual Compilation

If you want to manually compile this project use the following command:

```
pyinstaller --windowed --onefile --noconsole --icon=adb-assets/icon.ico --name=E7ADBShopRefresher --add-data "adb-assets;adb-assets" src/main.py
```
