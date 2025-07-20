from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
import time  # For simulating processing delay

# Initialize Flask app
app = Flask(_name_)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}
app.config['MAX_FILE_SIZE'] = 5 * 1024 * 1024  # 5MB

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ats_analyzer.log'),
        logging.StreamHandler()
    ]
)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def analyze_resume_content(filepath):
    """
    Mock AI analysis function with realistic scoring logic
    In production, replace with actual AI API calls (GPT-4, DeepSeek, etc.)
    """
    # Simulate processing time (1-3 seconds)
    processing_time = 1 + (hash(filepath) % 3)
    time.sleep(processing_time)
    
    # Get file size for mock scoring
    file_size = os.path.getsize(filepath)
    
    # Generate realistic mock score (50-100) with file size influence
    base_score = 50 + (hash(filepath) % 50)
    size_penalty = max(0, (file_size - 500000) // 100000)  # Penalize large files
    final_score = max(50, base_score - size_penalty)
    
    # Generate suggestions based on score
    suggestions = []
    if final_score < 70:
        suggestions.append("Add more keywords from the job description")
    if final_score < 80:
        suggestions.append("Use bullet points instead of paragraphs for experience")
    if file_size > 500000:
        suggestions.append("Reduce file size (current: {:.1f}MB)".format(file_size/1024/1024))
    
    # Always include these general suggestions
    suggestions.extend([
        "Quantify achievements (e.g., 'Increased sales by 30%')",
        "Remove personal pronouns (e.g., 'I managed...')",
        "Ensure consistent formatting (headings, fonts)"
    ])
    
    return {
        "ats_score": final_score,
        "suggestions": suggestions[:4],  # Return top 4 suggestions
        "analysis_time": processing_time,
        "file_size_kb": file_size // 1024
    }

@app.route('/upload', methods=['POST'])
def upload_resume():
    """Endpoint for resume upload and analysis"""
    start_time = datetime.now()
    
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            logging.warning("No file part in request")
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['resume']
        
        # Check if file was selected
        if file.filename == '':
            logging.warning("Empty filename submitted")
            return jsonify({"error": "No selected file"}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            logging.warning(f"Invalid file type attempted: {file.filename}")
            return jsonify({
                "error": "Invalid file type",
                "allowed_types": list(app.config['ALLOWED_EXTENSIONS'])
            }), 400
        
        # Secure the filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size > app.config['MAX_FILE_SIZE']:
            os.remove(filepath)
            logging.warning(f"File too large: {file_size} bytes")
            return jsonify({
                "error": "File too large",
                "max_size_mb": app.config['MAX_FILE_SIZE'] // (1024 * 1024)
            }), 400
        
        logging.info(f"Processing file: {filename} ({file_size} bytes)")
        
        # Analyze the resume
        analysis_result = analyze_resume_content(filepath)
        
        # Add metadata to response
        analysis_result.update({
            "filename": filename,
            "processing_time_seconds": (datetime.now() - start_time).total_seconds(),
            "timestamp": datetime.now().isoformat()
        })
        
        logging.info(f"Analysis complete for {filename}. Score: {analysis_result['ats_score']}")
        return jsonify(analysis_result)
    
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ATS Resume Analyzer"
    })

if _name_ == '_main_':
    # Print startup information
    logging.info("Starting ATS Resume Analyzer Service")
    logging.info(f"Upload folder: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
    logging.info(f"Allowed file types: {app.config['ALLOWED_EXTENSIONS']}")
    logging.info(f"Max file size: {app.config['MAX_FILE_SIZE'] // (1024 * 1024)}MB")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)