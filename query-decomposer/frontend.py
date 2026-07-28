import os

import graphviz
import streamlit as st
from main import run_pipeline, generate
from sql_generator import orient_tree, compute_bridge_vars

ASSETS = os.path.join(os.path.dirname(__file__), "assets")

st.set_page_config(layout="wide")

st.logo(image=os.path.join(ASSETS, "Universität_Zürich_logo.svg"), size="large", link="https://www.ifi.uzh.ch")

with st.container(horizontal=True, vertical_alignment="center"):
    st.title("Query Decomposer", width="content", anchor=False)
    with st.popover(":material/info:", type="tertiary"):
        st.markdown(
            """
**Supported**
- `SELECT *` (full join) or `SELECT COUNT(*)`
- Inner equi-joins: `JOIN ... ON a = b`, `JOIN ... USING (col)`
- Table/column aliases and self-joins
- Single-relation `WHERE` filters, combined with `AND`
- A `CREATE [MATERIALIZED] VIEW ... AS` wrapper and Feldera table annotations are accepted and ignored

**Not supported**
- Other aggregates or column projections
- Non-equi and outer joins
- `WHERE` conditions spanning multiple relations
- Subqueries

Validate your SQL in a database engine first. See the [README](PLACEHOLDER_README_URL) for details.
"""
        )


# --- input area ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Table Definitions**")
    schema_sql = st.text_area(
        "Table Definitions",
        label_visibility="collapsed",
        placeholder=(
            "CREATE TABLE EDGES (\n    src bigint,\n    tgt bigint\n);"
            ),
        height=400,
    )

with col2:
    st.markdown("**Query**")
    query_sql = st.text_area(
        "Query",
        label_visibility="collapsed",
        placeholder=(
            "SELECT * \nFROM EDGES AS R1(A, B) \nJOIN EDGES AS R2(B, C) ON R1.B = R2.B \nJOIN EDGES AS R3(C, D) ON R2.C = R3.C \nJOIN EDGES AS R4(B, D) ON R4.D = R3.D AND R4.B = R2.B AND (R4.B = R1.B) \nJOIN EDGES AS R5(A, D) ON R5.A = R1.A AND R5.D = R4.D AND (R5.D =R3.D);"
        ),
        height=400,
    )

with st.container(horizontal_alignment="center"):
    decompose = st.button("Decompose", width="stretch", type="primary")
if decompose:
    if not (schema_sql.strip() and query_sql.strip()):
        st.session_state["pipeline"] = None
        st.session_state["error"] = "Fill in both the table definitions and the query."
    else:
        try:
            tables, edges, var_to_col, bags, tree_edges, treewidth, fhw, predicates, alias_to_table, agg_type, special_col = run_pipeline(schema_sql, query_sql)
            st.session_state["pipeline"] = (tables, edges, var_to_col, bags, tree_edges, treewidth, fhw, predicates, alias_to_table, agg_type, special_col)
            st.session_state["error"] = None
        except Exception as e:
            st.session_state["error"] = str(e)
            st.session_state["pipeline"] = None

if st.session_state.get("error"):
    st.error(st.session_state["error"])

pipeline = st.session_state.get("pipeline")
if pipeline:
    tables, edges, var_to_col, bags, tree_edges, treewidth, fhw, predicates, alias_to_table, agg_type, special_col = pipeline


    # --- output area: decomposed query on left, FHW + tree on right ---
    out_col1, out_col2 = st.columns(2)

    with out_col1:
        st.markdown("**Tree Decomposition**")

        # root selectbox
        bag_ids = sorted(bags.keys())
        root = st.selectbox(
            "Root bag",
            options=bag_ids,
            index=0,
            format_func=lambda b: f"Bag {b}  {sorted(bags[b])}",
            label_visibility="collapsed"
        )
        st.caption(f"Fractional Hypertree Width: {fhw}")

        # orient the tree from the chosen root
        children, parent = orient_tree(bags, tree_edges, root)

        # bridge_vars[child] = variables shared between child and its parent
        bridge_vars = compute_bridge_vars(bags, parent, root)

        # graphviz directed graph
        dot = graphviz.Digraph()
        dot.attr(rankdir="TB", ranksep="1.0")     # top to bottom
        dot.edge_attr.update(arrowhead="none")    # no arrows

        for bag_id in bags:
            # wrap variables into rows of 4 so nodes are taller
            var_list = sorted(bags[bag_id])
            rows = []
            for i in range(0, len(var_list), 4):
                rows.append(", ".join(var_list[i:i + 4]))
            label = f"Bag {bag_id}\n{{{chr(10).join(rows)}}}"

            if bag_id == root:
                dot.node(str(bag_id), label, style="filled", fillcolor="#BDC9E8")
            else:
                dot.node(str(bag_id), label)

        for bag_id in bags:
            for child in children[bag_id]:
                edge_label = ", ".join(sorted(bridge_vars[child]))
                dot.edge(str(bag_id), str(child), label=edge_label)

        st.graphviz_chart(dot, width="content")

    with out_col2:
        st.markdown("**Decomposed Query**")
        method = st.radio("Method", ["IVM+", "IVM+* (Strict)"], horizontal=True, label_visibility="collapsed")
        strict_mode = (method == "IVM+* (Strict)")
        try:
            views = generate(tables, edges, var_to_col, bags, tree_edges, predicates, alias_to_table, root, strict_mode, agg_type, special_col)
            st.code("\n\n".join(views), language="sql")
        except Exception as e:
            st.error(str(e))

# --- footer ---
st.divider()
f1, f2 = st.columns(2, vertical_alignment="center")
with f1:
    with st.container(horizontal=True, vertical_alignment="center", gap="medium"):
        st.image(os.path.join(ASSETS, "DaST_logo.svg"), width=150, link="https://www.ifi.uzh.ch/dast")
        st.markdown("[Bachelor Thesis 2026](https://github.com/ermin-mumic/UZH-Bachelor-Thesis-IVM)")
with f2:
    st.markdown("[Ermin Mumic](https://github.com/ermin-mumic)", text_alignment="right")
