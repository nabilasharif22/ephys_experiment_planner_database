# db/experiments_crud.py
from db.connection import get_connection

# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_experiment(
    name,
    min_mice=None,
    cells_per_mouse=None,
    drugs_summary=None,
    notes=None,
    acsf_type_id=None,
    internal_type_id=None,
    mouse_strain_id=None,
    ideal_mouse_age_min=None,
    ideal_mouse_age_max=None,
    experiment_for_person_id=None,
    project_id=None
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO experiments (
            name,
            min_mice,
            cells_per_mouse,
            drugs_summary,
            acsf_type_id,
            internal_type_id,
            mouse_strain_id,
            ideal_mouse_age_min,
            ideal_mouse_age_max,
            experiment_for_person_id,
            project_id,
            notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        name,
        min_mice,
        cells_per_mouse,
        drugs_summary,
        acsf_type_id,
        internal_type_id,
        mouse_strain_id,
        ideal_mouse_age_min,
        ideal_mouse_age_max,
        experiment_for_person_id,
        project_id,
        notes
    ))

    conn.commit()
    experiment_id = cur.lastrowid
    conn.close()
    return experiment_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_experiment_by_id(experiment_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            min_mice,
            cells_per_mouse,
            drugs_summary,
            acsf_type_id,
            internal_type_id,
            mouse_strain_id,
            ideal_mouse_age_min,
            ideal_mouse_age_max,
            experiment_for_person_id,
            project_id,
            notes
        FROM experiments
        WHERE id = ?;
    """, (experiment_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "min_mice": row[2],
        "cells_per_mouse": row[3],
        "drugs_summary": row[4],
        "acsf_type_id": row[5],
        "internal_type_id": row[6],
        "mouse_strain_id": row[7],
        "ideal_mouse_age_min": row[8],
        "ideal_mouse_age_max": row[9],
        "experiment_for_person_id": row[10],
        "project_id": row[11],
        "notes": row[12],
    }


# ---------------------------------------------------------
# READ (all)
# ---------------------------------------------------------
def get_all_experiments():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            min_mice,
            cells_per_mouse,
            drugs_summary,
            acsf_type_id,
            internal_type_id,
            mouse_strain_id,
            ideal_mouse_age_min,
            ideal_mouse_age_max,
            experiment_for_person_id,
            project_id,
            notes
        FROM experiments;
    """)

    rows = cur.fetchall()
    conn.close()

    experiments = []
    for row in rows:
        experiments.append({
            "id": row[0],
            "name": row[1],
            "min_mice": row[2],
            "cells_per_mouse": row[3],
            "drugs_summary": row[4],
            "acsf_type_id": row[5],
            "internal_type_id": row[6],
            "mouse_strain_id": row[7],
            "ideal_mouse_age_min": row[8],
            "ideal_mouse_age_max": row[9],
            "experiment_for_person_id": row[10],
            "project_id": row[11],
            "notes": row[12],
        })

    return experiments


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_experiments():
    experiments = get_all_experiments()
    print("\nAvailable Experiments:")
    for exp in experiments:
        print(f"{exp['id']}: {exp['name']} (mice={exp['min_mice']}, cells={exp['cells_per_mouse']})")
    return experiments


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_experiment_partial(experiment_id, **fields):
    if not fields:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(experiment_id)

    sql = f"UPDATE experiments SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_experiment_interactive(experiment_id):
    exp = get_experiment_by_id(experiment_id)
    if exp is None:
        print("Experiment not found.")
        return 0

    print("\nYou are about to delete this experiment:")
    print(f"ID: {exp['id']}")
    print(f"Name: {exp['name']}")
    print(f"Drugs: {exp['drugs_summary']}")
    print(f"Notes: {exp['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM experiments WHERE id = ?;", (experiment_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Experiment deleted.")
    else:
        print("Deletion failed.")

    return affected
