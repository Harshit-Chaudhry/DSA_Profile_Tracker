import streamlit as st
import requests
import datetime

# 1. Function to get unique AC submissions
def get_unique_questions(username, days):
    url = "https://leetcode.com/graphql/"

    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/u/{username}/",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {
        "operationName": "recentAcSubmissionList",
        "variables": {
            "username": username,
            "limit": 100
        },
        "query": """
        query recentAcSubmissionList($username: String!, $limit: Int!) {
          recentAcSubmissionList(username: $username, limit: $limit) {
            id
            title
            timestamp
          }
        }
        """
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        submissions = data.get("data", {}).get("recentAcSubmissionList", [])
    except Exception as e:
        return 0, []

    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    unique_titles = {
        s["title"]
        for s in submissions
        if datetime.datetime.fromtimestamp(int(s["timestamp"])) >= cutoff
    }

    return len(unique_titles), list(unique_titles)

# 2. List of group members
members = [
    {"name": "Harshit", "username": "Harshit_Chaudhry"},
    {"name": "Krishna Mehta", "username": "_krishnamehta_"},
    {"name": "Soumalya", "username": "froskersss"},
    {"name": "Ritesh Hooda", "username": "ritesh-251"},
    {"name": "Alok", "username": "aloksingh98541"},
    {"name": "Samim", "username": "samim020"},
    {"name": "Ashish Jha", "username": "ashishjha0125"},
    {"name": "Yogesh", "username": "HY12925"},
]

# 3. Streamlit UI
st.set_page_config(page_title="LeetCode Weekly Tracker", layout="centered")
st.title("📊 LeetCode Weekly Tracker")
days = st.slider("Select number of days to track", min_value=1, max_value=30, value=7)

leaderboard = []

with st.spinner("Fetching data..."):
    for member in members:
        count, _ = get_unique_questions(member["username"], days)
        leaderboard.append((member["name"], count))

leaderboard.sort(key=lambda x: -x[1])

st.success(f"Tracked progress for {len(members)} users over last {days} days.")
st.markdown("### 🏆 Leaderboard")
for i, (name, count) in enumerate(leaderboard, start=1):
    st.write(f"**{i}. {name}** — ✅ {count} unique questions")

# Optional: Show raw table
if st.checkbox("Show full table"):
    st.dataframe({name: count for name, count in leaderboard}, use_container_width=True)
