from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route("/compare", methods=["POST"])
def compare():
    data = request.json
    companies = data["companies"]

    results = []
    for i, company in enumerate(companies):
        try:
            qci = company["qci"]
            relationship_level = company["relationshipLevel"]
            technicians = company["technicians"]
            open_jobs = company["openJobs"]
            scheduled_jobs = company["scheduledJobs"]

            # QCI Calculation
            weighted_qci = qci * 0.5

            # Relationship Level Calculation
            relationship_points = {"COL": 42.5, "CSP": 42.5, "CI": 15}
            weighted_relationship_score = relationship_points[relationship_level] * 0.3

            # Capacity Calculation
            total_capacity = technicians * 10
            active_jobs = open_jobs + scheduled_jobs
            remaining_capacity = max(0, total_capacity - active_jobs)
            capacity_score = (remaining_capacity / total_capacity) * 100 if total_capacity > 0 else 0
            weighted_capacity_score = capacity_score * 0.2

            # Final Score
            final_score = weighted_qci + weighted_relationship_score + weighted_capacity_score

            results.append({
                "companyId": i + 1,
                "finalScore": final_score
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # Sort results by final score in descending order
    results = sorted(results, key=lambda x: x["finalScore"], reverse=True)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)(debug=True)
