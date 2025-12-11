from detect import *

#class Clothes:


class ClothesManager:
	def __init__(self):
		self.clothes_data = None #data format [ID,  type, isIn?, season, tone]
	
#						    (ha, sang, outter)
	def add_clothes(self, ID, clothing_type, season, tone):
		self.clothes_sata.append([ID, clothing_type, season, tone])
	
	
class ClothesSorter:
	
	def __init__(self, detector, clthMgr):
		self.clthMgr = clthMgr
		
		self.detector = detector
		self.obj = None
		self.cnt = 0
		self.doSave = False

	def update(self):
		obj = self.detector.getObject()
		if obj[0]:
			self.obj = obj
			if self.cnt > 2:
				self.doSave = True
				
				return 1
			
			self.cnt = self.cnt + 1
		else:
			if self.cnt:
				self.cnt = self.cnt - 1
				if not self.cnt and self.doSave:
					
					self.obj = None
					self.doSave = False
					
					
		if not self.cnt and not self.doSave:
			self.obj = None
	
#	'ha', 'outer','sang'
	def extractInfo(self):
		if not self.obj:
			print("ClothesSorter_extractInfo: Noobject")
			return False
		clth_type = self.obj[5]
		if  clth_type == 'sang':
			pass
		elif  clth_type == 'ha':
			pass
		elif clth_type == 'outer':
			
			pass
