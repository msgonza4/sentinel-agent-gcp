from google.cloud import firestore
import datetime

# Initialize Firestore
db = firestore.Client(project="uiw-sentinel-agent")

def generate_security_brief():
    print("=" * 60)
    print("       UIW SENTINEL AGENT — SECURITY BRIEF")
    print(f"       Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 60)

    # Pull top 5 highest threat scores from Firestore
    findings = (
        db.collection("agent-findings")
        .order_by("threat_score", direction=firestore.Query.DESCENDING)
        .limit(5)
        .stream()
    )

    results = list(findings)

    if not results:
        print("\n No findings recorded yet in agent-findings collection.")
        return

    print(f"\n TOP {len(results)} THREAT FINDINGS\n")

    for i, doc in enumerate(results, start=1):
        data = doc.to_dict()
        print(f"  Finding #{i}")
        print(f"  Threat Score:      {data.get('threat_score', 'N/A')}")
        print(f"  Threat Vectors:    {', '.join(data.get('threat_vectors', []))}")
        print(f"  Recommendation:    {data.get('mitigation_recommendation', 'N/A')}")
        print(f"  Timestamp:         {data.get('timestamp', 'N/A')}")
        print("-" * 60)

    print("\n END OF SECURITY BRIEF")
    print("=" * 60)

if __name__ == "__main__":
    generate_security_brief()
