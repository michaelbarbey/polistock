# table formatting design

def calculate_column_widths(rows):
    # error handling for empty rows
    if not rows:
        return []

    num_cols = len(rows[0])
    # initializing widths to zero
    widths = [0] * num_cols

    # for each row, for each column, update max width
    for row in rows:
        for col_index in range(num_cols):
            cell = row[col_index]
            length = len(cell)
            if length > widths[col_index]:
                widths[col_index] = length
    return widths


def format_row_with_widths(row, widths):
    formatted = ""
    num_cols = len(row)

    # building lines
    for col_index in range(num_cols):
        cell = row[col_index]
        pad_amount = widths[col_index] - len(cell)
        # adding the cell, then spaces, then column separator
        formatted += cell + (" " * pad_amount) + "  |  "

    # removing the trailing separator
    return formatted.rstrip("  |  ")