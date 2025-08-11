ADGM_CHECKLISTS = {
    "Company Incorporation": [
        "Articles of Association",
        "Memorandum of Association",
        "Board Resolution",
        "Incorporation Application Form",
        "Register of Members and Directors"
    ],
    "Licensing": [
        "License Application",
        "Business Plan",
        "Compliance Policy"
    ]
}

def identify_process(uploaded_files):
    """Identify the process based on uploaded file names."""
    filenames = [f["name"].lower() for f in uploaded_files]  # Accessing the 'name' key
    
    if any("article" in f for f in filenames):
        return "Company Incorporation"
    elif any("license" in f for f in filenames):
        return "Licensing"
    return "Unknown Process"

def identify_document_type(filename):
    """Identify the document type based on the filename."""
    if "articles of association" in filename:
        return "Articles of Association"
    elif "memorandum of association" in filename:
        return "Memorandum of Association"
    elif "board resolution" in filename:
        return "Board Resolution"
    elif "incorporation application form" in filename:
        return "Incorporation Application Form"
    elif "register of members and directors" in filename:
        return "Register of Members and Directors"
    elif "license application" in filename:
        return "License Application"
    elif "business plan" in filename:
        return "Business Plan"
    elif "compliance policy" in filename:
        return "Compliance Policy"
    return "Unknown Document"

def validate_checklist(uploaded_files):
    """Validate uploaded files against the required checklist."""
    process = identify_process(uploaded_files)
    required = ADGM_CHECKLISTS.get(process, [])
    uploaded_types = [identify_document_type(f["name"].lower()) for f in uploaded_files]  # Accessing the 'name' key
    
    missing = [doc for doc in required if doc not in uploaded_types]
    
    return {
        "process": process,
        "documents_uploaded": len(uploaded_files),
        "required_documents": len(required),
        "missing_documents": missing,
        "is_complete": len(missing) == 0
    }

# Example usage
uploaded_files = [
    {"name": "Articles of Association.docx"},
    {"name": "Memorandum of Association.docx"},
    {"name": "Board Resolution.docx"},
    {"name": "Incorporation Application Form.docx"},
    {"name": "Register of Members and Directors.docx"}
]

result = validate_checklist(uploaded_files)
print(result)
