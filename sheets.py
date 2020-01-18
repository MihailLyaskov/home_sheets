import gspread
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

months_en_bg = {
	"January":"Януари",
	"February":"Февруари",
	"March":"Март",
	"April":"Април",
	"May":"Май",
	"June":"Юни",
	"July":"Юли",
	"August":"Август",
	"September":"Септември",
	"October":"Октомври",
	"November":"Ноември",
	"December":"Декември"
}

months_bg_en = {
	"Януари":"January",
	"Февруари":"February",
	"Март":"March",
	"Април":"April",
	"Май":"May",
	"Юни":"June",
	"Юли":"July",
	"Август":"August",
	"Септември":"September",
	"Октомври":"October",
	"Ноември":"November",
	"Декември":"December"
}

class Sheet(object):

	def __init__(self, creds_dir, sheet_name):
		self.credentials 	= ServiceAccountCredentials.from_json_keyfile_name(creds_dir, scope)
		self.sheet_name 	= sheet_name

	# Return openet worksheet in Spread Sheet
	def open(self):
		# Connect to Google API
		google_client 	= gspread.authorize(self.credentials)
		# Get Sheet
		spread_sheet 	= google_client.open(self.sheet_name)

		current_month 	= date.today().strftime("%B")
		worksheets 		= spread_sheet.worksheets()

		currnet_worksheet = self._check_for_worksheet(current_month, worksheets)
		# TO-DO If worksheet for this month not found, create one...
		return spread_sheet.worksheet(currnet_worksheet)

	# data {date : " d / m / y"}
	def add_entry(self, worksheet, data):
		worksheet.append_row(data, value_input_option="USER_ENTERED")

	def _check_for_worksheet(self, month, worksheets):
		month_translated = months_en_bg[month]
		for ws in worksheets:
			if month_translated == ws.title:
				return month_translated
		else:
			# TO-DO Raise error
			return None


if __name__ == "__main__":
	sheet = Sheet(
		creds_dir='./creds.json', 
		sheet_name='Test Sheet'
	)
	ws = sheet.open()
	print("Worksheet has {} rows".format(ws.row_count))
