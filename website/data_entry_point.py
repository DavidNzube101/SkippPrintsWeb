# Not tested
# import requests
# from . import __trash
# from . import encrypt

# VXD_INFO = encrypt.decrypter(__trash.retTr())

# from_ = "http://127.0.0.1:2781"
# # from_ = "https://vertexdb.pythonanywhere.com"

# # link_prefix = f"{from_}/handler/OPERATION/{VXD_INFO}/INFO-TO-RETIRIEVE-FROM-?"

# # "http://127.0.0.1:2781/handler/get-all/&co;&sq;&00;&02;&02;&14;&20;&13;&19;&ws;&13;&00;&12;&04;&sq;&fc;&ws;&sq;&004;&001;&022;&009;&004;&st;&022;&005;&018;&020;&005;&024;&004;&002;&at;&012;&005;&004;&009;&020;&019;&016;&001;&003;&005;&st;&003;&015;&013;&sq;&cm;&ws;&sq;&00;&02;&02;&14;&20;&13;&19;&ws;&15;&00;&18;&18;&22;&14;&17;&03;&sq;&fc;&ws;&sq;&18;&008;&009;&016;&013;&001;&014;&&4;&&2;&ast;&sq;&cm;&ws;&sq;&03;&01;&ws;&13;&00;&12;&04;&sq;&fc;&ws;&sq;&022;&009;&004;&002;&021;&025;&und;&004;&002;&sq;&cm;&ws;&sq;&03;&01;&ws;&15;&00;&18;&18;&22;&14;&17;&03;&sq;&fc;&ws;&sq;&&2;&&3;&024;&004;&005;&hyph;&024;&bc;&ast;&bo;&020;&018;&009;&013;&&1;&&2;&hs;&&2;&sq;&cc;/&20;&019;&005;&018;&019;"

# try:
# 	response = requests.get(from_)

# 	def request_then_text(url):
# 		req = requests.get(url)
# 		return req.text

# 	class dbORM:
# 		"""docstring for dbORM"""
# 		def __init__(self):
# 			self.init = True

# 		def get_all(table):
# 			table = encrypt.encrypter(table)
# 			# connect()
# 			return eval(request_then_text(url=f'{from_}/handler/get-all/{VXD_INFO}/{table}'))

# 		def find_all(table, column, value):
# 			table = encrypt.encrypter(table)
# 			find_pair = {column: value}
# 			find_pair = encrypt.encrypter(str(find_pair))
# 			return eval(request_then_text(url=f'{from_}/handler/find-all/{VXD_INFO}/{table}/{find_pair}'))

# 		def add_entry(table, entry):
# 			table = encrypt.encrypter(table)
# 			# try:
# 			entry = encrypt.encrypter(str(entry))

# 			return eval(request_then_text(url=f'{from_}/handler/add-entry/{VXD_INFO}/{table}/{entry}'))
			

# 			# except Exception as e:
# 			# 	print(f">>>>>>>>>>>>>>>>>>>>>>>>>>\ne: {e}\ntable: {table}\ncvp: {column_value_pairs}")

# 		def find_one(table, column, value):
# 			table = encrypt.encrypter(table)
# 			find_pair = {column: value}
# 			find_pair = encrypt.encrypter(str(find_pair))

# 			return eval(request_then_text(url=f'{from_}/handler/find-one/{VXD_INFO}/{table}/{find_pair}'))

# 		def update_entry(table, column, entry):
# 			entry = encrypt.encrypter(str(entry))
# 			column = encrypt.encrypter(column)
# 			table = encrypt.encrypter(table)
# 			return eval(request_then_text(url=f'{from_}/handler/update-entry/{VXD_INFO}/{table}/{column}/{entry}'))

# 		def delete_entry(table, column):
# 			table = encrypt.encrypter(table)
# 			column = encrypt.encrypter(column)
# 			return eval(request_then_text(url=f'{from_}/handler/delete-entry/{VXD_INFO}/{table}/{column}'))


# except Exception as e:
# 	print(e)
# 	dbORM = None
