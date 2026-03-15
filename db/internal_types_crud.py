# db/internal_types_crud.py

from db.connection import get_connection
from db.drugs_crud import get_drug_by_id


# ---------------------------------------------------------
# CREATE INTERNAL TYPE
# ---------------------------------------------------------
def create_internal_type(name, notes=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO internal_types (
            name,
            notes
        ) VALUES (?, ?);
    """, (name, notes))

    conn.commit()
    internal_id = cur.lastrowid
    conn.close()
    return internal_id


# ---------------------------------------------------------
# ADD DRUG/ADDITIVE TO INTERNAL TYPE
# ---------------------------------------------------------
def add_drug_to_internal(internal_type_id, drug_id, concentration):
    # Validate drug exists
    if get_drug_by_id(drug_id) is None:
        raise ValueError(f"Drug with id {drug_id} does not exist.")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO internal_type_drugs (
            internal_type_id,
            drug_id,
            concentration
        ) VALUES (?, ?, ?);
    """, (internal_type_id, drug_id, concentration))

    conn.commit()
    link_id = cur.lastrowid
    conn.close()
    return link_id


# ---------------------------------------------------------
# READ (single internal type)
# ---------------------------------------------------------
def get_internal_type_by_id(internal_type_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            notes
        FROM internal_types
        WHERE id = ?;
    """, (internal_type_id,))

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
# READ (internal type with full drug list)
# ---------------------------------------------------------
def get_internal_type_with_drugs(internal_type_id):
    internal = get_internal_type_by_id(internal_type_id)
    if internal is None:
        return None

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            internal_type_drugs.id,
            internal_type_drugs.drug_id,
            drugs.name,
            internal_type_drugs.concentration
        FROM internal_type_drugs
        JOIN drugs ON internal_type_drugs.drug_id = drugs.id
        WHERE internal_type_drugs.internal_type_id = ?;
    """, (internal_type_id,))

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

    internal["drugs"] = drugs
    return internal


# ---------------------------------------------------------
# READ (all internal types)
# ---------------------------------------------------------
def get_all_internal_types():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            notes
        FROM internal_types;
    """)

    rows = cur.fetchall()
    conn.close()

    internal_list = []
    for row in rows:
        internal_list.append({
            "id": row[0],
            "name": row[1],
            "notes": row[2],
        })

    return internal_list


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_internal_types():
    internal_list = get_all_internal_types()
    print("\nInternal Solution Types:")
    for i in internal_list:
        print(f"{i['id']}: {i['name']} (notes={i['notes']})")
    return internal_list


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_internal_type_partial(internal_type_id, **fields):
    if not fields:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(internal_type_id)

    sql = f"UPDATE internal_types SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_internal_type_interactive(internal_type_id):
    internal = get_internal_type_by_id(internal_type_id)
    if internal is None:
        print("Internal type not found.")
        return 0

    print("\nYou are about to delete this internal solution type:")
    print(f"ID: {internal['id']}")
    print(f"Name: {internal['name']}")
    print(f"Notes: {internal['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()

    # Delete linked drugs first
    cur.execute("DELETE FROM internal_type_drugs WHERE internal_type_id = ?;", (internal_type_id,))

    # Delete internal type
    cur.execute("DELETE FROM internal_types WHERE id = ?;", (internal_type_id,))

    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Internal type deleted.")
    else:
        print("Deletion failed.")

    return affected
