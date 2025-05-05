import win32com.client as win32
import os
import re
import markdown

hwp = win32.gencache.EnsureDispatch('HWPFrame.HwpObject')
hwp.XHwpWindows.Item(0).Visible = True
hwp.XHwpWindows.Item(0).SetTitle("Markdown to HWP")
hwp.XHwpWindows.Item(0).SetSize(800, 600)
hwp.XHwpWindows.Item(0).SetPos(100, 100)
hwp.XHwpWindows.Item(0).SetFont("Arial", 12)
hwp.XHwpWindows.Item(0).SetTextColor(0, 0, 0)
hwp.XHwpWindows.Item(0).SetBackgroundColor(255, 255, 255)
hwp.XHwpWindows.Item(0).SetLineSpacing(1.5)
hwp.XHwpWindows.Item(0).SetParagraphSpacing(12)
hwp.XHwpWindows.Item(0).SetAlignment(0)
hwp.XHwpWindows.Item(0).SetIndent(0)
hwp.XHwpWindows.Item(0).SetFirstLineIndent(0)

hwp.Run("FileNew")
hwp.Run("InsertText")
hwp.Run("InsertText", "Markdown to HWP")
hwp.Run("InsertText", "\n")
hwp.Run("InsertText", "This is a test of the HWP API.")
hwp.Run("InsertText", "\n")
hwp.Run("InsertText", "This is a test of the HWP API.")

