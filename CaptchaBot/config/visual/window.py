from termcolor import colored
import ctypes

# delete this if you are not using windows.
kernel32 = ctypes.WinDLL('kernel32')
hStdOut = kernel32.GetStdHandle(-11)
mode = ctypes.c_ulong()
kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
mode.value |= 4
kernel32.SetConsoleMode(hStdOut, mode)
# delete this if you are not using windows.

def printc(message, color):
	print(colored(message, color))    