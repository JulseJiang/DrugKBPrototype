from Base import DataStorage
# import speciallist

class speciallist():
		lis = {}
		"""
		lis={"ASD":["ASD","AUTISM"],
		     "SCZ":["SCZ"],
		     "ID":["ID"],
		     "DD":["DD"],
		     "EE":["EE"],
		     "TD":["TD","TOURETTE DISORDER"]}
		"""

class Datacreater():
	def __init__(self):
		self.a = "123"
		self.b = "456"

	def com(self):
		return self.a + self.b


class Datafinder():

	def __init__(self, key, colname="Genes"):
		self.key = key
		self.db = DataStorage.DataStorage(colname)

	"""
	def __call__(self,key):
		self.key=key
		self.db=DataStorage.DataStorage(colname)
		return self.db.FindByID(self.key)
	"""

	def is_type(self, a):
		lis = "1234567890"
		if ":" in a:
			return "chr"
		elif a.upper() in speciallist.lis:
			for i in speciallist.dic:
				pass
		else:
			v = 0
			for i in a:
				if i not in lis:
					v = 1
			if v == 1:
				return "symbol"
			else:
				return "ID"

	def FindAll(self):
		return self.db.FindAll()

	def FindOne(self):
		if self.is_type(self.key) == "ID":
			q = self.db.FindByID(self.key)
			if q != [None]:
				return q
			else:
				return None
		elif self.is_type(self.key) == "symbol":
			q = self.db.FindBySymbol(self.key.upper())
			if q != [None]:
				return q
			else:
				return None
		elif self.is_type(self.key) == "chr":
			q = self.db.FindByChr(self.key)
			if q != [None]:
				return q
			else:
				return None


class DiseaseFinder():

	def __init__(self, key):

		self.key = key
		self.dbA = DataStorage.DataStorage("DNM")
		self.dbB = DataStorage.DataStorage("CNV")

	def Find(self):
		x = {}
		x["DNM"] = self.dbA.FindBydisease(self.key)
		if self.key == "SCZ":
			x["CNV"] = self.dbB.FindBydisease("Schizophrenia")
		elif self.key == "ID":
			x["CNV"] = self.dbB.FindBydisease("Intellectual Disability/Developmental Disability")
		elif self.key == "BD":
			x["CNV"] = self.dbB.FindBydisease("Bipolar")
		elif self.key == "control":
			x["CNV"] = self.dbB.FindBydisease("Control")
		else:
			x["CNV"] = self.dbB.FindBydisease(self.key)
		return x


if __name__ == "__main__":
	a = DiseaseFinder("ADHD")
	print(a.Find())
