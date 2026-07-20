from flask import Flask, jsonify, render_template, request
# Import the stock list and data structures from your uploaded file
import ipo_data

app = Flask(__name__)


@app.route("/")
def index():
    """Renders the main page displaying the list of 2026 IPO stocks."""
    # Assuming ipo_data.py contains a list or dictionary named 'IPO_LIST'
    stocks = getattr(ipo_data, "IPO_LIST", [])
    return render_template("index.html", stocks=stocks)


@app.route("/api/stocks", methods=["GET"])
def get_stocks():
    """API endpoint to fetch all IPO stocks covered in ipo_data.py."""
    stocks = getattr(ipo_data, "IPO_LIST", [])
    return jsonify({"status": "success", "count": len(stocks), "data": stocks})


@app.route("/api/stocks/search", methods=["GET"])
def search_stocks():
    """API endpoint to search stocks by code or company name."""
    query = request.args.get("q", "").lower()
    stocks = getattr(ipo_data, "IPO_LIST", [])

    if not query:
        return jsonify({"status": "success", "data": stocks})

    # Filter based on stock code or name matching the query
    filtered_stocks = [
        s
        for s in stocks
        if query in str(s.get("code", "")).lower()
        or query in s.get("name", "").lower()
    ]

    return jsonify(
        {
            "status": "success",
            "count": len(filtered_stocks),
            "data": filtered_stocks,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
