# db/drugs_crud.py

from db.connection import get_connection
from datetime import datetime


# ---------------------------------------------------------
# Helper: Validate aliquoting fields
# ---------------------------------------------------------
def validate_aliquot_fields(aliquoted, aliquot_date, aliquot_volume):
    if aliquoted not in (None, "yes", "no"):
        raise ValueError("aliquoted must be 'yes' or 'no'.")

    if aliquoted == "yes":
        if not aliquot_date:
            raise ValueError("aliquot_date is required when aliquoted='yes'.")
        if not aliquot_volume:
            raise ValueError("aliquot_volume is required when aliquoted='yes'.")

        # Validate date format and ensure it's not in the future
        date_obj = datetime.strptime(aliquot_date, "%Y-%m-%d").date()
        today = datetime.today().date()

        if date_obj > today:
            raise ValueError("Aliquot date cannot be in the future.")


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_drug(
    name,
    stock_concentration=None,
    vendor=None,
    aliquoted="no",
    aliquot_date=None,
    aliquot_volume=None,
    notes=None
):
    validate_aliquot_fields(aliquoted, aliquot_date, aliquot_volume)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO drugs (
            name,
            stock_concentration,
            vendor,
            aliquoted,
            aliquot_date,
            aliquot_volume,
            notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        name,
        stock_concentration,
        vendor,
        aliquoted,
        aliquot_date,
        aliquot_volume,
        notes
    ))

    conn.commit()
    drug_id = cur.lastrowid
    conn.close()
    return drug_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_drug_by_id(drug_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            stock_concentration,
            vendor,
            aliquoted,
            aliquot_date,
            aliquot_volume,
            notes
        FROM drugs
        WHERE id = ?;
    """, (drug_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "stock_concentration": row[2],
        "vendor": row[3],
        "aliquoted": row[4],
        "aliquot_date": row[5],
        "aliquot_volume": row[6],
        "notes": row[7],
    }


# ---------------------------------------------------------
# READ (all)
# ---------------------------------------------------------
def get_all_drugs():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            stock_concentration,
            vendor,
            aliquoted,
            aliquot_date,
            aliquot_volume,
            notes
        FROM drugs;
    """)

    rows = cur.fetchall()
    conn.close()

    drugs = []
    for row in rows:
        drugs.append({
            "id": row[0],
            "name": row[1],
            "stock_concentration": row[2],
            "vendor": row[3],
            "aliquoted": row[4],
            "aliquot_date": row[5],
            "aliquot_volume": row[6],
            "notes": row[7],
        })

    return drugs


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_drugs():
    drugs = get_all_drugs()
    print("\nAvailable Drugs:")
    for d in drugs:
        print(
            f"{d['id']}: {d['name']} "
            f"(conc={d['stock_concentration']}, vendor={d['vendor']}, "
            f"aliquoted={d['aliquoted']}, date={d['aliquot_date']})"
        )
    return drugs


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_drug_partial(drug_id, **fields):
    if not fields:
        return 0

    # Validate aliquoting fields if present
    if any(k in fields for k in ("aliquoted", "aliquot_date", "aliquot_volume")):
        aliquoted = fields.get("aliquoted")
        aliquot_date = fields.get("aliquot_date")
        aliquot_volume = fields.get("aliquot_volume")
        validate_aliquot_fields(aliquoted, aliquot_date, aliquot_volume)

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(drug_id)

    sql = f"UPDATE drugs SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_drug_interactive(drug_id):
    drug = get_drug_by_id(drug_id)
    if drug is None:
        print("Drug not found.")
        return 0

    print("\nYou are about to delete this drug:")
    print(f"ID: {drug['id']}")
    print(f"Name: {drug['name']}")
    print(f"Stock concentration: {drug['stock_concentration']}")
    print(f"Vendor: {drug['vendor']}")
    print(f"Aliquoted: {drug['aliquoted']}")
    print(f"Aliquot date: {drug['aliquot_date']}")
    print(f"Aliquot volume: {drug['aliquot_volume']}")
    print(f"Notes: {drug['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM drugs WHERE id = ?;", (drug_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Drug deleted.")
    else:
        print("Deletion failed.")

    return affected
