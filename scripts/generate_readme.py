import os
import yaml
import re
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

START_MARKER = "<!-- AUTO-GENERATED-CONTENT:START (Do not remove this line) -->"
END_MARKER = "<!-- AUTO-GENERATED-CONTENT:END (Do not remove this line) -->"

OPEN_EMOJI = "🌐"
CLOSED_EMOJI = "🔐"
UK_GOV_EMOJI = "🏛️"
EXTERNAL_EMOJI = "🏢"

def generate_toc(topics):
    toc = "## Table of Contents\n\n"
    for topic in sorted(topics):
        toc += f"- [{topic}](#{topic.lower().replace(' ', '-')})\n"
    return toc

def generate_dataset_entry(dataset, file_path):
    return (
        f"""- __[{dataset['name']}]({dataset['source_url']})__ [[Metadata]]({file_path}):
        {OPEN_EMOJI if dataset.get("open_data") is True else CLOSED_EMOJI} {UK_GOV_EMOJI if dataset.get("made_by_ukgov") is True else EXTERNAL_EMOJI}:
        {dataset['description']}
        \n  - _Subtopics_: {', '.join([f'`{tag}`' for tag in dataset['subtopics']])}
        """
    )

def main():
    parser = argparse.ArgumentParser(description="Generate README for UK Government Datasets")
    parser.add_argument("--output", default="README.md", help="Output file name")
    args = parser.parse_args()

    topics = {}
    
    # Read all datasets
    for root, dirs, files in os.walk("datasets/"):
        if root in ["",".","datasets/"] or ".github" in root:
            continue

        topic = os.path.basename(root)
        topics[topic] = []

        logging.info(f"Reading topic: {topic}")

        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        logging.info(f"Processing {file_path}")
                        dataset = yaml.safe_load(f)
                    topics[topic].append((dataset, file_path))
                except yaml.YAMLError as e:
                    logging.error(f"Error parsing YAML file {file_path}: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error processing {file_path}: {e}")

    try:
        with open("README.md", "r") as readme:
            content = readme.read()
    except FileNotFoundError:
        logging.warning("README.md not found. Creating a new one.")
        content = f"# Awesome UK Government Datasets\n\n{START_MARKER}\n{END_MARKER}"
    
    # Generate new content for README
    new_content = generate_toc(topics) + "\n"

    # Add key for emojis 
    new_content += (
        "__Key__:\n\n"
        f"- {OPEN_EMOJI} Open Data\n"
        f"- {CLOSED_EMOJI} Closed Data\n"
        f"- {UK_GOV_EMOJI} UK Government Dataset\n"
        f"- {EXTERNAL_EMOJI} External Dataset\n\n"
    )

    # Add datasets to README
    for topic, datasets in sorted(topics.items()):
        new_content += f"\n## {topic}\n\n"
        for dataset, file_path in sorted(datasets, key=lambda x: x[0]['name']):
            new_content += generate_dataset_entry(dataset, file_path)
            new_content += "\n"

    # Update README with new content
    updated_content = re.sub(
        f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        f"{START_MARKER}\n{new_content}\n{END_MARKER}",
        content,
        flags=re.DOTALL
    )
    
    # Write updated content to README
    try:
        with open(args.output, "w") as readme:
            readme.write(updated_content)
        logging.info(f"README generated: {args.output}")
    except IOError as e:
        logging.error(f"Error writing to {args.output}: {e}")

if __name__ == "__main__":
    main()