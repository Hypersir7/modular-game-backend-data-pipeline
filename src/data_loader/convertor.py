

class Convertor:
	@staticmethod
	def convertToInt(value, default = None):
		try:
			return int(value)
		except (ValueError, TypeError):
			# COMMENT THIS LINE TO DISABLE DEBUGGING
			# print(f"[INFO] : could not convert to integer: value: {value} -> default: {default}")
			return default
	
	@staticmethod
	def treeConvertInt(parent, tag, default = None):
		
		treeElement = parent.find(tag)

		if treeElement is not None and treeElement.text is not None:
			return Convertor.convertToInt(treeElement.text, default)
		else:
			return default
		