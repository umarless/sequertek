import frappe
from  erpnext.projects.doctype.task.task import get_children

@frappe.whitelist()
def get_reports_to_for_resignation(employee):
    emp_doc = frappe.get_doc("Employee",employee)
    reports_to = []
    if emp_doc.reports_to:
        reports_to.append({
            "employee":emp_doc.reports_to,
            "email_id":frappe.db.get_value("Employee",emp_doc.reports_to,"user_id"),
            'send_email':1
        })
    reports_to.append({
        "employee":'',
        "email_id":frappe.db.get_value("HR Settings","HR Settings","default_email"),
        'send_email':1
    })
    # if emp_doc.expense_approver:
    # 	reports_to.append({
    # 		"employee":frappe.db.get_all("Employee",{"user_id":emp_doc.expense_approver},pluck='employee'),
    # 		"email_id":emp_doc.expense_approver,
    # 		'send_email':1
    # 	})
    # if emp_doc.shift_request_approver:
    # 	reports_to.append({
    # 		"employee":frappe.db.get_all("Employee",{"user_id":emp_doc.shift_request_approver},pluck='employee'),
    # 		"email_id":emp_doc.shift_request_approver,
    # 		'send_email':1
    # 	})
    # if emp_doc.leave_approver:
    # 	reports_to.append({
    # 		"employee":frappe.db.get_all("Employee",{"user_id":emp_doc.leave_approver},pluck='employee'),
    # 		"email_id":emp_doc.leave_approver,
    # 		'send_email':1
    # 	})
    return reports_to

@frappe.whitelist()
def get_all_tasks(task):
    lft,rgt = frappe.db.get_all('Task',filters={'name':task},fields=['lft','rgt'],as_list=True)[0]
    all_tasks = frappe.db.sql('''SELECT name as task,subject from `tabTask` where lft>{0} and rgt <{1} '''.format(lft,rgt),as_dict=1)
    return all_tasks


def has_permission(doc, user):
    assigned_users = []
    participant_doc_assignment = []
    if doc.event_participants:
        for row in doc.event_participants:
            participant_doc = frappe.get_doc(row.reference_doctype,row.reference_docname)
            participant_doc_assignment = participant_doc.get_assigned_users()
            if participant_doc_assignment:
                assigned_users.extend(participant_doc_assignment)
    if doc.event_type == "Public" or doc.owner == user or user in assigned_users:
        return True

    return False


@frappe.whitelist()
def get_default_contact(doctype, name):
	"""
	Returns default contact for the given doctype and name.
	Can be ordered by `contact_type` to either is_primary_contact or is_billing_contact.
	"""
	out = frappe.db.sql(
		"""
			SELECT dl.parent, c.is_primary_contact, c.is_billing_contact,cp.phone
			FROM `tabDynamic Link` dl
			INNER JOIN `tabContact` c ON c.name = dl.parent
            LEFT JOIN `tabContact Phone` cp
            ON cp.parent = dl.parent
			WHERE
				dl.link_doctype=%s AND
				dl.link_name=%s AND
				dl.parenttype = 'Contact'
			ORDER BY is_primary_contact DESC, is_billing_contact DESC
		""",
		(doctype, name),as_dict=1
	)
	if out:
		try:
			return out[0]['phone']
		except Exception:
			return None
	else:
		return None