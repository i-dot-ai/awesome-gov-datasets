import os
import yaml
import re
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

START_MARKER = "<!-- AUTO-GENERATED-CONTENT:START (Do not remove this line) -->"
END_MARKER = "<!-- AUTO-GENERATED-CONTENT:END (Do not remove this line) -->"

def generate_toc(topics):
    toc = "## Table of Contents\n\n"
    for topic in sorted(topics):
        toc += f"- [{topic}](#{topic.lower().replace(' ', '-')})\n"
    return toc

def generate_dataset_entry(dataset, file_path):
    return (
        f"- [{dataset['name']}]({dataset['source_url']}) [[Metadata]]({file_path}):\n"
        f"{dataset['description']}\n"
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
    for topic, datasets in sorted(topics.items()):
        new_content += f"\n## {topic}\n\n"
        for dataset, file_path in sorted(datasets, key=lambda x: x[0]['name']):
            new_content += generate_dataset_entry(dataset, file_path)

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