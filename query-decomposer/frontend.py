import graphviz
import streamlit as st
from main import run_pipeline, generate
from sql_generator import orient_tree, compute_bridge_vars

st.set_page_config(layout="wide")

st.title("Query Decomposer")

# --- input area ---
col1, col2 = st.columns(2)

with col1:
    schema_sql = st.text_area(
        "Table Definitions",
        placeholder="CREATE TABLE R (A INT, B INT);\nCREATE TABLE S (B INT, C INT);",
        height=400,
    )

with col2:
    query_sql = st.text_area(
        "Query",
        placeholder="SELECT * FROM R JOIN S USING (B)",
        height=400,
    )

both_filled = schema_sql.strip() != "" and query_sql.strip() != ""

method = st.radio("Method", ["IVM+", "IVM+* (Strict)"], horizontal=True)
strict_mode = (method == "IVM+* (Strict)")
if st.button("Decompose", disabled=not both_filled):
    try:
        tables, edges, var_to_col, bags, tree_edges, treewidth, predicates, alias_to_table = run_pipeline(schema_sql, query_sql)
        st.session_state["pipeline"] = (tables, edges, var_to_col, bags, tree_edges, treewidth, predicates, alias_to_table)
        st.session_state["error"] = None
    except Exception as e:
        st.session_state["error"] = str(e)
        st.session_state["pipeline"] = None

if st.session_state.get("error"):
    st.error(st.session_state["error"])

pipeline = st.session_state.get("pipeline")
if pipeline:
    tables, edges, var_to_col, bags, tree_edges, treewidth, predicates, alias_to_table = pipeline


    # --- output area: SQL on left, tree on right ---
    st.markdown(f"**Treewidth:** {treewidth}")

    out_col1, out_col2 = st.columns(2)

    with out_col2:
        # root selectbox 
        bag_ids = sorted(bags.keys())
        root = st.selectbox(
            "Root bag",
            options=bag_ids,
            index=0,
            format_func=lambda b: f"Bag {b}  {sorted(bags[b])}",
        )

        # orient the tree from the chosen root
        children, parent = orient_tree(bags, tree_edges, root)

        # bridge_vars[child] = variables shared between child and its parent
        bridge_vars = compute_bridge_vars(bags, parent, root)

        # graphviz directed graph
        dot = graphviz.Digraph()
        dot.attr(rankdir="TB", ranksep="0.8")     # top to bottom, more space between levels
        dot.edge_attr.update(arrowhead="none")    # no arrows

        for bag_id in bags:
            # wrap variables into rows of 4 so nodes are taller 
            var_list = sorted(bags[bag_id])
            rows = []
            for i in range(0, len(var_list), 4):
                rows.append(", ".join(var_list[i:i + 4]))
            label = f"Bag {bag_id}\n{{{chr(10).join(rows)}}}"

            if bag_id == root:
                dot.node(str(bag_id), label, style="filled", fillcolor="lightblue")
            else:
                dot.node(str(bag_id), label)

        for bag_id in bags:
            for child in children[bag_id]:
                edge_label = ", ".join(sorted(bridge_vars[child]))
                dot.edge(str(bag_id), str(child), label=edge_label)

        st.graphviz_chart(dot, width="content")

    with out_col1:
        try:
            views = generate(tables, edges, var_to_col, bags, tree_edges, predicates, alias_to_table, root, strict_mode)
            st.markdown("**Generated SQL:**")
            st.code("\n\n".join(views), language="sql")
        except Exception as e:
            st.error(str(e))
