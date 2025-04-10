import datetime
import requests

# TestWiki API endpoint
WIKI_API_URL = "https://testwiki.wiki/api.php"

# Bot credentials
BOT_USERNAME = ""
BOT_PASSWORD = ""

# User groups to include (excluding stewards)
USER_GROUPS = ["sysop", "bureaucrat", "interface-admin", "non-stewardsuppress"]

# Users to exclude
EXCLUDED_USERS = {"EPIC", "Dmehus", "Drummingman", "Justarandomamerican", "MacFan4000", "Abuse filter", "Bosco-bot", "DodoBot", "FuzzyBot", "MacFanBot", "Paflidychat"}

# Login to the wiki
def login():
    session = requests.Session()
    login_token_res = session.get(WIKI_API_URL, params={
        "action": "query", "meta": "tokens", "type": "login", "format": "json"
    })
    login_token = login_token_res.json()["query"]["tokens"]["logintoken"]
    session.post(WIKI_API_URL, data={
        "action": "login", "lgname": BOT_USERNAME, "lgpassword": BOT_PASSWORD,
        "lgtoken": login_token, "format": "json"
    })
    return session

# Get last activity
def get_last_activity(username, session):
    params = {
        "action": "query", "list": "usercontribs|logevents", "ucuser": username,
        "ucprop": "timestamp", "leuser": username, "leprop": "timestamp", "format": "json"
    }
    response = session.get(WIKI_API_URL, params=params).json()
    edits = response.get("query", {}).get("usercontribs", [])
    logs = response.get("query", {}).get("logevents", [])
    last_edit_time = edits[0]["timestamp"] if edits else None
    last_log_time = logs[0]["timestamp"] if logs else None
    last_activity = max(filter(None, [last_edit_time, last_log_time]), default=None)
    return datetime.datetime.strptime(last_activity, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc) if last_activity else None

# Determine activity status
def get_activity_status(last_activity):
    now = datetime.datetime.now(datetime.timezone.utc)
    if last_activity is None:
        return "Never Active"
    time_diff = (now - last_activity).days
    if time_diff <= 30:
        return '<span style="color: green;">Active</span>'
    elif time_diff <= 60:
        return '<span style="color: orange;">Inactive (1 month)</span>'
    elif time_diff <= 75:
        return '<span style="color: red;">Inactive (2 months)</span>'
    else:
        return '<span style="color: red; font-weight: bold;">Inactive (2 months, 2 weeks)</span>'

# Fetch users in groups, excluding stewards and specified users
def get_users_by_group(session):
    all_users = {}
    for group in USER_GROUPS:
        params = {"action": "query", "list": "allusers", "augroup": group, "auprop": "name", "aulimit": "max", "format": "json"}
        while True:
            response = session.get(WIKI_API_URL, params=params).json()
            for user in response.get("query", {}).get("allusers", []):
                if user["name"] not in EXCLUDED_USERS:
                    all_users[user["name"]] = group
            if "continue" in response:
                params.update(response["continue"])
            else:
                break
    return sorted(all_users.keys())

# Generate report
def generate_report():
    session = login()
    last_updated = datetime.datetime.now(datetime.timezone.utc).strftime("%d-%m-%Y %H:%M UTC")
    report_content = f"== Last updated: {last_updated} ==\n\n"
    report_content += "== Admins, Bureaucrats, Interface Admins, and Non-Steward Suppressors ==\n\n"
    report_content += '{| class="wikitable"\n! Username !! Last Action !! Status\n'
    users = get_users_by_group(session)
    grace_period_entries = []
    
    for user in users:
        last_activity = get_last_activity(user, session)
        if last_activity:
            last_activity_str = last_activity.strftime("%d-%m-%Y")
            if (datetime.datetime.now(datetime.timezone.utc) - last_activity).days > 75:
                grace_period = (last_activity + datetime.timedelta(days=90)).strftime("%d-%m-%Y")
                grace_period_entries.append(f"# {user} ; {last_activity_str} ; {grace_period}")
        else:
            last_activity_str = "Never"
        status = get_activity_status(last_activity)
        report_content += f"|-\n| [[User:{user}|{user}]] || {last_activity_str} || {status}\n"
    
    report_content += "|}\n\n"
    if grace_period_entries:
        report_content += "== Grace Periods ==\n" + "\n".join(grace_period_entries) + "\n"
    
    edit_params = {
        "action": "edit", "title": "Activity", "text": report_content,
        "summary": "Updating activity report",
        "token": session.get(WIKI_API_URL, params={"action": "query", "meta": "tokens", "format": "json"}).json()["query"]["tokens"]["csrftoken"],
        "format": "json"
    }
    session.post(WIKI_API_URL, data=edit_params)

if __name__ == "__main__":
    generate_report()
