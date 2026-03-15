# db/acsf_types_crud.py

from db.connection import get_connection
from db.drugs_crud import get_drug_by_id


# ---------------------------------------------------------
# CREATE ACSF TYPE
# ---------------------------------------------------------
def create_acsf_type(name, notes=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO acsf_types (
            name,
            notes
        ) VALUES (?, ?);
    """, (name, notes))

    conn.commit()
    acsf_id = cur.lastrowid
    conn.close()
    return acsf_id


# ---------------------------------------------------------
# ADD DRUG TO ACSF TYPE
# ---------------------------------------------------------
def add_drug_to_acsf(acsf_type_id, drug_id, concentration):
    # Validate drug exists
    if get_drug_by_id(drug_id) is None:
        raise ValueError(f"Drug with id {drug_id} does not exist.")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO acsf_type_drugs (
            acsf_type_id,
            drug_id,
            concentration
        ) VALUES (?, ?, ?);
    """, (acsf_type_id, drug_id, concentration))

    conn.commit()
    link_id = cur.lastrowid
    conn.close()
    return link_id


# ---------------------------------------------------------
# READ (single ACSF type)
# ---------------------------------------------------------
def get_acsf_type_by_id(acsf_type_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            notes
        FROM acsf_types
        WHERE id = ?;
    """, (acsf_type_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "notes": row[2],
    }


# ---------------------------------------------------------
# READ (ACSF type with full drug list)
# ---------------------------------------------------------
def get_acsf_type_with_drugs(acsf_type_id):
    acsf = get_acsf_type_by_id(acsf_type_id)
    if acsf is None:
        return None

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            acsf_type_drugs.id,
            acsf_type_drugs.drug_id,
            drugs.name,
            acsf_type_drugs.concentration
        FROM acsf_type_drugs
        JOIN drugs ON acsf_type_drugs.drug_id = drugs.id
        WHERE acsf_type_drugs.acsf_type_id = ?;
    """, (acsf_type_id,))

    rows = cur.fetchall()
    conn.close()

    drugs = []
    for row in rows:
        drugs.append({
            "link_id": row[0],
            "drug_id": row[1],
            "drug_name": row[2],
            "concentration": row[3],
        })

    acsf["drugs"] = drugs
    return acsf


# ---------------------------------------------------------
# READ (all ACSF types)
# ---------------------------------------------------------
def get_all_acsf_types():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            notes
        FROM acsf_types;
    """)

    rows = cur.fetchall()
    conn.close()

    acsf_list = []
    for row in rows:
        acsf_list.append({
            "id": row[0],
            "name": row[1],
            "notes": row[2],
        })

    return acsf_list


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_acsf_types():
    acsf_list = get_all_acsf_types()
    print("\nACSF Types:")
    for a in acsf_list:
        print(f"{a['id']}: {a['name']} (notes={a['notes']})")
    return acsf_list


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_acsf_type_partial(acsf_type_id, **fields):
    if not fields:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(acsf_type_id)

    sql = f"UPDATE acsf_types SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_acsf_type_interactive(acsf_type_id):
    acsf = get_acsf_type_by_id(acsf_type_id)
    if acsf is None:
        print("ACSF type not found.")
        return 0

    print("\nYou are about to delete this ACSF type:")
    print(f"ID: {acsf['id']}")
    print(f"Name: {acsf['name']}")
    print(f"Notes: {acsf['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()

    # Delete linked drugs first
    cur.execute("DELETE FROM acsf_type_drugs WHERE acsf_type_id = ?;", (acsf_type_id,))

    # Delete ACSF type
    cur.execute("DELETE FROM acsf_types WHERE id = ?;", (acsf_type_id,))

    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("ACSF type deleted.")
    else:
        print("Deletion failed.")

    return affected
