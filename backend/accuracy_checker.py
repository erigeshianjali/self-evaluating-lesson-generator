
from evidence_checker import check_evidence


def check_accuracy(claims, reference_text, source_name, source_url):

    # Step 1: Compare lesson claims with reference material
    evidence_result = check_evidence(
        claims,
        reference_text
    )

    # Step 2: Collect claims that need human review
    claims_for_review = [
        item["claim"]
        for item in evidence_result["results"]
        if item["status"] != "POTENTIAL_SUPPORT"
    ]

    # Step 3: Keep accuracy pending until human verification
    return {
        "status": "PENDING",
        "feedback": (
            "Evidence comparison completed. "
            "Human verification is required before approval."
        ),
        "evidence_results": evidence_result["results"],
        "claims_for_review": claims_for_review,
        "source": {
            "name": source_name,
            "url": source_url
        }
    }
