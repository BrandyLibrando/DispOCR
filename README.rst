DispOCR - Electronic Display OCR Tool
=====================================
**An OCR solution using PaddlePaddle for recognizing text and numbers from electronic displays, all through a dedicated graphical interface.** 

Allows selection of region of interest (ROI), as well as automatic data logging based on a configurable frequency. Also incorporates text correction using both SymSpell and LanguageTool.

The project also allows executing custom Python scripts based on whether a given condition is met in the OCR-detected text or numerical data. This can be used in a variety of use cases, from automating software-based processes to controlling external hardware through RPi GPIOs.

Can work with different webcams, but has specialized support for Luxonis OAK cameras to adjust camera configurations such as focus and exposure.

-------------------------------------

Created in fulfillment of thesis requirements. Intended system is Raspberry Pi 5, tested on Raspberry Pi 5, Windows 11, and Linux x64 (Debian & Arch) environments. GUI program and components written in Python 3.10 and QML (Qt 6.9). Built and distributed using PySide6 and Briefcase.

*Source code for the whole project authored by Julius Alvin Librando.*
