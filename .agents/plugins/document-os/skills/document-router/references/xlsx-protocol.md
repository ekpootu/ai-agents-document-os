# XLSX Processing Protocol

Microsoft Excel (`.xlsx`) workbooks contain calculation graphs, formula trees, styles, number formats, pivot tables, and charts.

## 1. The Cardinal Rule: Preserve Formulas
When reading an Excel file:
- `openpyxl.load_workbook(filename, data_only=False)` preserves the underlying formula strings (e.g. `=SUM(B2:B10)`).
- `openpyxl.load_workbook(filename, data_only=True)` loads the cached evaluated values.
- **Editing Rule**: When modifying cell values, NEVER overwrite formula cells with static values unless the user explicitly commands a "paste values" operation.

## 2. Multi-Sheet & Tabular Awareness
- Workbooks frequently have multiple sheets (e.g. `Summary`, `Raw Data`, `Assumptions`).
- Always list all sheet names via `inspect_doc.py` before querying.
- Use `pandas` for bulk data manipulation on tabular sheets (`pd.read_excel(..., sheet_name=...)`).
- Use `openpyxl` when style, formula, or cell-specific formatting must be preserved.
- Use `xlsxwriter` when generating new, heavily styled workbooks with conditional formatting and native Excel charts from scratch.

## 3. QA Error Checking
Every edited or generated `.xlsx` file must be scanned for formula error tokens:
- `#REF!` (Invalid cell reference)
- `#VALUE!` (Wrong data type in calculation)
- `#DIV/0!` (Division by zero)
- `#NAME?` (Unrecognized function name)
- `#N/A` (Missing lookup value)

Run `qa_doc.py <file.xlsx>` to automatically assert zero formula errors.
