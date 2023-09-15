import gradio as gr
import polars as pl


# exit()




def filter_on_ontology(ontology, data, cur_id):
    data = pl.read_csv("definitions.tsv", separator='\t')
    data = data.filter(pl.col("ontology") == ontology)
    cur_id = data.select(pl.col("internal_id")).min().get_column("internal_id").to_list()[0]
    next_row = data.filter(pl.col("internal_id") == cur_id).select(["label", "definition", "is_a", "relationships"])
    label = next_row.get_column("label").to_list()[0]
    definition = next_row.get_column("definition").to_list()[0]
    parent = next_row.get_column("is_a").to_list()[0]
    relationship = next_row.get_column("relationships").to_list()[0]

    return data, cur_id, label, definition, parent, relationship

def get_next(data, cur_id, acc, conf, struc, results):
    ## Naturally, IDs aren't sequential, so we need to find the next available one
    available_ids =set(data.get_column("internal_id").to_list())
    done_ids = set(results["internal_id"])
    available_ids = available_ids - done_ids
    cur_id = min(available_ids)
    next_row = data.filter(pl.col("internal_id") == cur_id).select(["label", "definition", "is_a", "relationships"])
    label = next_row.get_column("label").to_list()[0]
    definition = next_row.get_column("definition").to_list()[0]
    parent = next_row.get_column("is_a").to_list()[0]
    relationship = next_row.get_column("relationships").to_list()[0]

    results["internal_id"].append(cur_id)
    results["accuracy"].append(acc)
    results["confidence"].append(conf)
    results["structure_content"].append(struc)

    return cur_id, label, definition, parent, relationship, results


with gr.Blocks() as iface:
    cur_id = gr.State(value=1)
    data = gr.State(value=pl.read_csv("definitions.tsv", separator='\t'))
    results = gr.State(value={"internal_id": [], "accuracy": [], "confidence": [], "structure_content": []})

    ## Display
    with gr.Row():
        label = gr.Textbox(lines=1, label="label",interactive=False)
        definition = gr.Textbox(lines=3, label="Definition",interactive=False)

    with gr.Row():
        parent = gr.Textbox(lines=1, label="Parent",interactive=False)
        relationship = gr.Textbox(lines=1, label="Relationships",interactive=False)

    ## User input
    with gr.Row():
        acc = gr.Radio([1,2,3,4,5], label="Accuracy")
        conf = gr.Radio([1,2,3,4,5], label="Confidence")
        struc = gr.Radio([1,2,3,4,5], label="Structure/Content")
    with gr.Row():
        note = gr.Textbox(lines=3, label="Notes")
        sub = gr.Button(label="Submit", value="Submit")
        sub.click(get_next, inputs=[data, cur_id, acc, conf, struc, results], outputs=[cur_id, label, definition, parent, relationship, results])
    with gr.Row():
        ontology_select = gr.Dropdown(data.value.get_column("ontology").unique().to_list(), label="Ontology")
        ontology_select.change(filter_on_ontology, inputs=[ontology_select, data, cur_id], outputs=[data, cur_id, label, definition, parent, relationship])
    with gr.Row():
        out_name = gr.Textbox(lines=1, label="Output Name")
        write = gr.Button(label="Write", value="Write Output")
        write.click(lambda r, n: pl.DataFrame(r).write_csv(n), inputs=[results, out_name])
 

iface.launch()
