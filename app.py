import streamlit as st
import requests
import datetime

LIMIT=5
# AABRA KA DAABRA
def get_week_bounds():
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(days=now.weekday())
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    sunday = monday + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
    return monday, sunday

def get_unique_questions_this_week(username):
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
    except Exception:
        return 0, []

    monday, sunday = get_week_bounds()

    unique_titles = {
        s["title"]
        for s in submissions
        if monday.timestamp() <= int(s["timestamp"]) <= sunday.timestamp()
    }

    return len(unique_titles), list(unique_titles)

members = [
    {"name": "Harshit Chaudhary", "username": "Harshit_Chaudhry"},
    {"name": "Krishna Mehta", "username": "Krishna-Mehta-135"},    # https://leetcode.com/u/Krishna-Mehta-135/
    {"name": "Soumalya", "username": "froskersss"},
    {"name": "Ritesh Hooda", "username": "ritesh-251"},
    {"name": "Alok", "username": "aloksingh98541"},
    {"name": "Samim", "username": "samim020"},
    {"name": "Ashish Jha", "username": "ashishjha0125"},
    {"name": "Yogesh", "username": "HY12925"},
    {"name": "Dishu", "username": "dvsp1020"},
]
# https://leetcode.com/u/dvsp1020/


st.set_page_config(page_title="LeetCode Weekly Tracker", layout="centered")
st.title("📊 LeetCode Weekly Tracker")


st.warning(f"⚠️ **Disclaimer:** All members must solve at least **{LIMIT} unique questions** this week. "
           "Failure to do so will result in **removal** from the community.")


monday, sunday = get_week_bounds()
st.caption(f"Tracking submissions from **{monday.strftime('%b %d, %Y')}** to **{sunday.strftime('%b %d, %Y')}**")


leaderboard = []

with st.spinner("🔍 Fetching data from LeetCode..."):
    for member in members:
        count, _ = get_unique_questions_this_week(member["username"])
        leaderboard.append((member["name"], count))


leaderboard.sort(key=lambda x: -x[1])

st.success("✅ Fetched progress for all users.")
st.markdown("### 🏆 Leaderboard")


for i, (name, count) in enumerate(leaderboard, start=1):
    status_icon = "✅" if count >= LIMIT else "❌"
    st.write(f"**{i}. {name}** — {status_icon} {count} unique questions this week")


if st.checkbox("Show full data table"):
    st.dataframe(
        {
            "Name": [name for name, _ in leaderboard],
            "Questions Solved": [count for _, count in leaderboard],
            "Status": ["✅" if count >= LIMIT else "❌" for _, count in leaderboard]
        },
        use_container_width=True
    )


# 👣 Footer
#st.markdown("""
#---
#<div style='text-align: center; font-size: 14px; color: gray;'>
#    Created by <strong>Harshit</strong>
#</div>
#""", unsafe_allow_html=True)
