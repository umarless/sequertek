import frappe

@frappe.whitelist()
def get_primary_contact(doctype, name):
	"""
	Returns default contact for the given doctype and name.
	Can be ordered by `contact_type` to either is_primary_contact or is_billing_contact.
	"""
	out = frappe.db.sql(
		"""
			SELECT dl.parent, c.is_primary_contact, c.is_billing_contact,cp.phone,c.email_id
			FROM `tabDynamic Link` dl
			INNER JOIN `tabContact` c ON c.name = dl.parent
            LEFT JOIN `tabContact Phone` cp
            ON cp.parent = dl.parent
			WHERE
				dl.link_doctype=%s AND
				dl.link_name=%s AND
				dl.parenttype = 'Contact' AND
				c.is_primary_contact = 1
			ORDER BY c.creation DESC
		""",
		(doctype, name),as_dict=1
	)
	if out:
		try:
			return out[0]['phone'],out[0]['email_id']
		except Exception:
			return None
	else:
		return None

@frappe.whitelist()
def get_company_name_from_lead(link_name):
    return frappe.db.get_value("Lead",link_name,'company_name')
    # if doc.links:
    #     if doc.links[0]['link_doctype'] == "Lead":
    #     return frappe.db.get_value(doc.links[0]['link_doctype'],doc.links[0]['link_name'],'company_name')
    # else:
    #     return "NA"