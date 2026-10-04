#__libraries__
import csv
from datetime import datetime
import pandas as pd
import urllib.parse
import urllib.parse
import webbrowser


#__functions__
def view_stock():
	"""Display full stock of medicines."""
	df = pd.read_csv("Med Stock.csv", header = None, names = ["S.No.", "Name", "Tablets Left", "Days Left", "Dose", "Expiry Date"])
	return df

def add_med(med_name, med_tablets, med_dose, med_days, med_expiry):
	"""Add a new medicine to the stock."""
	try:
		with open("Med Stock.csv", "a") as f:
			writer = csv.writer(f)
			writer.writerow([(len(view_stock()) + 1), med_name, med_tablets, med_days, med_dose, med_expiry.strftime("%d-%m-%y")])
			return True
	except Exception as e:
		return f"Error adding the medicine: {e}"

def check_med(med_name):
    """Check if a medicine exists in the stock."""
    df = view_stock()
    if med_name in df["Name"].values:
        return True
    else:
        return False

def remove_med(med_name):
	try:
		df = view_stock()
		df = df[df["Name"] != med_name]
		df["S.No."] = range(1, len(df) + 1)
		df.to_csv("Med Stock.csv", index = False, header = False)
		return True
	except Exception as e:
		return f"Error removing the medicine: {e}"

def update_stock(med_name, new_tablets, new_days, new_dose, new_expiry):
	try:
		df = view_stock()
		df.loc[df["Name"] == med_name, ["Tablets Left", "Days Left", "Dose", "Expiry Date"]] = [new_tablets, new_days, new_dose, new_expiry.strftime("%d-%m-%y")]
		df.to_csv("Med Stock.csv", index = False, header = False)
		return True
	except Exception as e:
		return f"Error updating the stock: {e}"

def check_expiry():
	df = view_stock()
	df["Expiry Date"] = pd.to_datetime(df["Expiry Date"], format = "%d-%m-%y")
	expired_meds = df[df["Expiry Date"] < datetime.now()]
	expiring_in_10_days = df[(df["Expiry Date"] >= datetime.now()) & (df["Expiry Date"] <= datetime.now() + pd.Timedelta(days = 10))]
	expiring_in_30_days = df[(df["Expiry Date"] > datetime.now() + pd.Timedelta(days = 10)) & (df["Expiry Date"] <= datetime.now() + pd.Timedelta(days = 30))]
	if len(expired_meds) > 0:
		expired_meds["Expiry Date"] = expired_meds["Expiry Date"].dt.strftime("%d-%m-%y")
		expired_meds = expired_meds[["Name", "Expiry Date"]]
		expiring_in_10_days["Expiry Date"] = expiring_in_10_days["Expiry Date"].dt.strftime("%d-%m-%y")
		expiring_in_10_days = expiring_in_10_days[["Name", "Expiry Date"]]
		expiring_in_30_days["Expiry Date"] = expiring_in_30_days["Expiry Date"].dt.strftime("%d-%m-%y")
		expiring_in_30_days = expiring_in_30_days[["Name", "Expiry Date"]]
		return expired_meds, expiring_in_10_days, expiring_in_30_days
	else:
		return None

def generate_refill_list():
    """Find medicines that need refill (e.g., Days Left <= 5)"""
    df = view_stock()
    # Filter medicines running low
    low_stock = df[df["Days Left"] <= 10]
    return low_stock

def get_whatsapp_link(phone_number):
    """Generate a WhatsApp click-to-chat URL with pre-filled message"""
    low_stock = generate_refill_list()
    if len(low_stock) == 0:
        return None, "All medicines are in sufficient stock."
    
    msg = "Mummy ye dawaiyan khatam hone wali hain:\n\n"
    for _, row in low_stock.iterrows():
        msg += f"• {row['Name']}: {row['Tablets Left']} tablets left (~{int(row['Days Left'])} days left)\n"
    
    # URL encode the message string
    encoded_msg = urllib.parse.quote(msg)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={encoded_msg}"
    return whatsapp_url, msg