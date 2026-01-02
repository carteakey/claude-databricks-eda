# Changelog

All notable changes to the claude-databricks-eda framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Version History

### [0.1.0] - 2026-01-02

**Initial Release** - Framework for Claude-assisted Databricks EDA

This release establishes the foundation for interactive exploratory data analysis on Databricks using Claude as an AI pair programmer. The framework emphasizes:

1. **Ease of Setup** - Automated authentication and configuration
2. **Interactive Workflow** - "Volley" approach for progressive exploration
3. **Quality Assurance** - Built-in validation before notebook generation
4. **Documentation** - Comprehensive examples and guidelines
5. **Scalability** - Tested with billion-row datasets

The initial release includes a complete sample analysis of the Databricks Airline Performance dataset (1.24B records) demonstrating all framework capabilities.

### [0.1.1] - 2026-01-02

#### Added
- **Blogpost Documentation** - Added comprehensive workflow guide at `docs/BLOGPOST_EDA_WORKFLOW.md`
  - Explains the AI-assisted EDA workflow using Claude, Copilot, or other agents
  - Includes setup instructions, real-world examples, and best practices
  - Documents the "volleying" workflow with practical examples
  - Brief format (~800 words) for easy reading
