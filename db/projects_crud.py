# db/projects_crud.py

from db.connection import get_connection
from datetime import datetime


# ---------------------------------------------------------
# Helper: Validate start date
# ---------------------------------------------------------
def validate_start_date(start_date):
    if start_date is None:
        return
    try:
        date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("start_date must be in YYYY-MM-DD format.")
    if date_obj > datetime.today().date():
        raise ValueError("start_date cannot be in the future.")


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_project(name, description=None, pi=None, start_date=None, notes=None):
    validate_start_date(start_date)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO projects (
            name,
            description,
            pi,
            start_date,
            notes
        ) VALUES (?, ?, ?, ?, ?);
    """, (name, description, pi, start_date, notes))

    conn.commit()
    project_id = cur.lastrowid
    conn.close()
    return project_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_project_by_id(project_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            description,
            pi,
            start_date,
            notes
        FROM projects
        WHERE id = ?;
    """, (project_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "pi": row[3],
        "start_date": row[4],
        "notes": row[5],
    }


# ---------------------------------------------------------
# READ (all)
# ---------------------------------------------------------
def get_all_projects():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            description,
            pi,
            start_date,
            notes
        FROM projects;
    """)

    rows = cur.fetchall()
    conn.close()

    projects = []
    for row in rows:
        projects.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "pi": row[3],
            "start_date": row[4],
            "notes": row[5],
        })

    return projects


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_projects():
    projects = get_all_projects()
    print("\nProjects:")
    for p in projects:
        print(
            f"{p['id']}: {p['name']} "
            f"(PI={p['pi']}, start={p['start_date']}, notes={p['notes']})"
        )
    return projects


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_project_partial(project_id, **fields):
    if not fields:
        return 0

    # Validate start_date if present
    if "start_date" in fields:
        validate_start_date(fields["start_date"])

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(project_id)

    sql = f"UPDATE projects SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_project_interactive(project_id):
    project = get_project_by_id(project_id)
    if project is None:
        print("Project not found.")
        return 0

    print("\nYou are about to delete this project:")
    print(f"ID: {project['id']}")
    print(f"Name: {project['name']}")
    print(f"PI: {project['pi']}")
    print(f"Start date: {project['start_date']}")
    print(f"Description: {project['description']}")
    print(f"Notes: {project['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM projects WHERE id = ?;", (project_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Project deleted.")
    else:
        print("Deletion failed.")

    return affected
