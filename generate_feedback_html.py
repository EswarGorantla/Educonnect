import json

def generate_html_report(data):
    html_content = """
    <html>
    <head>
        <title>Mock Interview Feedback</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f9;
                color: #333;
                padding: 40px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #2980b9;
                padding-bottom: 10px;
            }
            .section {
                margin-bottom: 40px;
            }
            .frame {
                background: #fff;
                padding: 15px;
                margin-bottom: 20px;
                border-left: 5px solid #3498db;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            ul {
                margin: 0;
                padding-left: 20px;
            }
        </style>
    </head>
    <body>
        <h1>🎯 Mock Interview Feedback Report</h1>
    """

    frames = data.get("frames", [])
    summary = data.get("summary", {})

    html_content += "<div class='section'><h2>Frame-wise Feedback</h2>"

    for frame in frames:
        html_content += f"""
        <div class="frame">
            <h3>⏱️ Frame {frame['frame']}</h3>
            <strong>Issues:</strong>
            <ul>{"".join(f"<li>{issue}</li>" for issue in frame['issues'])}</ul>
            <strong>Suggestions:</strong>
            <ul>{"".join(f"<li>{tip}</li>" for tip in frame['tips'])}</ul>
        </div>
        """

    html_content += "</div>"

    html_content += "<div class='section'><h2>🧠 Summary</h2>"
    html_content += f"<p><strong>Overall:</strong> {summary.get('overall', 'N/A')}</p>"
    html_content += "<ul>" + "".join(f"<li>{s}</li>" for s in summary.get("suggestions", [])) + "</ul>"
    html_content += "</div>"

    html_content += "</body></html>"

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ HTML report generated: report.html")

# Load feedback data and generate HTML
with open("feedback/interview_feedback.json", "r") as f:
    feedback_data = json.load(f)

generate_html_report(feedback_data)
