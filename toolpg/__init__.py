# -- coding: utf-8 --

import os
from mods.bin_mod import bin_mod
work_path = bin_mod.work_path
configPage = []
for file in os.listdir(work_path+'\\toolpg\\'):
   if file == '__init__.py' or file == '__pycache__':
      continue
   else:
      configPage.append(file[:-3])

