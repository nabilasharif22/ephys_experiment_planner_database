# db/cells_crud.py

from db.connection import get_connection
from db.mice_crud import get_mouse_by_id
from db.experiments_crud import get_experiment_by_id
from datetime import datetime


# ---------------------------------------------------------
# Helper: enrich cell with mouse + experiment metadata
# ---------------------------------------------------------
def enrich_cell(cell_row):
    """
    Takes a raw cell row and returns a dict with full metadata:
    project, experiment, mouse strain, sex, dob, age, etc.
    """
    cell = {
        "id": cell_row[0],
        "mouse_id": cell_row[1],
        "cell_number": cell_row[2],
        "recording_type": cell_row[3],
        "notes": cell_row[4],
    }

    # Fetch mouse metadata
    mouse = get_mouse_by_id(cell["mouse_id"])
    if mouse:
        cell["mouse"] = mouse

        # Fetch experiment metadata
        exp = get_experiment_by_id(mouse["experiment_id"])
        if exp:
            cell["experiment"] = exp

    return cell


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_cell(
    mouse_id,
    cell_number,
    recording_type=None,
    notes=None
):
    """
    Create a cell for a given mouse.
    Automatically links to experiment, project, person, etc.
    """
    mouse = get_mouse_by_id(mouse_id)
    if mouse is None:
        raise ValueError(f"Mouse with id {mouse_id} does not exist.")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cells (
            mouse_id,
            cell_number,
            recording_type,
            notes
        ) VALUES (?, ?, ?, ?);
    """, (
        mouse_id,
        cell_number,
        recording_type,
        notes
    ))

    conn.commit()
    cell_id = cur.lastrowid
    conn.close()
    return cell_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_cell_by_id(cell_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            mouse_id,
            cell_number,
            recording_type,
            notes
        FROM cells
        WHERE id = ?;
    """, (cell_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return enrich_cell(row)


# ---------------------------------------------------------
# READ (all cells for a mouse)
# ---------------------------------------------------------
def get_cells_for_mouse(mouse_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            mouse_id,
            cell_number,
            recording_type,
            notes
        FROM cells
        WHERE mouse_id = ?;
    """, (mouse_id,))

    rows = cur.fetchall()
    conn.close()

    return [enrich_cell(row) for row in rows]


# ---------------------------------------------------------
# READ (all cells for an experiment)
# ---------------------------------------------------------
def get_cells_for_experiment(experiment_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            cells.id,
            cells.mouse_id,
            cells.cell_number,
            cells.recording_type,
            cells.notes
        FROM cells
        JOIN mice ON cells.mouse_id = mice.id
        WHERE mice.experiment_id = ?;
    """, (experiment_id,))

    rows = cur.fetchall()
    conn.close()

    return [enrich_cell(row) for row in rows]


# ---------------------------------------------------------
# READ (all cells for a project)
# ---------------------------------------------------------
def get_cells_for_project(project_id):
    """
    Cells → Mice → Experiments → Projects
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            cells.id,
            cells.mouse_id,
            cells.cell_number,
            cells.recording_type,
            cells.notes
        FROM cells
        JOIN mice ON cells.mouse_id = mice.id
        JOIN experiments ON mice.experiment_id = experiments.id
        WHERE experiments.project_id = ?;
    """, (project_id,))

    rows = cur.fetchall()
    conn.close()

    return [enrich_cell(row) for row in rows]


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_cells_for_mouse(mouse_id):
    cells = get_cells_for_mouse(mouse_id)
    print(f"\nCells for mouse {mouse_id}:")
    for c in cells:
        print(f"{c['id']}: cell #{c['cell_number']} ({c['recording_type']})")
    return cells


def list_cells_for_experiment(experiment_id):
    cells = get_cells_for_experiment(experiment_id)
    print(f"\nCells for experiment {experiment_id}:")
    for c in cells:
        print(
            f"{c['id']}: mouse {c['mouse_id']} → cell #{c['cell_number']} "
            f"({c['recording_type']})"
        )
    return cells


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_cell_partial(cell_id, **fields):
    if not fields:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(cell_id)

    sql = f"UPDATE cells SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_cell_interactive(cell_id):
    cell = get_cell_by_id(cell_id)
    if cell is None:
        print("Cell not found.")
        return 0

    print("\nYou are about to delete this cell:")
    print(f"ID: {cell['id']}")
    print(f"Mouse ID: {cell['mouse_id']}")
    print(f"Cell number: {cell['cell_number']}")
    print(f"Recording type: {cell['recording_type']}")
    print(f"Notes: {cell['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cells WHERE id = ?;", (cell_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Cell deleted.")
    else:
        print("Deletion failed.")

    return affected




def get_all_cells():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            mouse_id,
            cell_number,
            recording_type,
            notes
        FROM cells;
    """)

    rows = cur.fetchall()
    conn.close()

    return [enrich_cell(row) for row in rows]


def list_cells():
    cells = get_all_cells()
    print("\nAll Cells:")
    for c in cells:
        print(
            f"{c['id']}: mouse {c['mouse_id']} → cell #{c['cell_number']} "
            f"({c['recording_type']})"
        )
    return cells
