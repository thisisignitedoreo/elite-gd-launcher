# Be aware of monsters and shit-code
# Made by acid

from PySide6 import (
	QtWidgets,
	QtCore,
	QtGui,
	QtSvg,
)
from form import Ui_Form
from pathlib import Path
import subprocess
import traceback
import requests
import zipfile
import shutil
import base64
import json
import sys
import io
import os

if not os.path.isfile("settings.json"):
	open("settings.json", "w").write(json.dumps({"lang": "en"}))

with open("settings.json") as f:
	settings_global = json.load(f)

class EliteGDLauncher(QtWidgets.QWidget):
	def __init__(self):
		super(EliteGDLauncher, self).__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		self.path = "C:/Program Files/EliteGD"

		self.ui.lineEdit.setText(self.path)

		ru_icon = self.render_svg("assets/ru.svg", (32, 24))
		en_icon = self.render_svg("assets/us.svg", (32, 24))

		self.ui.radioButton.setIcon(en_icon)
		self.ui.radioButton_2.setIcon(ru_icon)

		if settings_global["lang"] == "ru":
			self.strings = {
				"pathSelect": "Путь:",
				"dirSel": "Выберите папку",
				"ready": "EliteGD установлена",
				"notReady": "EliteGD не установлена!",
				"play": "Играть",
				"install": "Установить",
				"en": "Английский",
				"ru": "Русский",
				"cm": "Чит-меню",
				"bots": "Боты",
				"instGdhm": "Установить GDHM",
				"instGdh": "Установить GDH",
				"instReplayBot": "Установить ReplayBot",
				"instEchoBot": "Установить EchoBot",
				"instSai": "Установить SAI Mod Pack",
				"offReplayBot": "Отключить ReplayBot",
				"offEchoBot": "Отключить EchoBot",
				"onReplayBot": "Включить ReplayBot",
				"onEchoBot": "Включить EchoBot",
				"browse": "Обзор",
				"recheck": "Перепроверить",
				"update": "Обновить",
				"mods": "Моды",
				"recent": "Недавние уровнии на GDPS:",
			}
			self.ui.radioButton.setChecked(False)
			self.ui.radioButton_2.setChecked(True)
		elif settings_global["lang"] == "en":
			self.strings = {
				"pathSelect": "Path:",
				"dirSel": "Select directory",
				"ready": "EliteGD is ready to play",
				"notReady": "EliteGD is not installed!",
				"play": "Play",
				"install": "Install",
				"en": "English",
				"ru": "Russian",
				"cm": "Cheat-menus",
				"bots": "Bots",
				"instGdhm": "Install GDHM",
				"instGdh": "Install GDH",
				"instReplayBot": "Install ReplayBot",
				"instEchoBot": "Install EchoBot",
				"instSai": "Install SAI Mod Pack",
				"offReplayBot": "Disable ReplayBot",
				"offEchoBot": "Disable EchoBot",
				"onReplayBot": "Enable ReplayBot",
				"onEchoBot": "Enable EchoBot",
				"browse": "Browse",
				"recheck": "Recheck",
				"update": "Update",
				"mods": "Mods",
				"recent": "Recent levels on GDPS:",
			}
			self.ui.radioButton.setChecked(True)
			self.ui.radioButton_2.setChecked(False)

		self.ui.radioButton.setText(self.strings["en"])
		self.ui.radioButton_2.setText(self.strings["ru"])
		self.ui.label_2.setText(self.strings["pathSelect"])
		self.ui.label_3.setText(self.strings["recent"])
		self.ui.label_4.setText(self.strings["cm"])
		self.ui.label_5.setText(self.strings["bots"])
		self.ui.label_6.setText(self.strings["mods"])
		self.ui.pushButton_3.setText(self.strings["instGdhm"])
		self.ui.pushButton_4.setText(self.strings["instGdh"])
		self.ui.pushButton_6.setText(self.strings["instSai"])
		self.ui.toolButton.setText(self.strings["recheck"])
		self.ui.toolButton_2.setText(self.strings["browse"])
		self.ui.toolButton_3.setText(self.strings["update"])

		self.connect()
		self.recheck_all()
		self.fetch_recent_levels()

	def connect(self):
		self.ui.toolButton.clicked.connect(self.recheck_all)
		self.ui.toolButton_2.clicked.connect(self.browse_path)
		self.ui.toolButton_3.clicked.connect(self.fetch_recent_levels)
		self.ui.radioButton.clicked.connect(lambda: self.lang_switched(0))
		self.ui.radioButton_2.clicked.connect(lambda: self.lang_switched(1))
		self.ui.pushButton.clicked.connect(self.install)
		self.ui.pushButton_2.clicked.connect(self.install_echo)
		self.ui.pushButton_3.clicked.connect(self.install_gdhm)
		self.ui.pushButton_4.clicked.connect(self.install_gdh)
		self.ui.pushButton_5.clicked.connect(self.install_replaybot)
		self.ui.pushButton_6.clicked.connect(self.install_sai)

	def install_gdhm(self):
		self.ui.pushButton.setEnabled(False)
		self.ui.pushButton_2.setEnabled(False)
		self.ui.pushButton_3.setEnabled(False)
		self.ui.pushButton_4.setEnabled(False)
		self.ui.pushButton_5.setEnabled(False)
		response = requests.get("https://adaf.xyz/adaf/hm/download/v34.18/b0fc84427313fb6168479888b3614da4f1004426987880ce5175a6d854069ed4/GDHM_TASBOT_v34.18.zip", stream=True)
		total_length = response.headers.get('content-length')
		gdhm = b""

		if total_length is None:
			gdhm += response.content
		else:
			dl = 0
			total_length = int(total_length)
			self.ui.progressBar.setMaximum(total_length)
			for data in response.iter_content(chunk_size=65536):
				app.processEvents()
				dl += len(data)
				gdhm += data
				self.ui.progressBar.setValue(dl)

		try:
			with zipfile.ZipFile(io.BytesIO(gdhm)) as zf:
				zf.extractall(self.path)
				folder = zf.namelist()[0].split("/")[0]
				shutil.copytree(self.path + "/" + folder, self.path + "/", dirs_exist_ok=True)
				shutil.rmtree(self.path + "/" + folder)
		except:
			msgbox = QtWidgets.QMessageBox()
			msgbox.setText(traceback.format_exc())
			msgbox.setIcon(QtWidgets.QMessageBox.Critical)
			msgbox.exec()

		with open(self.path + "/settings.json", "r") as f:
			settings = json.loads(f.read())

		settings["cheat_menu"] = 1

		with open(self.path + "/settings.json", "w") as f:
			f.write(json.dumps(settings))
		self.ui.pushButton.setEnabled(True)
		self.recheck_all()

	def install_gdh(self):
		self.ui.pushButton.setEnabled(False)
		self.ui.pushButton_2.setEnabled(False)
		self.ui.pushButton_3.setEnabled(False)
		self.ui.pushButton_4.setEnabled(False)
		self.ui.pushButton_5.setEnabled(False)
		response = requests.get("https://github.com/TobyAdd/GDH/releases/latest/download/GDH.zip", stream=True)
		total_length = response.headers.get('content-length')
		gdh = b""

		if total_length is None:
			gdh += response.content
		else:
			dl = 0
			total_length = int(total_length)
			self.ui.progressBar.setMaximum(total_length)
			for data in response.iter_content(chunk_size=65536):
				app.processEvents()
				dl += len(data)
				gdh += data
				self.ui.progressBar.setValue(dl)

		try:
			with zipfile.ZipFile(io.BytesIO(gdh)) as zf:
				zf.extractall(self.path)
		except:
			msgbox = QtWidgets.QMessageBox()
			msgbox.setText(traceback.format_exc())
			msgbox.setIcon(QtWidgets.QMessageBox.Critical)
			msgbox.exec()

		with open(self.path + "/settings.json", "r") as f:
			settings = json.loads(f.read())

		settings["cheat_menu"] = 2

		with open(self.path + "/settings.json", "w") as f:
			f.write(json.dumps(settings))
		self.ui.pushButton.setEnabled(True)
		self.recheck_all()

	def install_quickldr(self):
		self.ui.pushButton.setEnabled(False)
		response = requests.get("https://cdn.discordapp.com/attachments/837026406282035300/859008315413626920/quickldr-v1.1.zip", stream=True)
		total_length = response.headers.get('content-length')
		quickldr = b""

		if total_length is None:
			quickldr += response.content
		else:
			dl = 0
			total_length = int(total_length)
			self.ui.progressBar.setMaximum(total_length)
			for data in response.iter_content(chunk_size=65536):
				app.processEvents()
				dl += len(data)
				quickldr += data
				self.ui.progressBar.setValue(dl)

		try:
			with zipfile.ZipFile(io.BytesIO(quickldr)) as zf:
				zf.extractall(self.path)
		except:
			msgbox = QtWidgets.QMessageBox()
			msgbox.setText(traceback.format_exc())
			msgbox.setIcon(QtWidgets.QMessageBox.Critical)
			msgbox.exec()

		self.create_dir_if_nexist(self.path + "/quickldr")

		with open(self.path + "/settings.json", "r") as f:
			settings = json.loads(f.read())

		settings["quickldr"] = True

		with open(self.path + "/settings.json", "w") as f:
			f.write(json.dumps(settings))

		with open(self.path + "/quickldr/settings.txt", "w") as f:
			f.write("rb.dll\neb.dll\nSaiModPack.dll")

		self.ui.pushButton.setEnabled(True)
		self.recheck_all()

	def install_replaybot(self):
		with open(self.path + "/settings.json", "r") as f:
			settings = json.loads(f.read())

		if not settings["replaybot"][0]:
			if not settings["quickldr"]:
				self.install_quickldr()

			self.ui.pushButton.setEnabled(False)


			response = requests.get("https://github.com/matcool/ReplayBot/releases/latest/download/replay-bot.dll", stream=True)
			total_length = response.headers.get('content-length')
			replaybot = b""

			if total_length is None:
				replaybot += response.content
			else:
				dl = 0
				total_length = int(total_length)
				self.ui.progressBar.setMaximum(total_length)
				for data in response.iter_content(chunk_size=65536):
					app.processEvents()
					dl += len(data)
					replaybot += data
					self.ui.progressBar.setValue(dl)

			open(self.path + "/quickldr/rb.dll", "w").close()
			open(self.path + "/quickldr/rb.dll", "wb").write(replaybot)

			with open(self.path + "/settings.json", "r") as f:
				settings_ = json.loads(f.read())

			settings_["replaybot"][0] = True
			settings_["replaybot"][1] = True

			with open(self.path + "/settings.json", "w") as f:
				f.write(json.dumps(settings_))
			self.ui.pushButton.setEnabled(True)
		else:
			if settings["replaybot"][1]:
				os.rename(self.path + "/quickldr/rb.dll", self.path + "/quickldr/rb.dll.dis")

				with open(self.path + "/settings.json", "r") as f:
					settings_ = json.loads(f.read())

				settings_["replaybot"][1] = False

				with open(self.path + "/settings.json", "w") as f:
					f.write(json.dumps(settings_))
			
			else:
				os.rename(self.path + "/quickldr/rb.dll.dis", self.path + "/quickldr/rb.dll")

				with open(self.path + "/settings.json", "r") as f:
					settings_ = json.loads(f.read())

				settings_["replaybot"][1] = True

				with open(self.path + "/settings.json", "w") as f:
					f.write(json.dumps(settings_))
		self.recheck_all()

	def install_sai(self):
		with open(self.path + "/settings.json", "r") as f:
			settings = json.loads(f.read())

		if not settings["saimp"]:

			self.ui.pushButton.setEnabled(False)


			response = requests.get("https://www.dropbox.com/s/j83jb6mu8q307ip/smp.zip?dl=1", stream=True)
			total_length = response.headers.get('content-length')
			smp = b""

			if total_length is None:
				smp += response.content
			else:
				dl = 0
				total_length = int(total_length)
				self.ui.progressBar.setMaximum(total_length)
				for data in response.iter_content(chunk_size=65536):
					app.processEvents()
					dl += len(data)
					smp += data
					self.ui.progressBar.setValue(dl)

			try:
				with zipfile.ZipFile(io.BytesIO(smp)) as zf:
					zf.extractall(self.path)
			except:
				msgbox = QtWidgets.QMessageBox()
				msgbox.setText(traceback.format_exc())
				msgbox.setIcon(QtWidgets.QMessageBox.Critical)
				msgbox.exec()

			with open(self.path + "/settings.json", "r") as f:
				settings_ = json.loads(f.read())

			settings_["saimp"] = True

			with open(self.path + "/settings.json", "w") as f:
				f.write(json.dumps(settings_))
			self.ui.pushButton.setEnabled(True)
		self.recheck_all()

	def install_echo(self):
		with open(self.path + "/settings.json", "r") as f:
			settings = json.loads(f.read())

		if not settings["echobot"][0]:
			if not settings["quickldr"]:
				self.install_quickldr()

			self.ui.pushButton.setEnabled(False)


			response = requests.get("https://cdn.discordapp.com/attachments/838145374849204244/1054218314563453048/Echo.dll", stream=True)
			total_length = response.headers.get('content-length')
			echobot = b""

			if total_length is None:
				echobot += response.content
			else:
				dl = 0
				total_length = int(total_length)
				self.ui.progressBar.setMaximum(total_length)
				for data in response.iter_content(chunk_size=65536):
					app.processEvents()
					dl += len(data)
					echobot += data
					self.ui.progressBar.setValue(dl)

			open(self.path + "/quickldr/eb.dll", "w").close()
			open(self.path + "/quickldr/eb.dll", "wb").write(echobot)

			with open(self.path + "/settings.json", "r") as f:
				settings_ = json.loads(f.read())

			settings_["echobot"][0] = True
			settings_["echobot"][1] = True

			with open(self.path + "/settings.json", "w") as f:
				f.write(json.dumps(settings_))
			self.ui.pushButton.setEnabled(True)
		else:
			if settings["echobot"][1]:
				os.rename(self.path + "/quickldr/eb.dll", self.path + "/quickldr/eb.dll.dis")

				with open(self.path + "/settings.json", "r") as f:
					settings_ = json.loads(f.read())

				settings_["echobot"][1] = False

				with open(self.path + "/settings.json", "w") as f:
					f.write(json.dumps(settings_))
			
			else:
				os.rename(self.path + "/quickldr/eb.dll.dis", self.path + "/quickldr/eb.dll")

				with open(self.path + "/settings.json", "r") as f:
					settings_ = json.loads(f.read())

				settings_["echobot"][1] = True

				with open(self.path + "/settings.json", "w") as f:
					f.write(json.dumps(settings_))
		self.recheck_all()

	def lang_switched(self, lang):
		if lang == 0:
			open("settings.json", "w").write(json.dumps({"lang": "en"}))
			msgbox = QtWidgets.QMessageBox()
			msgbox.setText("Restart launcher to apply")
			msgbox.exec()
		elif lang == 1:
			open("settings.json", "w").write(json.dumps({"lang": "ru"}))
			msgbox = QtWidgets.QMessageBox()
			msgbox.setText("Перезагрузи лаунчер чтобы применить")
			msgbox.exec()

	def fetch_recent_levels(self):
		self.ui.listWidget.clear()	
		app.processEvents()
		resp = requests.get("https://rugd.gofruit.space/00Ch/db/getGJLevels21.php", data={"type": 4}).text
		levels = resp.split("#")[0].split("|")
		authors = resp.split("#")[1].split("|")

		for k, _ in enumerate(levels[0:25]):
			name = levels[k].split(":")[3]
			description = base64.b64decode(levels[k].split(":")[5]).decode("utf-8")
			level_id = levels[k].split(":")[1]
			author = authors[k].split(":")[1]
			item = QtWidgets.QListWidgetItem(name)
			font = item.font()
			font.setWeight(QtGui.QFont.Weight.Bold)
			item.setFont(font)
			item.setFlags(QtCore.Qt.ItemIsEnabled)
			self.ui.listWidget.addItem(item)
			item = QtWidgets.QListWidgetItem(f"by: {author} (id: {level_id})")
			item.setFlags(QtCore.Qt.ItemIsEnabled)
			self.ui.listWidget.addItem(item)
			if description != "":
				item = QtWidgets.QListWidgetItem(f"Description: {description}")
				item.setFlags(QtCore.Qt.ItemIsEnabled)
				self.ui.listWidget.addItem(item)
			item_empty = QtWidgets.QListWidgetItem("")
			item_empty.setFlags(QtCore.Qt.ItemIsSelectable)
			self.ui.listWidget.addItem(item_empty)

	def install(self):
		if self.recheck_status() != 0:
			self.create_dir_if_nexist(self.path)
			self.ui.pushButton.setEnabled(False)
			app.processEvents()
			response = requests.get("https://www.dropbox.com/s/sqk6lb0mgihxucy/game.zip?dl=1", stream=True)
			total_length = response.headers.get('content-length')
			game = b""

			if total_length is None:
				game += response.content
			else:
				dl = 0
				total_length = int(total_length)
				self.ui.progressBar.setMaximum(total_length)
				for data in response.iter_content(chunk_size=65536):
					app.processEvents()
					dl += len(data)
					game += data
					self.ui.progressBar.setValue(dl)

			with zipfile.ZipFile(io.BytesIO(game)) as zf:
				zf.extractall(self.path)

			with open(self.path + "/settings.json", "w") as f:
				f.write(
					json.dumps(
						{
							"cheat_menu": 0,
							"replaybot": [False, False],
							"echobot": [False, False],
							"saimp": False,
							"quickldr": False,
						}
					)
				)
			self.recheck_all()
			self.ui.pushButton.setEnabled(True)
		else:
			subprocess.Popen([self.path + "/elitegd 2.2.exe"], cwd=self.path)

	def browse_path(self):
		self.path = str(QtWidgets.QFileDialog.getExistingDirectory(self, self.strings["dirSel"]))
		self.ui.lineEdit.setText(self.path)
		self.recheck_all()

	def recheck_all(self):
		status = self.recheck_status()

		match status:
			case 0:
				self.ui.label.setText(self.strings["ready"])
				self.ui.pushButton.setText(self.strings["play"])
				settings = json.loads(open(self.path + "/settings.json").read())
				if settings["cheat_menu"] != 0:
					self.ui.pushButton_3.setEnabled(False)
					self.ui.pushButton_4.setEnabled(False)
				else:
					self.ui.pushButton_3.setEnabled(True)
					self.ui.pushButton_4.setEnabled(True)

				self.ui.pushButton_5.setEnabled(True)
				if settings["replaybot"][0]:
					if settings["replaybot"][1]:
						self.ui.pushButton_5.setText(self.strings["offReplayBot"])
					else:
						self.ui.pushButton_5.setText(self.strings["onReplayBot"])
				else:
					self.ui.pushButton_5.setText(self.strings["instReplayBot"])

				self.ui.pushButton_2.setEnabled(True)
				if settings["echobot"][0]:
					if settings["echobot"][1]:
						self.ui.pushButton_2.setText(self.strings["offEchoBot"])
					else:
						self.ui.pushButton_2.setText(self.strings["onEchoBot"])
				else:
					self.ui.pushButton_2.setText(self.strings["instEchoBot"])

				self.ui.pushButton_6.setEnabled(not settings["saimp"])

			case _:
				self.ui.label.setText(self.strings["notReady"])
				self.ui.pushButton.setText(self.strings["install"])
				self.ui.pushButton_2.setEnabled(False)
				self.ui.pushButton_3.setEnabled(False)
				self.ui.pushButton_4.setEnabled(False)
				self.ui.pushButton_5.setEnabled(False)

	def recheck_status(self):
		if not os.path.isdir(self.path):
			return -1

		if not (os.path.isfile(self.path + "/settings.json") and os.path.isfile(self.path + "/elitegd 2.2.exe")):
			return -1

		return 0

	def render_svg(self, path, size):
		svg_renderer = QtSvg.QSvgRenderer(path)
		image = QtGui.QImage(*size, QtGui.QImage.Format_ARGB32)
		image.fill(0x00000000)
		svg_renderer.render(QtGui.QPainter(image))
		pixmap = QtGui.QPixmap.fromImage(image)
		return QtGui.QIcon(pixmap)

	def create_dir_if_nexist(self, path):
		Path(path).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	window = EliteGDLauncher()
	window.show()

	sys.exit(app.exec())
