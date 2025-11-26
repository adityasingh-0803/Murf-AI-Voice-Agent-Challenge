from livekit.agents import tool

leads_db = []  # simple in-memory store

@tool
def create_lead(
    name: str,
    company: str,
    role: str,
    email: str,
    phone: str = "",
    use_case: str = ""
):
    """
    Save a lead for SDR follow-up.
    """
    leads_db.append({
        "name": name,
        "company": company,
        "role": role,
        "email": email,
        "phone": phone,
        "use_case": use_case
    })

    return (
        f"Thanks {name}. I’ve saved your details. Our team will "
        "reach out shortly with more information."
    )
