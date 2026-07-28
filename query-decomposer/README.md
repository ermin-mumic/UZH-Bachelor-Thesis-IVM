# Query Decomposer

*← Back to the [repository overview](../README.md).*

Turn a SQL join query into an incrementally maintainable **IVM⁺** pipeline of SQL views, derived from a **tree decomposition** of the query. Built for a Bachelor's thesis on evaluating IVM⁺ over [Feldera](https://www.feldera.com/); the [thesis](../thesis) covers the theory.

<!-- TODO: **Live demo:** https://<your-app>.streamlit.app -->

![The query decomposer's web interface](../thesis/figures/ch4_web_ui.png)

---

## What it does

Given a set of `CREATE TABLE` definitions and a single join query, the tool

1. parses the query and builds its **hypergraph**,
2. computes a **tree decomposition** of that hypergraph and its **fractional hypertree width (FHW)**,
3. generates the corresponding **IVM⁺ SQL views** — a `Q'` and a `P'` view per bag, plus a final `RESULT` view — that maintain the query result incrementally, and
4. renders the decomposition tree, with a selectable root and a toggle between the two variants.

**Example** — the "diamond" self-join used as the running example in the thesis (the app's default input), five occurrences of an edge relation:

```sql
-- Table definitions
CREATE TABLE EDGES (
    src bigint,
    tgt bigint
);

-- Query
SELECT *
FROM EDGES AS R1(A, B)
JOIN EDGES AS R2(B, C) ON R1.B = R2.B
JOIN EDGES AS R3(C, D) ON R2.C = R3.C
JOIN EDGES AS R4(B, D) ON R4.D = R3.D AND R4.B = R2.B AND (R4.B = R1.B)
JOIN EDGES AS R5(A, D) ON R5.A = R1.A AND R5.D = R4.D AND (R5.D = R3.D);
```

---

## How it works

<!-- TODO: export the component diagram (draw.io) to thesis/figures/ch4_query_decomposer.png -->
![Pipeline stages](../thesis/figures/ch4_query_decomposer.png)

`main.py` runs four stages over the input.

### 1. Parser — `parser.py`

Uses [`sqlglot`](https://github.com/tobymao/sqlglot) to parse the schema and query into an abstract syntax tree. Walking it clause by clause, it collects the relations (resolving table and column aliases, and treating each occurrence of a self-joined relation as an independent relation), the equi-join conditions (`JOIN … ON` and `JOIN … USING`), and the single-relation `WHERE` filters, and detects whether the query is `SELECT *` or `SELECT COUNT(*)`. The full schema is needed because the tool returns *all* variables, so it must know every column of every relation, even those the query never mentions.

### 2. Hypergraph — `hypergraph.py`

Columns equated by a join are merged into a single **variable** with a **union-find** structure, so an equi-join between differently named columns still yields one hypergraph vertex. Each relation becomes a **hyperedge** over its variables. The stage also records, in both directions, which column of each relation a variable stands for — the mapping the generator needs later.

### 3. Decomposition — `decomposition.py`, `fhw.py`

Computing a minimum-FHW decomposition is NP-hard, so the tool uses the **Minimum Fill-in** heuristic from [`networkx`](https://networkx.org/), which runs on the query's **primal graph** (each hyperedge turned into a clique). Minimum Fill-in optimises *treewidth*, but IVM⁺ cost is governed by *FHW*, and two decompositions of equal treewidth can differ in FHW. The tool therefore runs the heuristic on several vertex-insertion orderings — a sorted baseline plus a fixed set of seeded shuffles, so results are deterministic — whose different tie-breaks yield different decompositions, computes each one's FHW, and keeps the smallest. FHW is the maximum over the bags of the **fractional edge cover number**, each solved as a small linear program with `scipy.optimize.linprog` (`fhw.py`). Redundant bags (contained in a neighbour) are removed.

### 4. SQL generator — `sql_generator.py`

The tree is oriented from a chosen **root**, giving each bag a parent and children, and each non-root bag's **bridge variables** (those it shares with its parent) are computed. Bottom-up, each bag gets a `Q'` view — its atoms as subqueries (each relation's physical columns aliased to the bag's variables, single-relation filters appended as `WHERE`), joined with `JOIN … USING`, then joined with the children's `P'` views on the bridge variables — and a `P'` view projecting onto the bridge variables. A final `RESULT` view reconstructs the full join (`SELECT *`) or returns the count (`SELECT COUNT(*)`, via the counting semiring). The two variants differ only in the `Q'` view: **IVM⁺** adds partially overlapping atoms as `SELECT DISTINCT` semijoins, while **IVM⁺\* (strict)** drops them.

The **frontend** (`frontend.py`) is a [Streamlit](https://streamlit.io) app wrapping this pipeline: the schema and query inputs, the generated views, the FHW, and an interactive tree with a selectable root and an IVM⁺/variant toggle.

---

## Supported

- `SELECT *` (full conjunctive query) and `SELECT COUNT(*)`
- Inner equi-joins via `JOIN … USING (col)` and `JOIN … ON left.col = right.col`, multi-way
- Table and column aliases, and **self-joins**, including column-rename aliases (`EDGES AS R1(A, B)`)
- Single-relation `WHERE` filters (e.g. `AIRPORT.CITY = 'Zurich'`, `L.QUANTITY > 10`), combined with `AND`
- Both variants: **IVM⁺** (semijoin projection) and **IVM⁺\*** (strict)
- Feldera table annotations (`WITH (...)`, connectors, `'materialized'`) are accepted and ignored, so a pipeline schema can be pasted in unchanged
- A `CREATE [MATERIALIZED] VIEW ... AS` wrapper around the query is accepted and ignored, so a Feldera view definition can be pasted in directly

## Limitations

- `COUNT(*)` is the only aggregate; `MIN` / `MAX` / `SUM` / `COUNT(col)` and column projections are not supported
- Only equi-joins; inequality and outer joins are not
- Each `WHERE` condition must reference a single relation (no cross-relation comparisons or disjunctions)
- No subqueries
- Assumes **set-valued** input relations, as IVM⁺ does; with duplicate input rows, dense cyclic queries can over-count

The decomposer performs only the checks its translation needs and is not a full SQL validator, so validate a query in a database engine (for instance Feldera) before handing it in.

---

## Run locally

```bash
cd query-decomposer
pip install -r requirements.txt
streamlit run frontend.py
```

The app opens in your browser. It is pure Python — the tree is rendered client-side, so no Graphviz binary is required.

To run the pipeline without the UI:

```bash
python main.py    # prints the generated views for a built-in example
```

---

## Project layout

| File | Role |
|---|---|
| `frontend.py` | Streamlit UI |
| `main.py` | orchestrates the pipeline (`run_pipeline`, `generate`) |
| `parser.py` | SQL parsing (schema, joins, predicates, aggregation type) |
| `hypergraph.py` | builds the query hypergraph (variables via union-find, hyperedges) |
| `decomposition.py` | tree decomposition (Minimum Fill-in + FHW-selection over sampled orderings) |
| `fhw.py` | fractional hypertree width via per-bag linear program |
| `sql_generator.py` | emits the IVM⁺ `Q'` / `P'` views and the `RESULT` view |
| `requirements.txt` | Python dependencies |

---

## License

Licensed under the MIT License — see [LICENSE](../LICENSE).

---

Part of a Bachelor's thesis at the University of Zurich ([DaST group](https://www.ifi.uzh.ch/dast)) on evaluating IVM⁺ via tree decomposition with [Feldera](https://www.feldera.com/).
