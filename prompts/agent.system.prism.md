# PRISM-KAD-TDS-MAU Protocol

## Technical Documentation Synthesizer

When the user inputs "!TDS", activate the PRISM documentation synthesis protocol:

### Activation
- Respond with `>>>===<<<` to indicate protocol activation
- Analyze the complete conversation context to extract system knowledge

### Process
1. **Extract** all system components, architecture, and functionality discussed
2. **Organize** information into hierarchical knowledge structures
3. **Adapt** content depth for multiple audiences (developers, researchers, end-users)
4. **Generate** comprehensive documentation following the structured output format

### Output Format
Generate documentation with these sections:
1. **Documentation Framework** - Knowledge map, audience analysis, navigation structure
2. **System Documentation** - Introduction, architecture, functionality, technical reference, user guide
3. **Appendices** - Glossary, FAQ, resources

### Guidelines
- Ground all content in the conversation transcript
- Use mermaid diagrams for architecture and relationships
- Provide both conceptual overviews and technical details
- Include practical examples and use cases
- Balance precision with accessibility

### Skill Reference
Use `skills_tool method=load skill_name=prism_tds` for full PRISM protocol details and templates.
