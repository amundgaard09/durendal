# AmundWorks Documentation & Wiki

This repository contains the central documentation and wiki for all projects under the AmundWorks organization. It provides an overview of the ecosystem, along with usage guides, project breakdowns, and development information for each component.

Whether you're using the tools, contributing to development, or exploring the system, this documentation serves as the main entry point to AmundWorks.

## Table of Contents

- [AmundWorks Documentation & Wiki](#amundworks-documentation--wiki)
  - [Table of Contents](#table-of-contents)
  - [AmundWorks Overview](#amundworks-overview)
  - [Quick Start Guide](#quick-start-guide)
  - [Project Documentation](#project-documentation)
    - [AWPC - AmundWorks Python Collective](#awpc---amundworks-python-collective)
    - [UniForge CLI](#uniforge-cli)
    - [XO Neural Net Series](#xo-neural-net-series)
    - [Vulcan Personal Productivity Platform](#vulcan-personal-productivity-platform)
  - [Contributing to AmundWorks](#contributing-to-amundworks)
  - [License and Usage](#license-and-usage)

## AmundWorks Overview & Status

AmundWorks is a independent multi-displine engineering conglomerate focused on creating innovative solutions at the intersection of technology and design. The organization focuses on building open-source resources, tools, and platforms that empower individuals and communities to create, learn, and innovate. AmundWorks is committed to fostering a collaborative environment where creativity and technology can thrive together.

[![AmundWorks Status](https://img.shields.io/badge/Status-Active%20Development-green.svg)](https://github.com/amundgaard09/amundworks)

⚠️ AmundWorks is currently under active development. Some modules and APIs may change as the system evolves.

### Key Features

- **Modular Architecture**: Projects are designed to work independently or as part of the larger ecosystem
- **Python-First Development**: Built with Python for accessibility and widespread adoption
- **Open Source**: MIT licensed with active community contributions
- **Comprehensive Tooling**: From libraries to CLI tools to operating systems

### Project Structure

AmundWorks is organized around several core pillars:

- **AWPC**: Main Python collective, including the UNIx core libraries
- **UNIx**: Core utility modules (e.g., `unimath`, `unipower`, `univiz`, etc.)
- **UniForge CLI**: Command-line interface for STEM workflows
- **XO Neural Net Series**: Machine learning and AI models
- **Vulcan Personal Productivity Platform**: Personal digital life management platform

### Getting Help

- **Documentation**: Explore detailed guides in the sections below
- **Issues**: Report bugs or request features on GitHub
- **Contributing**: Join the community and help improve AmundWorks

## Quick Start Guide

To get started with the AmundWorks Python Collective, follow these steps:

1. Install the AWPC library from PyPI using pip:
   ```bash
   pip install awpc # latest stable version
   ```

2. Import wanted modules in your Python script:
   ```python
   from awpc import unimath, unipower
   ```

3. Start using the available functions and classes in your project.
    ```python
    result = unimath.LinearEvaluation(a=5, b=3, x=2)
    print(result)  # Output: 13
    ```
 
If you're interested in using the UniForge CLI, which is a command-line interface for various tools and utilities built on top of AWPC, you can access it as follows:

1. Access the UniForge CLI by running:
    ```bash
    uniforge
    ```

2. Test what the UniForge CLI can do by running a command, such as the pythagoras calculator (the underscore `_` is used to indicate the value to be calculated, which is the standard within the UniForge CLI):
    ```bash
    unimath pythagoras 3 4 _
    ```

    Results in:

    ```bash
    A: 3, B: 4, C: 5
    ```

    
## Project Documentation

The following sections provide detailed documentation for each of the major projects built by AmundWorks. Each project is described in terms of its purpose, features, and how to get started with using it.

### AWPC - AmundWorks Python Collective

The AmundWorks Python Collective is the collection of all Python projects, modules and packages built by AmundWorks. The UNIx library is a core component of **AWPC**, providing a set of utilities and functions that are used in Python-based projects within AmundWorks. All modules under UNIx follow a consistent naming convention, starting with the prefix "uni" to indicate their association with the UNIx library. For example, you might find modules like `unimath`, `unipower`, and `univiz` within the AWPC, each offering specific functionalities related to mathematics, electrical systems, and visualizations, respectively, as well as many other modules, with some still in development.

To install AWPC, use pip:

```bash
pip install awpc
```

### UniForge CLI

The UniForge CLI is a command-line interface toolchain for anything related to STEM. It's built upon the UNIx library and provides a powerful set of commands for calculations, visualizations, and simulations. The UniForge CLI is designed to be user-friendly and efficient, making it an essential tool for anyone working with STEM projects.

If you have the AWPC library installed, you can access the UniForge CLI by running the following command in your terminal:

```bash
uniforge
```

This will launch the UniForge CLI environment. It is built with **prompt_toolkit**'s *NestedCompleter*, which serves as an auto-completion system for the CLI.

### XO Neural Net Series

The XO Neural Net Series is a collection of neural network models developed as part of the AWPC. These models are designed for various applications, including image recognition, natural language processing, and more. The series includes neural network architectures that are optimized for performance and accuracy, making them suitable for a wide range of machine learning tasks.

The XO Series is still in development, but when a production-ready model is complete, it will be made available as part of the AWPC library, allowing users to easily integrate it into their machine learning projects.

### Vulcan Personal Productivity Platform

Vulcan is a personal productivity platform developed as part of the AWPC. Vulcan is especially built for student-athletes, but it is designed to be flexible and adaptable for anyone looking to improve their productivity and organization. The platform includes features such as task management, scheduling, note-taking, and more, all integrated into a cohesive system that helps users manage their time and responsibilities effectively.

Vulcan is still in development, but when it is ready for production, it will be made available as part of the AWPC library, allowing users to easily integrate it into their personal productivity workflows.

## Contributing to AmundWorks

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

AmundWorks is entirely open-source, and contributions from the community are always welcome. If you're interested in contributing to AmundWorks, you can start by checking out the GitHub repository for the specific project you're interested in. Start by adding an issue to the repository, and then you can submit a pull request with your proposed changes. The AmundWorks team will review your contribution and provide feedback as needed. Whether you're fixing bugs, adding new features, or improving documentation, your contributions are valuable to the growth and success of AmundWorks.

## License and Usage

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org)
[![License Details](https://img.shields.io/badge/License-Details-blue.svg)](LICENSE)

All projects under AmundWorks are licensed under the MIT License, which allows for free use, modification, and distribution of the software. Users are encouraged to review the specific license files included in each project for more details on the terms and conditions of use. By using any of the AWPC projects, you agree to comply with the terms of the MIT License and acknowledge that the software is provided "as is" without any warranties or liabilities.

