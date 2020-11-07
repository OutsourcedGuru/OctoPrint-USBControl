# coding=utf-8
from __future__                             import absolute_import
from subprocess import check_output
from subprocess import call, Popen, PIPE
from octoprint.settings import settings, valid_boolean_trues
import flask
import octoprint.plugin
import os
import re

class UsbcontrolPlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
										 	 octoprint.plugin.SimpleApiPlugin,
											 octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin):

	def get_settings_defaults(self):
		s =                                     settings()
		return dict(
			usb4 =                                True,
			all =                                 True,
			init =                                False,
			isRaspi2B =                           False,
			isRaspi3B =                           False,
			isRaspi3Bplus =                       False,
			isRaspi4B =	                          False,
			cpuRevision =                         'unknown',
			piModel =                             'unknown'
		)

	def get_template_vars(self):
		return dict(
			usb4 =                                self._settings.get(["usb4"]),
			all =                                 self._settings.get(["all"]),
			init =                                self._settings.get(["init"]),
			isRaspi2B =                           self._settings.get(["isRaspi2B"]),
			isRaspi3B =                           self._settings.get(["isRaspi3B"]),
			isRaspi3Bplus =                       self._settings.get(["isRaspi3Bplus"]),
			isRaspi4B =                           self._settings.get(["isRaspi4B"]),
			cpuRevision =                         self._settings.get(["cpuRevision"]),
			piModel =                             self._settings.get(["piModel"])
		)

	def get_template_configs(self):
		return [dict(type="settings", custom_bindings=False)]

	def get_assets(self):
		return dict(
			js =                                  ["js/usbcontrol.js"],
			css =                                 ["css/usbcontrol.css"],
			less =                                ["less/usbcontrol.less"]
		)

	def get_api_commands(self):
		return dict(usb2=["arg2"],usb3=["arg3"],usb4=["arg4"],usb5=["arg5"],all=["argAll"],save=["init"])

	def on_api_command(self, command, data):
		uhubctlFolder =                         "/home/pi/oprint/lib/python2.7/site-packages/usbcontrol/bin"
		#uhubctlFolder =                         "/home/pi/OctoPrint-USBControl/usbcontrol/bin"
		if command == "save":
			self._logger.info("save init in settings")
			progRev =                             Popen(["cat", "/proc/cpuinfo"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			cpuinfo, err =                        progRev.communicate(b"")
			matchObj =                            re.search(r'^Revision\s+:\s+(.*)$', cpuinfo, re.M)
			cpuRevision =                         matchObj.group(1) if matchObj else ""
			piModel =                             self.switch(cpuRevision, 'unknown')
			s =                                   settings()
			s.setBoolean(["plugins", "usbcontrol", "init"],           True)
			s.setBoolean(["plugins", "usbcontrol", "isRaspi2B"],      True if piModel == "Raspi2B" else False)
			s.setBoolean(["plugins", "usbcontrol", "isRaspi3B"],      True if piModel == "Raspi3B" else False)
			s.setBoolean(["plugins", "usbcontrol", "isRaspi3Bplus"],  True if piModel == "Raspi3B+" else False)
			s.setBoolean(["plugins", "usbcontrol", "isRaspi4B"],     True if piModel == "Raspi4B" else False)
			s.set(["plugins", "usbcontrol", "cpuRevision"],           cpuRevision)
			s.set(["plugins", "usbcontrol", "piModel"],               piModel)
			s.save()
		if command == "usb4":
			strArg4 =                             "{arg4}".format(**data)
			try:
				self._logger.info("usb4 `{}`...".format(strArg4))
				location =                          "--loc=1-1"
				output =                            call(["sudo", "./uhubctl", location, "--ports=1-4", "--action=" + strArg4], cwd=uhubctlFolder)
				if output > 0:
					self._logger.info("  uhubctrl returned: {}".format(output))
			except OSError as e:
				self._logger.info("uhubctl failed, throwing error")
				output =                            "N/A"
		if command == "all":
			strArgAll =                           "{argAll}".format(**data)
			try:
				self._logger.info("all `{}`...".format(strArgAll))
				location =                          "--loc=1-1"
				output =                            call(["sudo", "./uhubctl", location, "--ports=2", "--action=" + strArgAll], cwd=uhubctlFolder)
				if output > 0:
					self._logger.info("  uhubctrl returned: {}".format(output))
			except OSError as e:
				self._logger.info("uhubctl failed, throwing error")
				output =                            "N/A"

	def switch(self, key, default):
		case = {
			'0007':   'RaspiA',
			'0008':   'RaspiA',
			'0009':   'RaspiA',
			'0012':   'RaspiA+',
			'0015':   'RaspiA+',
			'0002':   'RaspiB',
			'0003':   'RaspiB',
			'0004':   'RaspiB',
			'0005':   'RaspiB',
			'0006':   'RaspiB',
			'000d':   'RaspiB',
			'000e':   'RaspiB',
			'000f':   'RaspiB',
			'0010':   'RaspiB+',
			'0013':   'RaspiB+',
			'900032': 'RaspiB+',
			'a01041': 'Raspi2B',
			'a21041': 'Raspi2B',
			'a21042': 'Raspi2B',
			'a02082': 'Raspi3B',
			'a22082': 'Raspi3B',
			'a020d3': 'Raspi3B+',
			'a03111': 'Raspi4B',
			'b03111': 'Raspi4B',
			'b03112': 'Raspi4B',
			'c03111': 'Raspi4B',
			'c03112': 'Raspi4B',
			'9000c1': 'ZeroW',
			'9000C1': 'ZeroW',
			'900092': 'Zero',
			'900093': 'Zero',
			'9020e0': 'Raspi3A+',
			'0011':   'Compute',
			'0014':   'Compute'
		}
		return case.get(key, default)

	def on_startup(self, host, port):
		pass

	def get_update_information(self):
		return dict(
			usbcontrol=dict(
				displayName =                       "Usbcontrol Plugin",
				displayVersion =                    self._plugin_version,
				type =                              "github_release",
				user =                              "OutsourcedGuru",
				repo =                              "OctoPrint-USBControl",
				current =                           self._plugin_version,
				pip =                               "https://github.com/OutsourcedGuru/OctoPrint-USBControl/archive/{target_version}.zip"
			)
		)

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ =               UsbcontrolPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

