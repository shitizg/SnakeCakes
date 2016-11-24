import wx
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from singleplayer import Singleplayer
from multiplayer import Multiplayer
from high_scores import highscores

ID_ABOUT = 101
ID_EXIT = 110


class MainMenu(wx.Frame):
    def __init__(self, parent=None, id=-1, title="Snake Cakes"):
        wx.Frame.__init__(self, parent, id, title, size=(500, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.control = wx.StaticText(self, 1, "Welcome to Snake Cakes! \n"
                                              "For information about how to play: \n\tGo to -->File and select 'About'.\n"
                                              "To Play: \n\t Go to -->Game and select an option to play.\n\n"
                                              "High-Scores are automoatically saved.",
                                     style=wx.TE_READONLY)

        #self.panel = Options(self)

        #self.Bind(wx.EVT_BUTTON, self.SinglePlayer, self.panel.single)
        #self.Bind(wx.EVT_BUTTON, self.MultiPlayer, self.panel.multi)

        self.CreateStatusBar()

        # File Menu Bar Creation
        filemenu = wx.Menu()
        menuitem = filemenu.Append(-1, "&About", "Snake Cakes Game")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuitem)
        filemenu.AppendSeparator()
        menuitem = filemenu.Append(-1, "&Exit", "Terminate the Program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuitem)

        gamemenu = wx.Menu()
        singleplayer = gamemenu.Append(-1, "&Single-Player", "Starts Single-Player SnakeCakes Game.")
        multiplayer = gamemenu.Append(-1, "&Multi-Player", "Starts Multi-Player SnakeCakes Game.")
        highscores = gamemenu.Append(-1, "&High-Scores", "Show Top 10 High Scores.")
        self.Bind(wx.EVT_MENU, self.SinglePlayer, singleplayer)
        self.Bind(wx.EVT_MENU, self.MultiPlayer, multiplayer)
        self.Bind(wx.EVT_MENU, self.HighScores, highscores)

        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        menubar.Append(gamemenu, "&Game")

        self.SetMenuBar(menubar)

        self.Show(True)

    def OnAbout(self, event):
        d = wx.MessageDialog(self,
                             "A python game using OpenGL graphics. \n Controls: \n\n\t q: to Quit Game\n\t p: to Pause Game \nPlayer1: \n\tW(Up)\n\tA(Left)\n\tS(Down)\n\tD(Right)\n \nPlayer2: \n\tI(Up)\n\tJ(Left)\n\tK(Down)\n\tL(Right)\n\nTasty cakes always show up in yellow.\nBad Cakes show up in other colors.\nThe cakes which are lies are yellow but still hurt you. \n\tOnce your health goes to zero, Game Over!\n\nCollect the cakes as the your snakes to win! \nBeware that some cakes are not as they seem. ",
                             "About Game", wx.OK)
        d.ShowModal()
        d.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def ask(self, parent=None, message='', value=''):
        dlg = wx.TextEntryDialog(parent, message, value=value)
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        return result

    def HighScores(self, event):
        scores = highscores("high-score.txt")
        d = wx.MessageDialog(self, "Top 10 High-Scores in Snake Cakes: \n\t%s" % scores.tostring(), "High-Scores", wx.OK)
        d.ShowModal()
        d.Destroy()

    def SinglePlayer(self, event):
        names = [self.ask(message='Type in your name:')]
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(Singleplayer(self, names, self.OnAppClose), 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        # self.control = SnakeCakes(self)

    def MultiPlayer(self, event):
        names = [self.ask(message='Player 1, please type in your name:'),
                 self.ask(message='Player 2, please type in your name:')]
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(Multiplayer(self, names, self.OnAppClose), 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

    def OnAppClose(self):
        global app
        glutHideWindow()
        app.ExitMainLoop()
        app.MainLoop()


class Options(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.single = wx.Button(self, label="Single-Player")
        self.multi = wx.Button(self, label="Mutli-Player")
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.single, flag=wx.BOTTOM, border=5)
        self.sizer.Add(self.multi, flag=wx.BOTTOM, border=5)
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, flag=wx.ALL | wx.EXPAND, border=5)
        self.SetSizerAndFit(self.border)


app = wx.App()
frame = MainMenu()
app.MainLoop()
del frame
del app
