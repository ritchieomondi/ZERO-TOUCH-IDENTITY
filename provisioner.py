import pandas as pd
import time

def run_provisioning_pipeline(df, progress_callback=None):
    results = []
    total_rows = len(df)
    existing_usernames = set()

    # Department RBAC Mappings
    group_map = {
        "Engineering": ["GRP_ENG_ALL", "GRP_GITHUB_ACCESS"],
        "IT": ["GRP_IT_ALL", "GRP_SYSADMIN_ACCESS"]
    }

    for index, row in df.iterrows():
        emp_id = str(row.get('Employee_ID', '')).strip()
        full_name = str(row.get('Full_Name', '')).strip()
        department = str(row.get('Department', '')).strip()
        role = str(row.get('Role', '')).strip()
        location = str(row.get('Location', '')).strip()

        # Parse First/Last Name from Full_Name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Collision Handling
        base_username = f"{first_name[0]}{last_name}".replace(" ", "").lower() if first_name and last_name else emp_id.lower()
        username = base_username
        counter = 1

        while username in existing_usernames:
            username = f"{base_username}{counter}"
            counter += 1

        existing_usernames.add(username)
        assigned_groups = group_map.get(department, ["GRP_DEFAULT_USERS"])

        # Simulated Execution Step
        time.sleep(0.2)

        results.append({
            "Employee ID": emp_id,
            "Username": username,
            "Full Name": full_name,
            "Department": department,
            "Location": location,
            "Target OU": f"OU={location},OU=Employees,DC=company,DC=local",
            "Assigned Groups": ", ".join(assigned_groups),
            "Status": "Provisioned"
        })

        if progress_callback:
            progress_callback((index + 1) / total_rows)

    return pd.DataFrame(results)