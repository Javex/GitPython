# test_config.py
# Copyright (C) 2008, 2009 Michael Trier (mtrier@gmail.com) and contributors
#
# This module is part of GitPython and is released under
# the BSD License: http://www.opensource.org/licenses/bsd-license.php

from test.testlib import *
from git import *
import StringIO
from copy import copy

class TestBase(TestCase):
	
	@classmethod
	def setUpAll(cls):
		cls.repo = Repo(GIT_REPO)
		
	def _to_memcache(self, file_path):
		fp = open(file_path, "r")
		sio = StringIO.StringIO()
		sio.write(fp.read())
		sio.seek(0)
		sio.name = file_path
		return sio
		
	def _parsers_equal_or_raise(self, lhs, rhs):
		pass
		
	def test_read_write(self):
		# writer must create the exact same file as the one read before
		for filename in ("git_config", "git_config_global"):
			file_obj = self._to_memcache(fixture_path(filename))
			file_obj_orig = copy(file_obj)
			w_config = GitConfigParser(file_obj, read_only = False)
			w_config.read()					# enforce reading
			assert w_config._sections
			w_config.write()				# enforce writing
			assert file_obj.getvalue() == file_obj_orig.getvalue()
		# END for each filename
		
	def test_base(self):
		path_repo = fixture_path("git_config")
		path_global = fixture_path("git_config_global")
		r_config = GitConfigParser([path_repo, path_global], read_only=True)
		assert r_config.read_only
		num_sections = 0
		num_options = 0
		
		# test reader methods
		assert r_config._is_initialized == False
		for section in r_config.sections():
			num_sections += 1
			for option in r_config.options(section):
				num_options += 1
				val = r_config.get(section, option)
				assert val
				
				# writing must fail
				self.failUnlessRaises(IOError, r_config.set, section, option, None)
				self.failUnlessRaises(IOError, r_config.remove_option, section, option )
			# END for each option
			self.failUnlessRaises(IOError, r_config.remove_section, section)
		# END for each section 
		assert num_sections and num_options
		assert r_config._is_initialized == True
		
		
		self.fail("TODO: Base config writer testing")
