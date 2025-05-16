# Copyright (c) 2025, infus and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DemandManagement(Document):

	def before_insert(self):
		self.talep_eden = frappe.session.user
	
	# talep.py içine eklenir
def get_permission_query_conditions(user):
    
    if not user or user == "Guest":
        return "1=0"  # misafir hiç görmesin

    # Eğer admin ise her şeyi görsün
    if "System Manager" in frappe.get_roles(user):
        return None

    # Kullanıcının rollerini al
    user_roles = frappe.get_roles(user)

    # Kullanıcının görebileceği taleplerin türlerini al
    talep_turleri = frappe.get_all("Demand Type", filters={
        "rol": ["in", user_roles]
    }, pluck="name")

    # Talep türü eşleşmesi olanlar ve owner olanlar
    if talep_turleri:
        talep_turleri = [f"'{t}'" for t in talep_turleri]
        talep_turu_in = ", ".join(talep_turleri)
        return f"(tur IN ({talep_turu_in}) OR talep_eden = '{user}')"
    else:
        # Sadece kendi taleplerini görebilsin
        return f"`tabDemand Management`.talep_eden = '{user}'"

def has_permission(doc, ptype, user):
    if "HR User" in frappe.get_roles(user) or "System Manager" in frappe.get_roles(user):
        return True

    # Kendi oluşturduğu talebe erişebilir
    return doc.owner == user
