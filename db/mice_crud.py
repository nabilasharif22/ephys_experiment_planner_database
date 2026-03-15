# db/mice_crud.py

from db.connection import get_connection
from datetime import datetime


# ---------------------------------------------------------
# Helper: Calculate age from DOB
# ---------------------------------------------------------
def calculate_age_days(dob):
    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
    today = datetime.today().date()

    if dob_date > today:
        raise ValueError("DOB cannot be in the future.")

    return (today - dob_date).days


# ---------------------------------------------------------
# Helper: Validate virus injection fields
# ---------------------------------------------------------
def validate_virus_fields(virus_injected, virus_name, virus_injection_date):
    if virus_injected not in (None, "yes", "no"):
        raise ValueError("virus_injected must be 'yes' or 'no'.")

    if virus_injected == "yes":
        if not virus_name:
            raise ValueError("virus_name is required when virus_injected='yes'.")
        if not virus_injection_date:
            raise ValueError("virus_injection_date is required when virus_injected='yes'.")

        inj_date = datetime.strptime(virus_injection_date, "%Y-%m-%d").date()
        today = datetime.today().date()

        if inj_date > today:
            raise ValueError("Virus injection date cannot be in the future.")


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_mouse(
    experiment_id,
    mouse_id_code,
    strain_id=None,
    age_days=None,
    sex=None,
    dob=None,
    virus_injected="no",
    virus_name=None,
    virus_injection_date=None,
    notes=None
):
    # Validate virus fields
    validate_virus_fields(virus_injected, virus_name, virus_injection_date)

    # If DOB is provided, compute age_days automatically
    if dob is not None:
        age_days = calculate_age_days(dob)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO mice (
            experiment_id,
            mouse_id_code,
            strain_id,
            age_days,
            sex,
            dob,
            virus_injected,
            virus_name,
            virus_injection_date,
            notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        experiment_id,
        mouse_id_code,
        strain_id,
        age_days,
        sex,
        dob,
        virus_injected,
        virus_name,
        virus_injection_date,
        notes
    ))

    conn.commit()
    mouse_id = cur.lastrowid
    conn.close()
    return mouse_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_mouse_by_id(mouse_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            experiment_id,
            mouse_id_code,
            strain_id,
            age_days,
            sex,
            dob,
            virus_injected,
            virus_name,
            virus_injection_date,
            notes
        FROM mice
        WHERE id = ?;
    """, (mouse_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "experiment_id": row[1],
        "mouse_id_code": row[2],
        "strain_id": row[3],
        "age_days": row[4],
        "sex": row[5],
        "dob": row[6],
        "virus_injected": row[7],
        "virus_name": row[8],
        "virus_injection_date": row[9],
        "notes": row[10],
    }


# ---------------------------------------------------------
# READ (all mice for an experiment)
# ---------------------------------------------------------
def get_mice_for_experiment(experiment_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            experiment_id,
            mouse_id_code,
            strain_id,
            age_days,
            sex,
            dob,
            virus_injected,
            virus_name,
            virus_injection_date,
            notes
        FROM mice
        WHERE experiment_id = ?;
    """, (experiment_id,))

    rows = cur.fetchall()
    conn.close()

    mice = []
    for row in rows:
        mice.append({
            "id": row[0],
            "experiment_id": row[1],
            "mouse_id_code": row[2],
            "strain_id": row[3],
            "age_days": row[4],
            "sex": row[5],
            "dob": row[6],
            "virus_injected": row[7],
            "virus_name": row[8],
            "virus_injection_date": row[9],
            "notes": row[10],
        })

    return mice


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_mice_for_experiment(experiment_id):
    mice = get_mice_for_experiment(experiment_id)
    print(f"\nMice for experiment {experiment_id}:")
    for m in mice:
        print(
            f"{m['id']}: {m['mouse_id_code']} "
            f"(age={m['age_days']}, sex={m['sex']}, dob={m['dob']}, "
            f"virus={m['virus_injected']}, virus_name={m['virus_name']})"
        )
    return mice


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_mouse_partial(mouse_id, **fields):
    if not fields:
        return 0

    # If DOB is updated, recompute age_days
    if "dob" in fields and fields["dob"] is not None:
        fields["age_days"] = calculate_age_days(fields["dob"])

    # Validate virus fields if any are present
    if any(k in fields for k in ("virus_injected", "virus_name", "virus_injection_date")):
        virus_injected = fields.get("virus_injected")
        virus_name = fields.get("virus_name")
        virus_injection_date = fields.get("virus_injection_date")
        validate_virus_fields(virus_injected, virus_name, virus_injection_date)

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(mouse_id)

    sql = f"UPDATE mice SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_mouse_interactive(mouse_id):
    mouse = get_mouse_by_id(mouse_id)
    if mouse is None:
        print("Mouse not found.")
        return 0

    print("\nYou are about to delete this mouse:")
    print(f"ID: {mouse['id']}")
    print(f"Mouse ID Code: {mouse['mouse_id_code']}")
    print(f"Age: {mouse['age_days']}")
    print(f"Sex: {mouse['sex']}")
    print(f"DOB: {mouse['dob']}")
    print(f"Virus injected: {mouse['virus_injected']}")
    print(f"Virus name: {mouse['virus_name']}")
    print(f"Virus injection date: {mouse['virus_injection_date']}")
    print(f"Notes: {mouse['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mice WHERE id = ?;", (mouse_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Mouse deleted.")
    else:
        print("Deletion failed.")

    return affected



def get_all_mice():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            experiment_id,
            mouse_id_code,
            strain_id,
            age_days,
            sex,
            dob,
            virus_injected,
            virus_name,
            virus_injection_date,
            notes
        FROM mice;
    """)

    rows = cur.fetchall()
    conn.close()

    mice = []
    for row in rows:
        mice.append({
            "id": row[0],
            "experiment_id": row[1],
            "mouse_id_code": row[2],
            "strain_id": row[3],
            "age_days": row[4],
            "sex": row[5],
            "dob": row[6],
            "virus_injected": row[7],
            "virus_name": row[8],
            "virus_injection_date": row[9],
            "notes": row[10],
        })

    return mice


def list_mice():
    mice = get_all_mice()
    print("\nAll Mice:")
    for m in mice:
        print(
            f"{m['id']}: Mouse {m['mouse_id_code']} | "
            f"Exp={m['experiment_id']} | Strain={m['strain_id']} | "
            f"Sex={m['sex']} | DOB={m['dob']} | Age={m['age_days']} | "
            f"Virus={m['virus_injected']} | Notes={m['notes']}"
        )
    return mice

