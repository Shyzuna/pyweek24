"""
Title: dialog File
Desc: Dialog object to used to display text
Creation Date: 21/10/17
LastMod Date: 21/10/17
TODO:
*
"""

import os
import settings.settings as settings

class Dialog(object):
    """
    I am a dialog
    """
    def __init__(self, file):
        """
        Init the dialog
        """
        self.content = []
        with open(os.path.join(settings.DIALOGS_PATH, file + ".dialog")) as dialogFile:
            line = dialogFile.readline()
            while line:
                line = line.rstrip()
                author,text,time = line.split('|')
                self.content.append({
                    "author": author,
                    "text": text,
                    "time": int(time)
                })
                line = dialogFile.readline()

        self.played = False
        self.isPlaying = False
        self.currentDial = 0
        self.currentTime = 0

    def play(self, guiManager):
        """
        Play a dialog if not already played
        :return: Nothing
        """
        if not self.played and not self.isPlaying:
            self.isPlaying = True
            text = "{}: {}".format(self.content[self.currentDial]["author"],self.content[self.currentDial]["text"])
            guiManager.textBuffer.renderText(text)

    def update(self, guiManager, deltaTime):
        """
        Update dialog
        :param guiManager:
        :param deltaTime:
        :return:
        """
        if self.isPlaying:
            self.currentTime += deltaTime
            if self.currentTime > self.content[self.currentDial]["time"]:
                self.currentDial += 1
                self.currentTime = 0
                if self.currentDial >= len(self.content):
                    self.played = True
                    self.isPlaying = False
                else:
                    text = "{}: {}".format(self.content[self.currentDial]["author"], self.content[self.currentDial]["text"])
                    guiManager.textBuffer.renderText(text)