import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.auth import init_db, signup_user, login_user

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Student Performance Predictor", page_icon="🎓", layout="wide")

# ---------------- INIT DATABASE ----------------
init_db()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "signin"

# ---------------- LOAD DATA & MODEL ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed_student_data.csv")

@st.cache_resource
def load_model():
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/columns.pkl", "rb") as f:
        columns = pickle.load(f)
    return model, columns

@st.cache_data
def load_raw_data():
    raw = pd.read_csv("data/student_data.csv")
    raw['total_score'] = raw['math score'] + raw['reading score'] + raw['writing score']
    raw['average_score'] = raw['total_score'] / 3
    raw['result'] = raw['average_score'].apply(lambda x: 1 if x >= 40 else 0)
    return raw

df = load_data()
df_raw = load_raw_data()
model, model_columns = load_model()

# ---------------- LOGIN / SIGNUP PAGE ----------------
def show_login_page():
    st.markdown("<br>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.3, 1])

    with center:
        st.markdown("<h2 style='text-align:center;'>🎓 Student Performance Predictor</h2>", unsafe_allow_html=True)

        with st.container(border=True):
            if st.session_state.auth_mode == "signin":
                st.markdown("<h4 style='text-align:center;'>Login to your account</h4>", unsafe_allow_html=True)

                email = st.text_input("Email", key="login_email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")

                if st.button("Sign In", use_container_width=True, type="primary"):
                    if email and password:
                        success, name, msg = login_user(email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_name = name
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please enter both email and password.")

                st.divider()
                st.caption("OR")

                if st.button("🔵 Sign in with Google", use_container_width=True, key="google_signin_1"):
                    st.login("google")

                st.write("")
                st.caption("Don't have an account?")
                if st.button("Create an account", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()

            else:  # signup mode
                st.markdown("<h4 style='text-align:center;'>Create a new account</h4>", unsafe_allow_html=True)

                new_name = st.text_input("Full Name", key="signup_name", placeholder="Your name")
                new_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
                new_password = st.text_input("Password", type="password", key="signup_password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Re-enter password")

                if st.button("Create Account", use_container_width=True, type="primary"):
                    if not (new_name and new_email and new_password and confirm_password):
                        st.warning("Please fill all fields.")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        success, msg = signup_user(new_name, new_email, new_password)
                        if success:
                            st.success("✅ Account created successfully! Logging you in...")
                            st.session_state.logged_in = True
                            st.session_state.user_name = new_name
                            st.rerun()
                        else:
                            st.error(msg)

                st.divider()
                st.caption("OR")

                if st.button("🔵 Sign up with Google", use_container_width=True, key="google_signin_2"):
                    st.login("google")

                st.write("")
                st.caption("Already have an account?")
                if st.button("Back to Sign In", use_container_width=True):
                    st.session_state.auth_mode = "signin"
                    st.rerun()


# ---------------- GOOGLE OAUTH CHECK ----------------
if st.user.is_logged_in:
    st.session_state.logged_in = True
    st.session_state.user_name = st.user.name

# ================================================================
# AUTH GATE — Login pannalana idhu kku keezha edhume run aagadhu
# ================================================================
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ---------------- LOGGED IN - WELCOME BAR + LOGOUT ----------------
col_a, col_b = st.columns([6, 1])
with col_a:
    st.write(f"👋 Welcome, **{st.session_state.user_name}**")
with col_b:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        if st.user.is_logged_in:
            st.logout()
        st.rerun()

# ---------------- TOP HORIZONTAL NAVBAR ----------------
page = option_menu(
    menu_title=None,
    options=["Home", "Dataset Overview", "EDA & Visuals", "Predict Result", "Model Insights", "Dashboard"],
    icons=["house", "bar-chart", "graph-up", "bullseye", "cpu", "speedometer2"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0e1117"},
        "icon": {"color": "orange", "font-size": "16px"},
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "margin": "0px",
            "color": "#FAFAFA",
            "--hover-color": "#262730"
        },
        "nav-link-selected": {
            "background-color": "#FF4B4B",
            "color": "#FFFFFF"
        },
    }
)

# ================================================================
# PAGE 1: HOME
# ================================================================
if page == "Home":
    st.title("🎓 Student Performance Prediction System")
    st.image("https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200", use_container_width=True)
    st.write("### Welcome! 👋")
    st.write("This ML-powered web app predicts whether a student will **Pass or Fail** based on their scores and background details.")

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Total Students", len(df))
    with col2:
        with st.container(border=True):
            st.metric("Pass Rate", f"{(df['result'].mean()*100):.1f}%")
    with col3:
        with st.container(border=True):
            st.metric("Avg Score", f"{df['average_score'].mean():.1f}")

    st.write("### 🔑 Key Features")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("#### 📊 Data Analysis")
            st.write("Explore the dataset with interactive charts and statistics.")
    with c2:
        with st.container(border=True):
            st.markdown("#### 🎯 Live Prediction")
            st.write("Enter student details and get instant Pass/Fail prediction.")
    with c3:
        with st.container(border=True):
            st.markdown("#### 📊 Dashboard")
            st.write("Filter and analyze student performance interactively.")

# ================================================================
# PAGE 2: DATASET OVERVIEW
# ================================================================
elif page == "Dataset Overview":
    st.title("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
            st.metric("Rows", df.shape[0])
    with col2:
        with st.container(border=True):
            st.metric("Columns", df.shape[1])
    with col3:
        with st.container(border=True):
            st.metric("Pass Count", int(df['result'].sum()))
    with col4:
        with st.container(border=True):
            st.metric("Fail Count", int((df['result'] == 0).sum()))

    st.write("### Preview of Data")
    st.dataframe(df.head(20), use_container_width=True)

    st.write("### Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Full Dataset", csv, "student_data.csv", "text/csv")

# ================================================================
# PAGE 3: EDA & VISUALIZATIONS
# ================================================================
elif page == "EDA & Visuals":
    st.title("📈 Exploratory Data Analysis")

    tab1, tab2, tab3 = st.tabs(["Score Distribution", "Pass/Fail Analysis", "Correlation"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            sns.histplot(df['math score'], kde=True, color="skyblue", ax=ax)
            ax.set_title("Math Score Distribution")
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            sns.histplot(df['reading score'], kde=True, color="salmon", ax=ax)
            ax.set_title("Reading Score Distribution")
            st.pyplot(fig)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            df['result'].map({1: 'Pass', 0: 'Fail'}).value_counts().plot(
                kind='pie', autopct='%1.1f%%', colors=['#4CAF50', '#F44336'], ax=ax)
            ax.set_ylabel("")
            ax.set_title("Pass vs Fail")
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            sns.boxplot(x=df['result'].map({1: 'Pass', 0: 'Fail'}), y=df['average_score'], ax=ax)
            ax.set_title("Average Score by Result")
            st.pyplot(fig)

    with tab3:
        fig, ax = plt.subplots(figsize=(10, 6))
        numeric_df = df.select_dtypes(include=['int64', 'float64', 'bool'])
        sns.heatmap(numeric_df.corr(), cmap="coolwarm", center=0, ax=ax)
        st.pyplot(fig)

# ================================================================
# PAGE 4: PREDICTION
# ================================================================
elif page == "Predict Result":
    st.title("🎯 Predict Student Result")

    with st.container(border=True):
        st.write("#### Enter Student Details")
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox("Gender", ["female", "male"])
            race = st.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
            parent_edu = st.selectbox("Parental Level of Education", [
                "some high school", "high school", "some college",
                "associate's degree", "bachelor's degree", "master's degree"
            ])

        with col2:
            lunch = st.selectbox("Lunch Type", ["standard", "free/reduced"])
            test_prep = st.selectbox("Test Preparation Course", ["none", "completed"])

        st.write("#### Enter Scores")
        c1, c2, c3 = st.columns(3)
        with c1:
            math_score = st.slider("Math Score", 0, 100, 50)
        with c2:
            reading_score = st.slider("Reading Score", 0, 100, 50)
        with c3:
            writing_score = st.slider("Writing Score", 0, 100, 50)

        predict_btn = st.button("🔍 Predict Result", use_container_width=True)

    if predict_btn:
        input_dict = {
            'math score': math_score,
            'reading score': reading_score,
            'writing score': writing_score,
            'gender_male': 1 if gender == 'male' else 0,
            'race/ethnicity_group B': 1 if race == 'group B' else 0,
            'race/ethnicity_group C': 1 if race == 'group C' else 0,
            'race/ethnicity_group D': 1 if race == 'group D' else 0,
            'race/ethnicity_group E': 1 if race == 'group E' else 0,
            "parental level of education_bachelor's degree": 1 if parent_edu == "bachelor's degree" else 0,
            "parental level of education_high school": 1 if parent_edu == "high school" else 0,
            "parental level of education_master's degree": 1 if parent_edu == "master's degree" else 0,
            "parental level of education_some college": 1 if parent_edu == "some college" else 0,
            "parental level of education_some high school": 1 if parent_edu == "some high school" else 0,
            'lunch_standard': 1 if lunch == 'standard' else 0,
            'test preparation course_none': 1 if test_prep == 'none' else 0,
        }

        input_df = pd.DataFrame([input_dict])
        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0]
        avg = (math_score + reading_score + writing_score) / 3

        result_col1, result_col2 = st.columns(2)
        with result_col1:
            with st.container(border=True):
                if prediction == 1:
                    st.success("### ✅ Result: PASS")
                else:
                    st.error("### ❌ Result: FAIL")
                st.write(f"**Confidence:** {max(proba)*100:.1f}%")
        with result_col2:
            with st.container(border=True):
                st.metric("Average Score", f"{avg:.2f}")
                st.progress(int(avg))

# ================================================================
# PAGE 5: MODEL INSIGHTS
# ================================================================
elif page == "Model Insights":
    st.title("🤖 Model Performance & Insights")

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Model Used", "Random Forest")
    with col2:
        with st.container(border=True):
            st.metric("Accuracy", "99.5%")
    with col3:
        with st.container(border=True):
            st.metric("Total Features", len(model_columns))

    st.write("### 🔥 Feature Importance")
    importance_df = pd.DataFrame({
        'Feature': model_columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=importance_df, x='Importance', y='Feature', palette='viridis', ax=ax)
    ax.set_title("Top 10 Important Features")
    st.pyplot(fig)

    st.write("### 📋 About the Model")
    with st.container(border=True):
        st.write("""
        - **Algorithm:** Random Forest Classifier  
        - **Train/Test Split:** 80% / 20%  
        - **Target:** Pass (Average Score ≥ 40) or Fail  
        - **Accuracy:** 99.5% on test data
        """)

# ================================================================
# PAGE 6: DASHBOARD
# ================================================================
elif page == "Dashboard":
    st.title("📊 Analytics Dashboard")

    with st.container(border=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            gender_filter = st.multiselect("Gender", df_raw['gender'].unique(), default=list(df_raw['gender'].unique()))
        with f2:
            lunch_filter = st.multiselect("Lunch Type", df_raw['lunch'].unique(), default=list(df_raw['lunch'].unique()))
        with f3:
            prep_filter = st.multiselect("Test Prep", df_raw['test preparation course'].unique(), default=list(df_raw['test preparation course'].unique()))

    filtered_df = df_raw[
        (df_raw['gender'].isin(gender_filter)) &
        (df_raw['lunch'].isin(lunch_filter)) &
        (df_raw['test preparation course'].isin(prep_filter))
    ]

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        with st.container(border=True):
            st.metric("Students", len(filtered_df))
    with k2:
        with st.container(border=True):
            st.metric("Pass Rate", f"{(filtered_df['result'].mean()*100):.1f}%" if len(filtered_df) else "0%")
    with k3:
        with st.container(border=True):
            st.metric("Avg Math", f"{filtered_df['math score'].mean():.1f}" if len(filtered_df) else "0")
    with k4:
        with st.container(border=True):
            st.metric("Avg Writing", f"{filtered_df['writing score'].mean():.1f}" if len(filtered_df) else "0")

    st.write("### 📈 Score Trends")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            fig, ax = plt.subplots()
            avg_scores = filtered_df[['math score', 'reading score', 'writing score']].mean()
            avg_scores.plot(kind='bar', color=['#FF4B4B', '#4B8BFF', '#4BFF87'], ax=ax)
            ax.set_title("Average Scores by Subject")
            ax.set_ylabel("Score")
            st.pyplot(fig)
    with c2:
        with st.container(border=True):
            fig, ax = plt.subplots()
            gender_result = pd.crosstab(filtered_df['gender'], filtered_df['result'].map({1: 'Pass', 0: 'Fail'}))
            gender_result.plot(kind='bar', stacked=True, color=['#F44336', '#4CAF50'], ax=ax)
            ax.set_title("Pass/Fail by Gender")
            ax.set_ylabel("Count")
            st.pyplot(fig)

    st.write("### 🎓 Parental Education Impact")
    with st.container(border=True):
        fig, ax = plt.subplots(figsize=(10, 5))
        edu_avg = filtered_df.groupby('parental level of education')['average_score'].mean().sort_values()
        edu_avg.plot(kind='barh', color='#FFA726', ax=ax)
        ax.set_xlabel("Average Score")
        ax.set_title("Average Score by Parental Education Level")
        st.pyplot(fig)

    st.write("### 📋 Filtered Data")
    with st.container(border=True):
        st.dataframe(filtered_df, use_container_width=True)