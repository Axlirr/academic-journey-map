# Contributing to Academic Journey Map

First off, thank you for considering contributing to Academic Journey Map! It's people like you that make this project such a great tool for the academic community.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue list](https://github.com/Axlirr/academic-journey-map/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](https://github.com/Axlirr/academic-journey-map/issues). When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed functionality
* Any possible drawbacks or challenges
* If possible, a mock-up or sketch of the proposed feature

### Pull Requests

1. Fork the repository and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Issue that pull request!

## Development Process

1. Clone the repository
```bash
git clone https://github.com/Axlirr/academic-journey-map.git
cd academic-journey-map
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

3. Install development dependencies
```bash
pip install -r requirements-dev.txt
```

4. Create a branch
```bash
git checkout -b feature/your-feature-name
```

5. Make your changes and commit
```bash
git add .
git commit -m "Description of your changes"
```

6. Push to your fork
```bash
git push origin feature/your-feature-name
```

7. Open a Pull Request

## Style Guide

### Python Code Style

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use type hints
* Write docstrings for all public methods and classes
* Keep lines under 88 characters (Black default)
* Use meaningful variable names

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Documentation Style

* Use Markdown for documentation
* Include code examples when relevant
* Keep explanations clear and concise
* Update the README.md if needed

## Testing

* Write tests for all new features
* Ensure all tests pass before submitting a pull request
* Include both unit tests and integration tests
* Test edge cases and error conditions

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_visualizations.py
```

## Code Review Process

The core team looks at Pull Requests on a regular basis. After feedback has been given we expect responses within two weeks. After two weeks we may close the PR if it isn't showing any activity.

## Community

* Join our [Discord server](https://discord.gg/academic-journey)
* Follow us on [Twitter](https://twitter.com/AcademicJourney)
* Read our [blog](https://academic-journey-map.com/blog)

## Recognition

Contributors who make significant improvements will be added to the README.md and given credit for their work.

## Questions?

Feel free to contact the core team if you have any questions or need guidance:

* 📧 Email: contributors@academic-journey-map.com
* 💬 Discord: [Join our community](https://discord.gg/academic-journey)
* 📝 GitHub Discussions: [Start a discussion](https://github.com/Axlirr/academic-journey-map/discussions)