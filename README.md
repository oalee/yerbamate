<h1 style="color:green"><span style="color:green">Maté 🧉</span> your friendly AI project and experiment manager</h1>

Maté is a python project, package and experiment manager. Whether you are a
seasoned deep learning researcher or just starting out, Maté provides you with
the tools to easily add source code and dependencies of models, trainers, and
data loaders to your projects. With Maté, you can also evaluate, train, and keep
track of your experiments with ease 🚀

## Features 🎉

- Seamless integration with popular deep learning libraries such as PyTorch,
  TensorFlow, and JAX.
- Easy to use interface to add source code of models, trainers, and data loaders
  to your projects.
- Support for full customizability and reproducibility of results through the
  inclusion of source code dependencies in your project.
- Modular project structure that enforces a clean and organized codebase.
- Convenient environment management through the Maté Environment API.
- Support for pip and conda for dependency management.
- Works with Colab.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](https://oalee.github.io/yerbamate/#/?id=project-structure-%f0%9f%93%81)
- [Example Projects](#example-projects)
- [Documentation](https://oalee.github.io/yerbamate/)
- [Contributing](#contributing)
- [FAQ](#faq)

## Installation 🔌

```bash
pip install yerbamate
```

## Quick Start ⚡

### **Initialize a project**

```bash
mate init deepnet
```

This will generate the following structure:

```bash
/
|-- models/
|   |-- __init__.py
|-- experiments/
|   |-- __init__.py
|-- trainers/
|   |-- __init__.py
|-- data/
|   |-- __init__.py
```

### **Install an experiment**

To install an experiment, you can use `mate install` to install a module from a
github repository:

```bash
mate install oalee/big_transfer/experiments/bit -yo pip
```

### **Install a module**
You can install independant modules such as models, trainers, and data loaders from github projects that follow the [Maté modular project structure](https://oalee.github.io/yerbamate#project-structure).

```bash
mate install oalee/lightweight-gan/lgan/trainers/lgan 
mate install oalee/big_transfer/models/bit -yo pip
mate install oalee/deep-vision/deepnet/models/vit_pytorch -yo pip
mate install oalee/deep-vision/deepnet/trainers/classification -yo pip
```

### **Setting up environment**

Take a look at
[Environment API](https://oalee.github.io/yerbamate#maté-environment-api) and
set up your environment before running your experiments.

### **Train a model**

To train a model, you can use the `mate train` command. This command will train
the model with the specified experiment. For example, to train the an experiment
called `learn` in the `bit` module, you can use the following command:

```bash
mate train bit learn
# or alternatively use python
python -m train deepnet.experiments.bit.learn
```

## Project Structure 📁

Deep learning projects can be organized into the following structure with modularity and seperation of concerns in
mind. This offers a clean and organized codebase that is easy to maintain and is
sharable out-of-the-box.

```bash
/
|-- models/
|   |-- __init__.py
|-- experiments/
|   |-- __init__.py
|-- trainers/
|   |-- __init__.py
|-- data/
|   |-- __init__.py
```

### Modularity

Modularity is a software design principle that focuses on creating
self-contained, reusable and interchangeable components. In the context of a
deep learning project, modularity means creating three independent standalone
modules for models, trainers and data. This allows for a more organized,
maintainable and sharable project structure. The forth module, experiments, is
not independent, but rather combines the three modules together to create a
complete experiment.

### Sample Project Structure

This structure highlights modularity and seperation of concerns. The `models`,
`data` and `trainers` modules are independent and can be used in any project.
The `experiments` module is not independent, but rather combines the three
modules together to create a complete experiment.


```bash
.
├── mate.json
└── deepnet
    ├── data
    │   ├── bit
    │   │   ├── fewshot.py
    │   │   ├── __init__.py
    │   │   ├── minibatch_fewshot.py
    │   │   ├── requirements.txt
    │   │   └── transforms.py
    │   └── __init__.py
    ├── experiments
    │   ├── bit
    │   │   ├── aug.py
    │   │   ├── dependencies.json
    │   │   ├── __init__.py
    │   │   ├── learn.py
    │   │   └── requirements.txt
    │   └── __init__.py
    ├── __init__.py
    ├── models
    │   ├── bit_torch
    │   │   ├── downloader
    │   │   │   ├── downloader.py
    │   │   │   ├── __init__.py
    │   │   │   ├── requirements.txt
    │   │   │   └── utils.py
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   └── requirements.txt
    │   └── __init__.py
    └── trainers
        ├── bit_torch
        │   ├── __init__.py
        │   ├── lbtoolbox.py
        │   ├── logger.py
        │   ├── lr_schduler.py
        │   ├── requirements.txt
        │   └── trainer.py
        └── __init__.py
```

## Example Projects 📚

Please check out the [transfer learning](https://github.com/oalee/big-transfer),
[vision models](https://github.com/oalee/deep-vision), and
[lightweight gan](https://github.com/oalee/lightweight-gan).

## Documentation 📚

Please check out the [documentation](https://oalee.github.io/yerbamate).

## Guides 📖

For more information on modularity, please check out this [guide]().

## Contributing 🤝

We welcome contributions from the community! Please check out our
[contributing](https://github.com/oalee/yerbamate/blob/main/CONTRIBUTING.md)
guide for more information on how to get started.

## Contact 🤝

For questions please contact:

yerba.mate.dl(at)proton.me
