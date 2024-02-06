import sys
import json
import spacy
import argparse
from extend import spacy_component
nlp = spacy.load("en_core_web_sm")

parser = argparse.ArgumentParser(description='run extend')
parser.add_argument('-dataset_file', type=str, default="data/blink_test.json")
parser.add_argument('-result_file', type=str, default="data/yago_old.result")
parser.add_argument('-candidate_file', type=str, default="data/yago_old.candidate")
parser.add_argument('-checkpoint_path', type=str, default="experiments/extend-longformer-large/2021-10-22/09-11-39/checkpoints/best.ckpt")
parser.add_argument('-device', type=int, default=0)
parser.add_argument('-tokens_per_batch', type=int, default=4000)
parser.add_argument('-max_input_length', type=int, default=3000)


def load_blink(file_name):
    return  [json.loads(line) for line in open(file_name, encoding='utf8')]

def run(
        dataset_file,
        result_file,
        candidate_file,
        checkpoint_path,
        device,
        tokens_per_batch,
        max_input_length,
):
    extend_config = dict(
        checkpoint_path=checkpoint_path,
        mentions_inventory_path=candidate_file,
        device=device,
        tokens_per_batch=tokens_per_batch,
    )

    nlp.add_pipe("extend", after="ner", config=extend_config)

    wf = open(result_file, 'w', encoding='utf8')
    samples = load_blink(dataset_file)
    for index, sample in enumerate(samples):
        if index % 1000 ==0:print('processing {a} lines'.format(a=index))
        id = sample['id']
        input_sentence = sample['input'][:max_input_length]
        mention = sample['meta']['mention']
        wp_title = sample['output'][0]['provenance'][0]['title']
        print(id, mention, wp_title)
        doc = nlp(input_sentence)

        disambiguated_entities = dict([(ent.text, ent._.disambiguated_entity) for ent in doc.ents])
        if mention not in disambiguated_entities:continue
        if disambiguated_entities[mention] is None: continue
        predicted = disambiguated_entities[mention]
        wf.write(id+'\t'+ mention + '\t' + predicted+ '\t'+wp_title+'\n')
        wf.flush()


if __name__ == '__main__':
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    run(
        args.dataset_file,
        args.result_file,
        args.candidate_file,
        args.checkpoint_path,
        args.device,
        args.tokens_per_batch,
        args.max_input_length,
    )
