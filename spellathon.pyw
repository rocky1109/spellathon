import sys
from random import randint
from PyQt4.QtCore import *
from PyQt4.QtGui import *
Signal = pyqtSignal


class Game(QDialog):
	
	gameName = "SPELLATHON"
	alphaList = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
	gameDist = {1 : [2, 8] , 2 : [3, 6], 3: [3, 4], 4: [4, 2], 5: [4, 3], 6:[4, 3], 7: [5, 2], 8: [5, 3]}
	fixedList = []
	varList = []
	presentList = []
	absentList = []
	score = 0
	acceptedList = Signal(QStringList)
	gameLevel = None
	repeats = 1
	minThreshold = 18
	maxThreshold = 60
	possibleWords = []
	
	def __init__(self, parent=None):
		
		super(Game, self).__init__(parent)
		self.sortOrder = Qt.AscendingOrder
		
		self.dictWords = []
		
		self.makeDisplay()
		self.formLayout()
		
		self.openFileAndGetWords()
		self.setWindowTitle(self.gameName)
	
	def openFileAndGetWords(self):
		
		dictFile = open("words.txt","r")
		
		for lines in dictFile.readlines():
			line = [lines.strip("\n")]
			self.dictWords.append(str(line[0]))
	
	
	def makeDisplay(self):
		
		# Adding banners
		
		self.gameBanner			= QLabel("<font color=red size=72><b>"+self.gameName+"</b></font>")
		self.fixedBanner		= QLabel("<font color=blue><h3> Fixed alphabets : </h3></font>")
		self.varBanner			= QLabel("<font color=blue><h3> Variable alphabets alphabets : </h3></font>")
		self.fixedAlphaList		= QLabel()
		self.varAlphaList		= QLabel()
		self.levelBanner		= QLabel("<font color=black> <h2> Level : "+str(self.gameLevel)+"</h2></font>")
		self.scoreBanner		= QLabel("<font color=black> <h2> Score : "+str(self.score)+"</h2></font>")
		self.copyrightBanner	= QLabel("Spellathon, Copyright "+u'\u00A9'+" 2015 <br>Rocky <a href=\"mailto:riverdale1109@gmail.com\">riverdale1109@gmail.com </a>")
		
		self.gameBanner.setAlignment(Qt.AlignCenter)
		self.copyrightBanner.setAlignment(Qt.AlignCenter)
		
		# Display container
		self.listWidget			= QListWidget()
		self.resultWidget		= QTextBrowser()
		self.possibleWidget		= QTextBrowser()
		
		# Operational buttons
		self.addButton			= QPushButton("&Add...") 
		self.editButton			= QPushButton("&Edit...") 
		self.deleteButton		= QPushButton("&Delete...") 
		self.upButton			= QPushButton("&Up") 
		self.downButton			= QPushButton("D&own") 
		self.sortButton			= QPushButton("&Sort") 
		self.cleanButton		= QPushButton("&Clean") 
		self.submitButton		= QPushButton("Submi&t") 
		self.nextButton			= QPushButton("&Next") 
		
		# Button click events
		self.addButton.clicked.connect(self.add)
		self.editButton.clicked.connect(self.edit)
		self.deleteButton.clicked.connect(self.delete)
		self.upButton.clicked.connect(self.up)
		self.downButton.clicked.connect(self.down)
		self.sortButton.clicked.connect(self.sort)
		self.cleanButton.clicked.connect(self.clean)
		self.submitButton.clicked.connect(self.submit)
		self.nextButton.clicked.connect(self.next_)
		self.nextButton.setEnabled(False)
	
	
	def formLayout(self):
		
		# Building Layout
		vLay = QVBoxLayout()
		scoreNlevelLay = QHBoxLayout()
		alphaLay = QGridLayout()
		contentLay = QHBoxLayout()
		bottomButtonLay = QHBoxLayout()
		buttonLay = QGridLayout()
		
		scoreNlevelLay.addWidget(self.levelBanner)
		scoreNlevelLay.addWidget(self.scoreBanner)
		
		alphaLay.addWidget(self.fixedBanner,0,0)
		alphaLay.addWidget(self.fixedAlphaList,0,1)
		alphaLay.addWidget(self.varBanner,1,0)
		alphaLay.addWidget(self.varAlphaList, 1,1)
		
		contentLay.addWidget(self.listWidget)
		contentLay.addWidget(self.resultWidget)
		contentLay.addWidget(self.possibleWidget)
		
		buttonLay.addWidget(self.addButton,0,0)
		buttonLay.addWidget(self.editButton,0,1)
		buttonLay.addWidget(self.deleteButton,0,2)
		buttonLay.addWidget(self.upButton,1,0)
		buttonLay.addWidget(self.downButton,1,1)
		buttonLay.addWidget(self.sortButton,1,2)
		buttonLay.addWidget(self.cleanButton,2,0)
		buttonLay.addWidget(self.submitButton,2,1)
		buttonLay.addWidget(self.nextButton,2,2)
		
		bottomButtonLay.addLayout(buttonLay)
		
		vLay.addWidget(self.gameBanner)
		vLay.addWidget(self.HLine())
		vLay.addWidget(self.HLine())
		vLay.addLayout(alphaLay)
		vLay.addWidget(self.HLine())
		vLay.addLayout(scoreNlevelLay)
		vLay.addWidget(self.HLine())
		vLay.addLayout(contentLay)
		vLay.addWidget(self.HLine())
		vLay.addLayout(bottomButtonLay)
		vLay.addWidget(self.HLine())
		vLay.addWidget(self.copyrightBanner)
		
		self.setLayout(vLay)
				
		
	def HLine(self):
		t = QFrame()
		t.setFrameShape(QFrame.HLine)
		t.setFrameShadow(QFrame.Sunken)
		return t
		
			
	def add(self):
		row = self.listWidget.currentRow()
		title = "Add {0}".format(self.gameName)
		string, ok = QInputDialog.getText(self, title, title)
		
		if not self.listWidget.findItems(string, Qt.MatchExactly):
				if ok and not string.isEmpty():
					self.listWidget.insertItem(row, string)
		else:
			QMessageBox.warning(self, "Spellathon",
			"Item already exists!",
			QMessageBox.Ok )
		
			
	def edit(self):
		row = self.listWidget.currentRow()
		item = self.listWidget.item(row)
		if item is not None:
			title = "Edit {0}".format(self.gameName)
			string, ok = QInputDialog.getText(self, title, title,
						QLineEdit.Normal, item.text())
			if not self.listWidget.findItems(string, Qt.MatchExactly):
				if ok and not string.isEmpty():
					item.setText(string)
			else:
				QMessageBox.warning(self, "Spellathon",
				"Item already exists!",
				QMessageBox.Ok )
		
			
	def delete(self):
		row = self.listWidget.currentRow()
		item = self.listWidget.item(row)
		if item is None:
			return
		reply = QMessageBox.question(self, "Remove {0}".format(
				self.gameName), "Remove {0} `{1}'?".format(
				self.name, unicode(item.text())),
				QMessageBox.Yes|QMessageBox.No)
	
		if reply == QMessageBox.Yes:
			item = self.listWidget.takeItem(row)
			del item
			
	def up(self):
		row = self.listWidget.currentRow()
		if row >= 1:
			thisItem = self.listWidget.item(row)
			prevItem = self.listWidget.item(row - 1)
			text = thisItem.text()
			thistem.setText(prevItem.text())
			prevItem.setText(text)
			self.listWidget.setCurrentItem(prevItem)
			
	def down(self):
		row = self.listWidget.currentRow()
		if row < self.listWidget.count() - 1:
			thisItem = self.listWidget.item(row)
			nextItem = self.listWidget.item(row + 1)
			text = thisItem.text()
			thisItem.setText(nextItem.text())
			nextItem.setText(text)
			self.listWidget.setCurrentItem(nextItem)
			
	def sort(self):
		self.listWidget.sortItems(self.sortOrder)
		if self.sortOrder == Qt.AscendingOrder:
			self.sortOrder = Qt.DescendingOrder
		else:
			self.sortOrder = Qt.AscendingOrder
			
	def submit(self):
		
		self.addButton.setEnabled(False)
		self.editButton.setEnabled(False)
		self.deleteButton.setEnabled(False)
		self.upButton.setEnabled(False)
		self.downButton.setEnabled(False)
		self.sortButton.setEnabled(False)
		self.cleanButton.setEnabled(False)
		self.submitButton.setEnabled(False)
		self.nextButton.setEnabled(True)
		
		self.stringList = QStringList()
		for row in range(self.listWidget.count()):
			self.stringList.append(self.listWidget.item(row).text())
		
		self.presentList = []
		self.absentList = []
		
		# Find the word from dictionary file
		for item in self.stringList:
			if self.possibleWords.count(item) > 0:
				self.presentList.append(item)
			else:
				self.absentList.append(item)
				
		# add the results to listWidgets
		for item in self.presentList:
			#row = self.listWidget.currentRow()
			self.resultWidget.append("<font color=green>" +str(item)+"</font>")
			
		for item in self.absentList:
			#row = self.listWidget.currentRow()
			self.resultWidget.append("<font color=red>" +str(item)+"</font>")
		
		for item in self.possibleWords:
			self.possibleWidget.append("<font color=blue>" +str(item)+"</font>")
		
		self.score += (self.presentList.__len__() * self.gameLevel)
		self.scoreBanner.setText("<font color=black> <h2> Score : "+str(self.score)+"</h2></font>")
		
							
	def clean(self):
		self.listWidget.clear()
	
	def next_(self):
		
		self.addButton.setEnabled(True)
		self.editButton.setEnabled(True)
		self.deleteButton.setEnabled(True)
		self.upButton.setEnabled(True)
		self.downButton.setEnabled(True)
		self.sortButton.setEnabled(True)
		self.cleanButton.setEnabled(True)
		self.submitButton.setEnabled(True)
		self.nextButton.setEnabled(False)
		
		self.listWidget.clear()
		self.resultWidget.clear()
		self.possibleWidget.clear()
		self.gameLevel += 1
		#self.maxThreshold -= 7				# Increases complexity of game
		self.minThreshold -= 2
		if self.gameLevel > 8:			# Max levels
			QMessageBox.information(self, "Spellathon","Congratulation you Scored : <font color=green><b>"+str(self.score)+"</b></font> <br>Hope you enjoyed!", QMessageBox.Ok )
			QDialog.accept(self)
		else:
			self.startGame(self.gameLevel)
		
		
	def getRandomAlphabets(self, no_of):
		
		i = 0
		li = []
		while i < no_of:
			no = randint(0,25)
			flag = 0
			
			for n in self.fixedList:
				if n == self.alphaList[no]:
					flag = 1
					break
					
			if flag == 0:
				for n in li:
					if n == self.alphaList[no]:
						flag = 1
						break
					
			if flag == 0:
				li.append(self.alphaList[no])
				i += 1
				
		return li
	
	
	def maxWords(self, fList, vList):
		self.possibleWords = []
			
		for word in self.dictWords:
			flag = False
						
			fixedFlag = []
			
			for x in range(0,self.fixedList.__len__(),1):
				fixedFlag.append(False)
						
			for l in word:
				if fList.count(l) < 1:
					if vList.count(l) < 1:
						flag = True
						break
				else:
					fixedFlag[fList.index(l)] = True
										
			if flag == False and fixedFlag.count(False) < 1:
				self.possibleWords.append(word)
			
		return self.possibleWords.__len__()
		
		
	def startGame(self, gameLevel):
		self.gameLevel = gameLevel
		self.levelBanner.setText("<font color=black> <h2> Level : "+str(self.gameLevel)+" / 8</h2></font>")
		
		while True:
			self.fixedList = self.getRandomAlphabets(self.gameDist[gameLevel][0])
			self.varList = self.getRandomAlphabets(self.gameDist[gameLevel][1])
			val = self.maxWords(self.fixedList, self.varList)
			if val > self.minThreshold:# and val < self.maxThreshold:
				break
				
		self.fixedAlphaList.setText(str(self.fixedList))
		self.varAlphaList.setText(str(self.varList))
		print self.fixedList
		print self.varList
		print 'possible words:' 
		print self.possibleWords

def main():
	
	app = QApplication(sys.argv)
	game = Game()
	game.show()
	game.startGame(1)
	app.exec_()
	
if __name__ == "__main__":
	main()
