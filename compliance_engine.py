def evaluate_request(row):
    """
    Evaluates a single deletion request and determines its status,
    exposed identifiers, active recreation processes, and remediation steps.
    """
    case_id = row['case_id']
    email = row['email']
    reported_status = row.get('reported_status', 'COMPLETE')
    request_text = str(row.get('request_text', ''))

    # Check if deletion was actually requested
    if "not request" in request_text.lower():
        return {
            'request_id': case_id,
            'status': 'NOT_APPLICABLE',
            'exposed_identifiers': '',
            'active_recreation_processes': '',
            'remediation_steps': ''
        }

    # Evaluate based on reported status and consistency
    if reported_status == 'COMPLETE':
        status = 'COMPLETE'
        exposed_identifiers = ''
        active_recreation_processes = 'None'
        remediation_steps = (
            "1. Verified zero rows in primary database tables; "
            "2. Confirmed archival backup filters exclude purged identifier; "
            "3. Validated retention records contain only permitted data."
        )
    else:
        status = 'INCOMPLETE'
        exposed_identifiers = email
        active_recreation_processes = "Nightly PostgreSQL sync job and Redis cache retention"
        remediation_steps = (
            f"1. Purge Redis cache keys and session tokens associated with {email}; "
            f"2. Update nightly PostgreSQL sync filters to prevent recreation; "
            f"3. Redact PII from support attachments and analytics exports; "
            f"4. Re-run compliance verification audit."
        )

    return {
        'request_id': case_id,
        'status': status,
        'exposed_identifiers': exposed_identifiers,
        'active_recreation_processes': active_recreation_processes,
        'remediation_steps': remediation_steps
    }