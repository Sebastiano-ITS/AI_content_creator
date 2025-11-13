import json, os

with open(os.path.join(os.path.dirname(__file__), "templates.json")) as f:
    TEMPLATES = json.load(f)

def few_shot_prompt(template_key, params, examples):
    meta = TEMPLATES[template_key]
    header = (
        f"Template: {meta['name']}\n"
        f"Struttura: {meta['template']}\n"
        f"Istruzioni: {meta.get('instructions', '')}"
    )
    example_texts = []
    for i, ex in enumerate(examples, 1):
        ex_input = ", ".join(f"{k}={v}" for k, v in ex["input"].items())
        example_texts.append(f"ESEMPIO {i}\nINPUT: {ex_input}\nOUTPUT: {ex['output']}")
    return "\n\n".join([
        header,
        "---",
        *example_texts,
        "---",
        f"ORA GENERA rispettando struttura e istruzioni. Parametri: {params}"
    ])

def cot_prompt(template_key, params):
    meta = TEMPLATES[template_key]
    return (
        f"Template: {meta['name']}\nStruttura: {meta['template']}\n"
        f"Istruzioni: {meta.get('instructions', '')}\n"
        f"1) Pianifica passo-passo (reasoning) come applicare struttura e istruzioni.\n"
        f"2) Scrivi il contenuto finale adatto a {params}."
    )

def role_prompt(template_key, params, role_description):
    meta = TEMPLATES[template_key]
    return (
        f"Ruolo assegnato: {role_description}\n"
        f"Template: {meta['name']}\nStruttura: {meta['template']}\n"
        f"Istruzioni: {meta.get('instructions', '')}\n"
        f"Applica ruolo, struttura e istruzioni ai parametri: {params}"
    )
