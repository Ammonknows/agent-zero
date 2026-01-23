"""
PRISM-KAD-TDS-MAU Documentation Generator

Generates technical documentation from a template and extracted knowledge.
Supports multiple output formats and audience-specific content filtering.

Usage:
    python generate_docs.py <input_json> <output_path> [--format md|html]

Arguments:
    input_json: Path to JSON file containing extracted system knowledge
    output_path: Path where generated documentation will be written

The input JSON should contain the following structure:
{
    "system_name": "Name of the system",
    "version": "1.0.0",
    "purpose_overview": "Description of system purpose",
    "key_features": ["feature1", "feature2"],
    "components": [
        {
            "name": "Component Name",
            "purpose": "What it does",
            "functionality": "Key capabilities",
            "interactions": ["interacts with X", "receives from Y"],
            "technical_details": "Implementation info"
        }
    ],
    "functionality": {
        "core": [...],
        "advanced": [...],
        "use_cases": [...]
    },
    "technical": {
        "specifications": "...",
        "api_reference": "...",
        "implementation": "..."
    },
    "user_guide": {
        "installation": "...",
        "basic_usage": "...",
        "troubleshooting": "..."
    },
    "appendices": {
        "glossary": {...},
        "faq": [...],
        "resources": [...]
    }
}
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional


def _get_func_name(core_list: List, index: int, default: str) -> str:
    """Extract function name from a core functionality list item."""
    if index >= len(core_list):
        return default
    item = core_list[index]
    if isinstance(item, dict):
        return item.get("name", default)
    return str(item) if item else default


def load_template(template_name: str) -> str:
    """Load a template file from the templates directory."""
    script_dir = Path(__file__).parent.parent
    template_path = script_dir / "templates" / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def render_template(template: str, context: Dict[str, Any]) -> str:
    """Simple template rendering with {{variable}} substitution."""
    result = template
    for key, value in context.items():
        placeholder = "{{" + key + "}}"
        if isinstance(value, list):
            rendered_value = "\n".join(f"- {item}" for item in value)
        elif isinstance(value, dict):
            rendered_value = "\n".join(f"- **{k}:** {v}" for k, v in value.items())
        else:
            rendered_value = str(value)
        result = result.replace(placeholder, rendered_value)
    return result


def generate_knowledge_map(data: Dict[str, Any]) -> str:
    """Generate a mermaid mindmap from system knowledge."""
    system_name = data.get("system_name", "System")
    components = data.get("components", [])
    functionality = data.get("functionality", {})

    lines = [
        "```mermaid",
        "mindmap",
        f"  root([{system_name} Knowledge Map])",
        "    Purpose & Scope",
    ]

    # Add purpose items
    if data.get("purpose_overview"):
        purpose_short = data["purpose_overview"][:60]
        lines.append(f"      {purpose_short}")

    # Add components
    lines.append("    System Architecture")
    for comp in components[:5]:
        name = comp.get("name", "Unknown")
        lines.append(f"      {name}")

    # Add functionality
    lines.append("    Core Functionality")
    for func in functionality.get("core", [])[:5]:
        if isinstance(func, dict):
            lines.append(f"      {func.get('name', 'Unknown')}")
        else:
            lines.append(f"      {func}")

    lines.append("```")
    return "\n".join(lines)


def generate_architecture_diagram(components: List[Dict[str, Any]]) -> str:
    """Generate a mermaid flowchart from component interactions."""
    if not components:
        return "    A[System] --> B[No components defined]"

    lines = []
    node_ids = {}
    for i, comp in enumerate(components):
        node_id = chr(65 + i) if i < 26 else f"N{i}"
        node_ids[comp.get("name", f"Component_{i}")] = node_id
        lines.append(f"    {node_id}[{comp.get('name', f'Component {i}')}]")

    # Add interactions
    for comp in components:
        src_id = node_ids.get(comp.get("name", ""))
        if not src_id:
            continue
        for interaction in comp.get("interactions", []):
            if isinstance(interaction, str):
                # Try to find target component
                for target_name, target_id in node_ids.items():
                    if target_name.lower() in interaction.lower() and target_id != src_id:
                        lines.append(f"    {src_id} --> {target_id}")
                        break

    return "\n".join(lines)


def generate_component_docs(components: List[Dict[str, Any]]) -> str:
    """Generate detailed component documentation."""
    if not components:
        return "No components documented."

    sections = []
    for comp in components:
        section = [
            f"**Component: {comp.get('name', 'Unknown')}**",
            f"- **Purpose:** {comp.get('purpose', 'Not specified')}",
            f"- **Functionality:** {comp.get('functionality', 'Not specified')}",
        ]

        interactions = comp.get("interactions", [])
        if interactions:
            section.append("- **Interactions:**")
            for inter in interactions:
                section.append(f"  - {inter}")

        tech = comp.get("technical_details", "")
        if tech:
            section.append(f"- **Technical Details:** {tech}")

        section.append("")
        sections.append("\n".join(section))

    return "\n".join(sections)


def generate_functionality_docs(functionality: Dict[str, Any]) -> str:
    """Generate functionality documentation."""
    sections = []

    core = functionality.get("core", [])
    if core:
        for func in core:
            if isinstance(func, dict):
                sections.append(f"**{func.get('name', 'Function')}**")
                sections.append(f"- **Description:** {func.get('description', '')}")
                if func.get("use_cases"):
                    sections.append("- **Use Cases:**")
                    for uc in func["use_cases"]:
                        sections.append(f"  - {uc}")
                if func.get("examples"):
                    sections.append("- **Examples:**")
                    for ex in func["examples"]:
                        sections.append(f"  - {ex}")
                sections.append("")
            else:
                sections.append(f"- {func}")

    return "\n".join(sections) if sections else "Core functionality not yet documented."


def generate_glossary(glossary: Dict[str, str]) -> str:
    """Generate glossary section."""
    if not glossary:
        return "No glossary entries defined."

    lines = []
    for term, definition in sorted(glossary.items()):
        lines.append(f"- **{term}:** {definition}")
    return "\n".join(lines)


def generate_faq(faq: List[Dict[str, str]]) -> str:
    """Generate FAQ section."""
    if not faq:
        return "No FAQ entries defined."

    lines = []
    for i, entry in enumerate(faq, 1):
        lines.append(f"**Q{i}: {entry.get('question', 'Unknown')}**")
        lines.append(f"  {entry.get('answer', 'No answer provided.')}")
        lines.append("")
    return "\n".join(lines)


def build_documentation(data: Dict[str, Any]) -> str:
    """Build complete documentation from extracted system knowledge."""
    template = load_template("documentation_template.md")

    components = data.get("components", [])
    functionality = data.get("functionality", {})
    technical = data.get("technical", {})
    user_guide = data.get("user_guide", {})
    appendices = data.get("appendices", {})

    context = {
        "system_name": data.get("system_name", "System"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "doc_version": "1.0",
        "system_version": data.get("version", "1.0.0"),
        # Knowledge map placeholders
        "problem_addressed": data.get("problem_addressed", "Problem domain"),
        "target_users": data.get("target_users", "Target users"),
        "key_capabilities": data.get("key_capabilities", "Key capabilities"),
        "component_1": components[0]["name"] if len(components) > 0 else "Component 1",
        "component_2": components[1]["name"] if len(components) > 1 else "Component 2",
        "component_3": components[2]["name"] if len(components) > 2 else "Component 3",
        "function_area_1": _get_func_name(functionality.get("core", []), 0, "Area 1"),
        "function_area_2": _get_func_name(functionality.get("core", []), 1, "Area 2"),
        "function_area_3": _get_func_name(functionality.get("core", []), 2, "Area 3"),
        "technologies": data.get("technologies", "Technologies"),
        "algorithms": data.get("algorithms", "Algorithms"),
        "data_structures": data.get("data_structures", "Data Structures"),
        "workflows": data.get("workflows", "Workflows"),
        "interfaces": data.get("interfaces", "Interfaces"),
        "use_cases": data.get("use_cases_summary", "Use Cases"),
        # Content sections
        "purpose_overview": data.get("purpose_overview", "Purpose not specified."),
        "key_features": "\n".join(f"- {f}" for f in data.get("key_features", [])) or "No features listed.",
        "getting_started": data.get("getting_started", "Getting started information not provided."),
        "architecture_diagram": generate_architecture_diagram(components),
        "architecture_description": data.get("architecture_description", "Architecture description not provided."),
        "component_details": generate_component_docs(components),
        "integration_points": data.get("integration_points", "No integration points documented."),
        "core_functionality": generate_functionality_docs(functionality),
        "advanced_features": data.get("advanced_features", "No advanced features documented."),
        "use_cases_detailed": data.get("use_cases_detailed", "No detailed use cases provided."),
        "technical_specifications": technical.get("specifications", "No specifications provided."),
        "api_reference": technical.get("api_reference", "No API reference provided."),
        "implementation_details": technical.get("implementation", "No implementation details provided."),
        "installation_guide": user_guide.get("installation", "No installation guide provided."),
        "basic_usage": user_guide.get("basic_usage", "No usage guide provided."),
        "troubleshooting": user_guide.get("troubleshooting", "No troubleshooting guide provided."),
        "glossary": generate_glossary(appendices.get("glossary", {})),
        "faq": generate_faq(appendices.get("faq", [])),
        "additional_resources": "\n".join(f"- {r}" for r in appendices.get("resources", [])) or "No additional resources listed.",
        "feedback_info": data.get("feedback_info", "Please provide feedback through the appropriate channels."),
    }

    return render_template(template, context)


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_docs.py <input_json> <output_path> [--format md|html]")
        print("\nGenerates technical documentation from extracted system knowledge.")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    output_format = "md"

    if "--format" in sys.argv:
        fmt_idx = sys.argv.index("--format")
        if fmt_idx + 1 < len(sys.argv):
            output_format = sys.argv[fmt_idx + 1]

    # Load input data
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Generate documentation
    documentation = build_documentation(data)

    # Write output
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "html":
        # Wrap in basic HTML structure
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('system_name', 'System')} Documentation</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 2rem; line-height: 1.6; }}
        pre {{ background: #f6f8fa; padding: 1rem; border-radius: 6px; overflow-x: auto; }}
        code {{ background: #f6f8fa; padding: 0.2rem 0.4rem; border-radius: 3px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
        th {{ background: #f6f8fa; }}
        h1 {{ border-bottom: 2px solid #333; padding-bottom: 0.5rem; }}
        h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 0.3rem; }}
    </style>
</head>
<body>
<pre>{documentation}</pre>
</body>
</html>"""
        output_file.write_text(html_content, encoding="utf-8")
    else:
        output_file.write_text(documentation, encoding="utf-8")

    print(f"Documentation generated: {output_file}")
    print(f"Format: {output_format}")
    print(f"System: {data.get('system_name', 'Unknown')}")


if __name__ == "__main__":
    main()
