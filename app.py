import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from rational_analyzer import RationalAnalyzer
from game_modes import GameModes
import random

# Page configuration
st.set_page_config(
    page_title="Rational Function Graph Game",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "Function Input"
if 'current_function' not in st.session_state:
    st.session_state.current_function = None
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

# Main title and description
st.title("🎯 Rational Function Graph Game")
st.markdown("""
Welcome to the **Interactive Rational Function Learning Game**! 

Master the art of graphing rational functions by identifying key features and understanding their behavior.
Earn points, unlock achievements, and progress through increasingly challenging levels!

### 🎮 Game Features:
- **Interactive Graphing**: Visualize functions with highlighted features
- **Multiple Game Modes**: Practice different skills
- **Progressive Difficulty**: Start simple, build complexity
- **Achievement System**: Earn badges for mastery
- **Real-time Feedback**: Learn from mistakes instantly
""")

# Sidebar for game controls and stats
with st.sidebar:
    st.header("🎮 Game Dashboard")
    
    # Game mode selection
    game_mode = st.selectbox(
        "Select Game Mode:",
        ["Function Input", "Feature Quiz", "Graph Builder", "End Behavior Race"],
        key="game_mode_selector"
    )
    
    # Stats display
    st.subheader("📊 Your Stats")
    st.metric("Current Level", st.session_state.level)
    st.metric("Total Score", st.session_state.score)
    
    # Achievements
    st.subheader("🏆 Achievements")
    if st.session_state.achievements:
        for achievement in st.session_state.achievements:
            st.success(f"✅ {achievement}")
    else:
        st.info("Complete challenges to earn achievements!")
    
    # Reset button
    if st.button("🔄 Reset Game"):
        st.session_state.score = 0
        st.session_state.level = 1
        st.session_state.current_function = None
        st.session_state.achievements = []
        st.rerun()

# Main game area
game_modes = GameModes()

if game_mode == "Function Input":
    game_modes.function_input_mode()
elif game_mode == "Feature Quiz":
    game_modes.feature_quiz_mode()
elif game_mode == "Graph Builder":
    game_modes.graph_builder_mode()
elif game_mode == "End Behavior Race":
    game_modes.end_behavior_race_mode()

# Achievement check
def check_achievements():
    """Check for new achievements based on current stats"""
    new_achievements = []
    
    if st.session_state.score >= 10 and "First Steps" not in st.session_state.achievements:
        new_achievements.append("First Steps")
    
    if st.session_state.score >= 50 and "Asymptote Ace" not in st.session_state.achievements:
        new_achievements.append("Asymptote Ace")
    
    if st.session_state.level >= 5 and "Level Master" not in st.session_state.achievements:
        new_achievements.append("Level Master")
    
    if st.session_state.score >= 100 and "Function Expert" not in st.session_state.achievements:
        new_achievements.append("Function Expert")
    
    for achievement in new_achievements:
        if achievement not in st.session_state.achievements:
            st.session_state.achievements.append(achievement)
            st.success(f"🎉 Achievement Unlocked: {achievement}!")

check_achievements()

# Footer with instructions
st.markdown("""
---
### 📚 Quick Reference:
- **Vertical Asymptotes**: Values where denominator = 0 (but numerator ≠ 0)
- **Horizontal Asymptotes**: Determined by degree comparison of numerator/denominator
- **Holes**: Common factors in numerator and denominator
- **X-intercepts**: Values where numerator = 0 (but denominator ≠ 0)
- **Y-intercept**: Function value at x = 0
""")
