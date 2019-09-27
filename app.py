import wx
import random

F_STORAGE_NAME = 'strings.txt'
TAIL_MARKER = ' как приедут'

class IrinaFrame(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(IrinaFrame, self).__init__(*args, **kwargs)
		self.Center()

		captionSizerStyle = wx.EXPAND|wx.TOP

		sCaptions = wx.BoxSizer(wx.HORIZONTAL)
		pSourceCaption = wx.Panel(self, size = wx.Size(100, 20))
		wx.StaticText(pSourceCaption, label = 'Исходные данные')
		sCaptions.Add(pSourceCaption, 1, captionSizerStyle, 2)
		pResultCaption = wx.Panel(self, size = wx.Size(100, 20))
		wx.StaticText(pResultCaption, label = 'Результат')
		sCaptions.Add(pResultCaption, 1, captionSizerStyle, 2)

		defaultSizerStyle = wx.EXPAND|wx.ALL

		sTextBoxes = wx.BoxSizer(wx.HORIZONTAL)
		styleTextCtrl = wx.TE_MULTILINE|wx.TE_DONTWRAP
		self.tcSource = wx.TextCtrl(self, style = styleTextCtrl)
		self.tcResult = wx.TextCtrl(self, style = styleTextCtrl|wx.TE_READONLY)
		sTextBoxes.Add(self.tcSource, 1, defaultSizerStyle, 2)
		sTextBoxes.Add(self.tcResult, 1, defaultSizerStyle, 2)

		sButton = wx.BoxSizer(wx.HORIZONTAL)
		bRandomize = wx.Button(self, -1, 'Перемешать')
		sButton.Add(bRandomize, 1, defaultSizerStyle, 2)

		sMain = wx.BoxSizer(wx.VERTICAL)
		sMain.Add(sCaptions, 0, wx.EXPAND, 0)
		sMain.Add(sTextBoxes, 1, wx.EXPAND, 0)
		sMain.Add(sButton, 0, wx.EXPAND, 0)
		self.SetSizer(sMain)

		self.Bind(wx.EVT_BUTTON, self.onRandomizeClick, bRandomize)
		self.Bind(wx.EVT_CLOSE , self.onExitApp)

		storageLoaded = False
		try:
			with open(F_STORAGE_NAME, 'rt', encoding = 'utf-8') as f:
				for line in f:
					self.tcSource.write(line)
			storageLoaded = True
		except:
			pass

		self.CreateStatusBar()
		initialStatusText = 'Строки, кончающиеся на "' + TAIL_MARKER + '", будут в конце списка'
		if storageLoaded:
			initialStatusText += '. Загружены последние данные'
		self.SetStatusText(initialStatusText)
	# def __init__(self, *args, **kwargs):

	def onRandomizeClick(self, event):
		sList = []
		lList = []
		for i in range(self.tcSource.NumberOfLines):
			line = self.tcSource.GetLineText(i)
			if line:
				if line.endswith(TAIL_MARKER):
					lList.insert(random.randint(0, len(lList)), line)
				else:
					sList.insert(random.randint(0, len(sList)), line)

		self.tcResult.SetValue('')
		for i, line in enumerate(sList + lList, start = 1):
			self.tcResult.write(str(i) + '.\t' + line)
			self.tcResult.write('\n')

		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(self.tcResult.Value))
			self.SetStatusText('Перемешанные строки в буфере обмена, готовы к вставке')
		else:
			self.SetStatusText('Буфер обмена недоступен, скопируйте строки вручную')


	def onExitApp(self, event):
		f = open(F_STORAGE_NAME, 'wt', encoding = 'utf-8')
		for i in range(self.tcSource.NumberOfLines):
			line = self.tcSource.GetLineText(i)
			if line:
				f.write(line)
				f.write('\n')
		event.Skip()
		

# class IrinaFrame(wx.Frame):

if __name__ == '__main__':
	app = wx.App()
	fMain = IrinaFrame(None, title = 'Рандомизация строк', size = wx.Size(600, 400))
	fMain.Show()
	app.MainLoop()
