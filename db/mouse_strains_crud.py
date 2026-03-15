# db/mouse_strains_crud.py

from db.connection import get_connection


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_mouse_strain(name, genotype=None, notes=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO mouse_strains (
            name,
            genotype,
            notes
        ) VALUES (?, ?, ?);
    """, (name, genotype, notes))

    conn.commit()
    strain_id = cur.lastrowid
    conn.close()
    return strain_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_mouse_strain_by_id(strain_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            genotype,
            notes
        FROM mouse_strains
        WHERE id = ?;
    """, (strain_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "genotype": row[2],
        "notes": row[3],
    }


# ---------------------------------------------------------
# READ (all)
# ---------------------------------------------------------
def get_all_mouse_strains():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            genotype,
            notes
        FROM mouse_strains;
    """)

    rows = cur.fetchall()
    conn.close()

    strains = []
    for row in rows:
        strains.append({
            "id": row[0],
            "name": row[1],
            "genotype": row[2],
            "notes": row[3],
        })

    return strains


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_mouse_strains():
    strains = get_all_mouse_strains()
    print("\nMouse Strains:")
    for s in strains:
        print(
            f"{s['id']}: {s['name']} "
            f"(genotype={s['genotype']}, notes={s['notes']})"
        )
    return strains


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_mouse_strain_partial(strain_id, **fields):
    if not fields:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(strain_id)

    sql = f"UPDATE mouse_strains SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_mouse_strain_interactive(strain_id):
    strain = get_mouse_strain_by_id(strain_id)
    if strain is None:
        print("Mouse strain not found.")
        return 0

    print("\nYou are about to delete this mouse strain:")
    print(f"ID: {strain['id']}")
    print(f"Name: {strain['name']}")
    print(f"Genotype: {strain['genotype']}")
    print(f"Notes: {strain['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mouse_strains WHERE id = ?;", (strain_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Mouse strain deleted.")
    else:
        print("Deletion failed.")

    return affected
