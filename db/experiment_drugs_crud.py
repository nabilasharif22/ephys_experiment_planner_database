# db/experiment_drugs_crud.py

from db.connection import get_connection
from db.experiments_crud import get_experiment_by_id
from db.drugs_crud import get_drug_by_id


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------
def validate_experiment_and_drug(experiment_id, drug_id):
    if get_experiment_by_id(experiment_id) is None:
        raise ValueError(f"Experiment with id {experiment_id} does not exist.")

    if get_drug_by_id(drug_id) is None:
        raise ValueError(f"Drug with id {drug_id} does not exist.")


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_experiment_drug(
    experiment_id,
    drug_id,
    stock_concentration=None,
    desired_concentration=None,
    volume_to_add=None,
    notes=None
):
    validate_experiment_and_drug(experiment_id, drug_id)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO experiment_drugs (
            experiment_id,
            drug_id,
            stock_concentration,
            desired_concentration,
            volume_to_add,
            notes
        ) VALUES (?, ?, ?, ?, ?, ?);
    """, (
        experiment_id,
        drug_id,
        stock_concentration,
        desired_concentration,
        volume_to_add,
        notes
    ))

    conn.commit()
    ed_id = cur.lastrowid
    conn.close()
    return ed_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_experiment_drug_by_id(ed_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            experiment_id,
            drug_id,
            stock_concentration,
            desired_concentration,
            volume_to_add,
            notes
        FROM experiment_drugs
        WHERE id = ?;
    """, (ed_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "experiment_id": row[1],
        "drug_id": row[2],
        "stock_concentration": row[3],
        "desired_concentration": row[4],
        "volume_to_add": row[5],
        "notes": row[6],
    }


# ---------------------------------------------------------
# READ (all for experiment)
# ---------------------------------------------------------
def get_drugs_for_experiment(experiment_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            experiment_id,
            drug_id,
            stock_concentration,
            desired_concentration,
            volume_to_add,
            notes
        FROM experiment_drugs
        WHERE experiment_id = ?;
    """, (experiment_id,))

    rows = cur.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "experiment_id": row[1],
            "drug_id": row[2],
            "stock_concentration": row[3],
            "desired_concentration": row[4],
            "volume_to_add": row[5],
            "notes": row[6],
        })

    return results


# ---------------------------------------------------------
# READ (all for drug)
# ---------------------------------------------------------
def get_experiments_for_drug(drug_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            experiment_id,
            drug_id,
            stock_concentration,
            desired_concentration,
            volume_to_add,
            notes
        FROM experiment_drugs
        WHERE drug_id = ?;
    """, (drug_id,))

    rows = cur.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "experiment_id": row[1],
            "drug_id": row[2],
            "stock_concentration": row[3],
            "desired_concentration": row[4],
            "volume_to_add": row[5],
            "notes": row[6],
        })

    return results


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_drugs_for_experiment(experiment_id):
    items = get_drugs_for_experiment(experiment_id)
    print(f"\nDrugs for experiment {experiment_id}:")
    for d in items:
        print(
            f"{d['id']}: drug_id={d['drug_id']} "
            f"(stock={d['stock_concentration']}, desired={d['desired_concentration']}, "
            f"volume={d['volume_to_add']})"
        )
    return items


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_experiment_drug_partial(ed_id, **fields):
    if not fields:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(ed_id)

    sql = f"UPDATE experiment_drugs SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_experiment_drug_interactive(ed_id):
    item = get_experiment_drug_by_id(ed_id)
    if item is None:
        print("Experiment-drug entry not found.")
        return 0

    print("\nYou are about to delete this experiment-drug entry:")
    print(f"ID: {item['id']}")
    print(f"Experiment ID: {item['experiment_id']}")
    print(f"Drug ID: {item['drug_id']}")
    print(f"Stock concentration: {item['stock_concentration']}")
    print(f"Desired concentration: {item['desired_concentration']}")
    print(f"Volume to add: {item['volume_to_add']}")
    print(f"Notes: {item['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM experiment_drugs WHERE id = ?;", (ed_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Experiment-drug entry deleted.")
    else:
        print("Deletion failed.")

    return affected
