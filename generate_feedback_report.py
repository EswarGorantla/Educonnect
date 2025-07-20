import json

# Load the generated feedback
with open("feedback/interview_feedback.json", "r") as f:
    feedback_data = json.load(f)

# Example structure — adjust based on what your data contains
def generate_report(data):
    print("\n🎯 MOCK INTERVIEW FEEDBACK REPORT\n")
    
    for frame in data.get("frames", []):
        time = frame.get("timestamp", "Unknown")
        issues = frame.get("issues", [])
        
        if issues:
            print(f"⏱ Time: {time}")
            for issue in issues:
                print(f"  ❗ Issue: {issue}")
            print("  💡 Tip: Practice maintaining better posture and eye contact.\n")

    print("✅ End of Feedback.\nKeep practicing for better performance!")

# Run
generate_report(feedback_data)
