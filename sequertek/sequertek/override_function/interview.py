import frappe
import json 
from frappe import _

@frappe.whitelist()
def get_assessment_details(parenttype, parent, parentfield_s):
    parentfield = json.loads(parentfield_s)

    assessment_details = {}

    for field in parentfield:
        details = frappe.get_all(
            "Assessment Table",
            fields=["skill", "rating"],
            filters={
                "parent": parent,
                "parenttype": parenttype,
                "parentfield": field
            },
            order_by="idx"
        )
        assessment_details[field] = details

    # Make sure the parent and parenttype are correct for Skill Assessment
    # details = frappe.get_all(
	# 	"Skill Assessment", filters={"parentfield":"skill_assessment","parenttype":"Interview Feedback"}, fields=["skill","rating"], order_by="idx"
	# )
    
    # assessment_details["skill_assessment"] = details
    # Fetching key strengths and key areas as additional fields
    key_strengths = frappe.get_value("Interview Feedback", parent, "key_strengths")
    key_areas = frappe.get_value("Interview Feedback", parent, "key_areas")
    
    # Adding these fields to the assessment details
    assessment_details["key_strengths"] = key_strengths
    assessment_details["key_areas"] = key_areas

    return assessment_details


@frappe.whitelist()
def create_interview_feedback(data, interview_name, interviewer, job_applicant):
    # if frappe.db.exists("Interview Feedback",{
	# 			interviewer: frappe.session.user,
	# 			interview: interview_name,
	# 			docstatus: ("!=", 2),
	# 		}): frappe.throw("Feedback Exsist!!")

    if isinstance(data, str):
        data = frappe._dict(json.loads(data))

    if frappe.session.user != interviewer:
        frappe.throw(_("Only Interviewers are allowed to submit Interview Feedback"))

    interview_feedback = frappe.new_doc("Interview Feedback")
    interview_feedback.interview = interview_name
    interview_feedback.interviewer = interviewer
    interview_feedback.job_applicant = job_applicant

    # Handle behavioral, attributes, and technical assessments
    if "behavioral" in data:
        for d in data.behavioral:
            d = frappe._dict(d)
            interview_feedback.append("skill_assessment", {"skill": d.skill, "rating": d.rating})

    if "attributes" in data:
        for d in data.attributes:
            d = frappe._dict(d)
            interview_feedback.append("attributes", {"skill": d.skill, "rating": d.rating})

    if "technical" in data:
        for d in data.technical:
            d = frappe._dict(d)
            interview_feedback.append("technical", {"skill": d.skill, "rating": d.rating})

    # if "skill_assessment" in data:
    #     for d in data.skill_assessment:
    #         d = frappe._dict(d)
    #         interview_feedback.append("skill_assessment", {"skill": d.skill, "rating": d.rating})

    

    # Handle feedback and result
    interview_feedback.feedback = data.feedback
    interview_feedback.result = data.result
    interview_feedback.key_strengths = data.key_strengths
    frappe.logger().info(f"Key Strengths: {data.key_strengths}")
    interview_feedback.key_areas = data.key_areas
    frappe.logger().info(f"Key Areas: {data.key_areas}")


    interview_feedback.flags.ignore_mandatory = True

   
    interview_feedback.insert()
    interview_feedback.submit()


    frappe.msgprint(
        _("Interview Feedback {0} submitted successfully").format(
            frappe.utils.get_link_to_form("Interview Feedback", interview_feedback.name)
        )
    )

