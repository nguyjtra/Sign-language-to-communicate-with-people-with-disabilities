# Sign Language Recognition

This project uses a ResNet50 model to recognize American Sign Language (ASL) characters from a webcam feed.

## Prerequisites

Ensure you have Python installed (Python 3.9+ recommended).

Install the required dependencies:

```bash
python3 -m pip install -r setup.txt

```

## Dataset and Models

You can download the dataset and pre-trained models from the following Google Drive link:
[Download Models and Dataset](https://drive.google.com/drive/folders/1IYqvwjuZjqibtFlOR7VUm7OzBLQ-Lxz6?usp=sharing)

## Presentation

You can view the project presentation here:
[View Presentation](https://docs.google.com/presentation/d/19fm19EvjPBaC-GOkvzxcejNifA9LI9KXStbVtf67ico/edit?usp=sharing)

## Project Report

You can read the full project report here:
[View Report](https://docs.google.com/document/d/15-RLz2UakyQvDs9GF8MiAFJCB7N3VSllJfNzghdjnIg/edit?tab=t.0)

## Directory Structure

Ensure your project directory looks like this:

![Directory Structure](assets/directory_structure.png)

## How to Run

### 1. Train the Model (Optional)

If you haven't trained the model yet or want to retrain it:

```bash
python "Train Model.py"
```

This will train the model using the images in the `dataset` folder and save the model and class labels to the `models` folder.

### 2. Run the Application

To start the real-time sign language recognition app:

```bash
python run_app.py
```

### Application Instructions

- **Place hand in the green box**: Position your hand within the green rectangle on the screen.
- **Hold hand still for 0.5s**: The application requires the hand to be stable to register a character.
- **Press 'R'**: Clear the current text.
- **Press 'Q'**: Quit the application.

<pre><div><div class="language-bash relative overflow-hidden rounded-b border-x border-b border-gray-500/25 bg-ide-editor-background" aria-label="highlighted-code-language-bash"><pre><div class="overflow-x-auto bg-ide-editor-background p-2"><div class="rendered-markdown"><div data-code="id#12"><span><div class="monaco-tokenized-source"><span class="mtk16">python3</span><span class="mtk1"></span><span class="mtk6">-m</span><span class="mtk1"></span><span class="mtk12">pip</span><span class="mtk1"></span><span class="mtk12">install</span><span class="mtk1"></span><span class="mtk6">-r</span><span class="mtk1"></span><span class="mtk12">setup.txt</span></div></span></div></div></div></pre></div></div></pre>
# Sign-language-to-communicate-with-people-with-disabilities
