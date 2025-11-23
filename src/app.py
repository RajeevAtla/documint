"""Gradio application entrypoint."""

from typing import Tuple

import gradio as gr

from src.agents.workflow import build_workflow
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Build workflow once at startup
WORKFLOW = build_workflow()


def modernize_documentation(url: str, progress=gr.Progress(track_tqdm=True)) -> Tuple[str, str, str, str]:
    """
    Run the documentation modernization workflow and format outputs.

    Args:
        url: Documentation URL.
        progress: Gradio progress tracker.

    Returns:
        Tuple of markdown strings for original, analysis, modernized, and quality report.
    """
    if not url:
        return "⚠️ Please provide a URL.", "", "", ""

    progress(0.05, desc="Building workflow...")
    try:
        progress(0.2, desc="Fetching documentation...")
        initial_state = {
            "url": url,
            "raw_html": "",
            "original_content": "",
            "analyzed_sections": [],
            "research_results": [],
            "modernized_markdown": "",
            "quality_report": {},
            "messages": [],
            "error": None,
        }

        result = WORKFLOW.invoke(initial_state)

        if result.get("error"):
            return f"⚠️ Error: {result['error']}", "", "", ""

        progress(0.4, desc="Analyzing content...")
        progress(0.6, desc="Researching best practices...")
        progress(0.8, desc="Generating modernized documentation...")
        progress(0.9, desc="Performing quality check...")

        original = result.get("original_content", "No content available")

        analyzed_sections = result.get("analyzed_sections", [])
        if analyzed_sections:
            analysis = "## Issues Identified\n\n"
            severity_groups = {"high": [], "medium": [], "low": []}
            for issue in analyzed_sections:
                severity = issue.get("severity", "low")
                severity_groups.get(severity, severity_groups["low"]).append(issue)

            for label, icon in [("high", "⚠️"), ("medium", "⚡"), ("low", "ℹ️")]:
                group = severity_groups.get(label, [])
                if group:
                    analysis += f"### {icon} {label.capitalize()} Severity\n"
                    for issue in group:
                        analysis += f"- **{issue.get('section', 'N/A')}**: {issue.get('description', '')}\n"
                    analysis += "\n"
        else:
            analysis = "No issues identified."

        modernized = result.get("modernized_markdown", "No content generated")

        quality_report = result.get("quality_report", {})
        scores = quality_report.get("scores", {})
        suggestions = quality_report.get("suggestions", [])
        avg_score = quality_report.get("average_score", 0)

        quality = "## Quality Assessment\n\n"
        quality += "### Scores\n\n"
        quality += f"- **Completeness**: {scores.get('completeness', 'N/A')}/10\n"
        quality += f"- **Clarity**: {scores.get('clarity', 'N/A')}/10\n"
        quality += f"- **Technical Accuracy**: {scores.get('technical_accuracy', 'N/A')}/10\n"
        quality += f"- **Modernization Effectiveness**: {scores.get('modernization_effectiveness', 'N/A')}/10\n"
        quality += f"\n**Average Score**: {avg_score}/10\n\n"

        if suggestions:
            quality += "### Suggestions for Improvement\n\n"
            for suggestion in suggestions:
                quality += f"- {suggestion}\n"

        progress(1.0, desc="Complete!")
        logger.info("Processing completed successfully for %s", url)

        return original, analysis, modernized, quality

    except Exception as exc:
        logger.error("Error processing documentation: %s", exc, exc_info=True)
        error_msg = f"⚠️ An error occurred: {str(exc)}"
        return error_msg, "", "", ""


def create_interface() -> gr.Blocks:
    """Create and configure Gradio interface."""

    with gr.Blocks(title="Technical Documentation Modernizer", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
        # 🛠️ Technical Documentation Modernizer

        Modernize technical documentation using AI-powered analysis and generation.

        **How it works:**
        1. Enter a documentation URL
        2. AI analyzes the content for outdated information
        3. Researches current best practices
        4. Generates modernized markdown documentation
        5. Provides quality assessment
        """
        )

        with gr.Row():
            url_input = gr.Textbox(
                label="Documentation URL",
                placeholder="https://example.com/docs/guide",
                scale=4,
            )
            submit_btn = gr.Button("✨ Modernize", variant="primary", scale=1)

        gr.Markdown("### Example URLs to try:")
        gr.Examples(
            examples=[
                ["https://docs.python.org/2.7/tutorial/introduction.html"],
                ["https://legacy.reactjs.org/docs/getting-started.html"],
            ],
            inputs=url_input,
            label="Click to load example",
        )

        with gr.Tabs():
            with gr.Tab("📄 Original Documentation"):
                original_output = gr.Markdown(
                    label="Original Content",
                    value="Original documentation will appear here...",
                )

            with gr.Tab("🔍 Analysis"):
                analysis_output = gr.Markdown(
                    label="Issues Identified",
                    value="Analysis results will appear here...",
                )

            with gr.Tab("📝 Modernized Documentation"):
                modernized_output = gr.Markdown(
                    label="Modernized Content",
                    value="Modernized documentation will appear here...",
                )

            with gr.Tab("✅ Quality Report"):
                quality_output = gr.Markdown(
                    label="Quality Assessment",
                    value="Quality assessment will appear here...",
                )

        gr.Markdown(
            """
        ---
        ### Tips:
        - Best results with technical documentation (guides, tutorials, API docs)
        - Processing takes 30-60 seconds depending on content length
        - The tool analyzes structure, updates outdated info, and applies modern best practices
        """
        )

        submit_btn.click(
            fn=modernize_documentation,
            inputs=[url_input],
            outputs=[original_output, analysis_output, modernized_output, quality_output],
        )

    return demo


def main():
    """Main application entry point."""
    logger.info("Starting Technical Documentation Modernizer")

    try:
        demo = create_interface()
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)
    except Exception as exc:
        logger.error("Failed to start application: %s", exc, exc_info=True)
        raise


if __name__ == "__main__":
    main()
