

class Convertor:
	@staticmethod
	def convertToInt(value, default = None):
		try:
			return int(value)
		except (ValueError, TypeError):
			print(f"[INFO] : could not convert to integer")
			return default
