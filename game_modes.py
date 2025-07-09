import streamlit as st
import random
from rational_analyzer import RationalAnalyzer
import numpy as np

class GameModes:
    """Class containing different game modes for the rational function game"""
    
    def __init__(self):
        self.difficulty_levels = {
            1: {"complexity": "simple", "points_multiplier": 1},
            2: {"complexity": "medium", "points_multiplier": 1.5},
            3: {"complexity": "hard", "points_multiplier": 2},
            4: {"complexity": "expert", "points_multiplier": 3}
        }
    
    def function_input_mode(self):
        """Mode where students input their own rational function"""
        st.header("🔢 Function Input Mode")
        st.markdown("Enter a rational function and explore its properties!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input Function")
            numerator = st.text_input("Numerator (e.g., x+1, x**2-4)", value="x+1")
            denominator = st.text_input("Denominator (e.g., x-2, x**2-1)", value="x-2")
            
            show_features = st.multiselect(
                "Show Features:",
                ["Vertical Asymptotes", "Horizontal Asymptote", "Holes", "X-intercepts", "Y-intercept"],
                default=["Vertical Asymptotes", "Horizontal Asymptote"]
            )
            
            x_range = st.slider("X-axis range", -20, 20, (-10, 10))
            y_range = st.slider("Y-axis range", -20, 20, (-10, 10))
            
            if st.button("📊 Analyze Function"):
                self.analyze_and_display_function(numerator, denominator, show_features, x_range, y_range)
        
        with col2:
            st.subheader("Analysis Results")
            if st.session_state.get('current_analysis'):
                analysis = st.session_state.current_analysis
                
                if 'error' in analysis:
                    st.error(analysis['error'])
                else:
                    st.success("✅ Function analyzed successfully!")
                    
                    # Display features
                    if analysis['vertical_asymptotes']:
                        st.write(f"**Vertical Asymptotes:** {analysis['vertical_asymptotes']}")
                    
                    if analysis['horizontal_asymptote'] is not None:
                        st.write(f"**Horizontal Asymptote:** y = {analysis['horizontal_asymptote']}")
                    
                    if analysis['holes']:
                        st.write(f"**Holes:** {analysis['holes']}")
                    
                    if analysis['x_intercepts']:
                        st.write(f"**X-intercepts:** {analysis['x_intercepts']}")
                    
                    if analysis['y_intercept'] is not None:
                        st.write(f"**Y-intercept:** {analysis['y_intercept']}")
                    
                    end_behavior = analysis['end_behavior']
                    if end_behavior[0] is not None and end_behavior[1] is not None:
                        st.write(f"**End Behavior:** As x→-∞: {end_behavior[0]}, As x→+∞: {end_behavior[1]}")
    
    def feature_quiz_mode(self):
        """Quiz mode where students identify features of generated functions"""
        st.header("🧠 Feature Quiz Mode")
        st.markdown("Identify the features of randomly generated rational functions!")
        
        # Generate or retrieve current function
        if 'quiz_function' not in st.session_state or st.button("🎲 Generate New Function"):
            self.generate_quiz_function()
        
        if 'quiz_function' in st.session_state:
            func_data = st.session_state.quiz_function
            
            st.subheader("Current Function:")
            st.latex(f"f(x) = \\frac{{{func_data['numerator_latex']}}}{{{func_data['denominator_latex']}}}")
            
            # Display the graph
            analyzer = RationalAnalyzer(func_data['numerator'], func_data['denominator'])
            if analyzer.valid:
                fig = analyzer.plot_function(x_range=(-8, 8), y_range=(-8, 8))
                st.pyplot(fig)
                
                # Quiz questions
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Answer Questions:")
                    
                    # Vertical asymptotes
                    va_answer = st.text_input("Vertical asymptotes (comma-separated):", key="va_input")
                    
                    # Horizontal asymptote
                    ha_answer = st.text_input("Horizontal asymptote (or 'none'):", key="ha_input")
                    
                    # X-intercepts
                    xi_answer = st.text_input("X-intercepts (comma-separated):", key="xi_input")
                    
                    # Y-intercept
                    yi_answer = st.text_input("Y-intercept:", key="yi_input")
                
                with col2:
                    st.subheader("Your Progress:")
                    
                    if st.button("✅ Submit Answers"):
                        score = self.grade_quiz_answers(analyzer, va_answer, ha_answer, xi_answer, yi_answer)
                        st.session_state.score += score
                        
                        if score > 0:
                            st.success(f"Great job! You earned {score} points!")
                        else:
                            st.error("Try again! Check your answers.")
                        
                        # Show correct answers
                        analysis = analyzer.get_analysis_summary()
                        st.subheader("Correct Answers:")
                        st.write(f"Vertical asymptotes: {analysis['vertical_asymptotes']}")
                        st.write(f"Horizontal asymptote: {analysis['horizontal_asymptote']}")
                        st.write(f"X-intercepts: {analysis['x_intercepts']}")
                        st.write(f"Y-intercept: {analysis['y_intercept']}")
                        
                        # Level up check
                        if st.session_state.score >= st.session_state.level * 10:
                            st.session_state.level += 1
                            st.balloons()
                            st.success(f"🎉 Level up! You're now level {st.session_state.level}!")
    
    def graph_builder_mode(self):
        """Mode where students build graphs step by step"""
        st.header("🏗️ Graph Builder Mode")
        st.markdown("Build the graph step-by-step by identifying and placing features!")
        
        # Generate function if not exists
        if 'builder_function' not in st.session_state or st.button("🎯 New Challenge"):
            self.generate_builder_function()
        
        if 'builder_function' in st.session_state:
            func_data = st.session_state.builder_function
            
            st.subheader("Build this function:")
            st.latex(f"f(x) = \\frac{{{func_data['numerator_latex']}}}{{{func_data['denominator_latex']}}}")
            
            # Step-by-step building
            steps = ["Vertical Asymptotes", "Horizontal Asymptote", "Holes", "Intercepts", "Graph Shape"]
            
            if 'current_step' not in st.session_state:
                st.session_state.current_step = 0
            
            current_step = st.session_state.current_step
            
            if current_step < len(steps):
                st.subheader(f"Step {current_step + 1}: {steps[current_step]}")
                
                if steps[current_step] == "Vertical Asymptotes":
                    self.build_vertical_asymptotes(func_data)
                elif steps[current_step] == "Horizontal Asymptote":
                    self.build_horizontal_asymptote(func_data)
                elif steps[current_step] == "Holes":
                    self.build_holes(func_data)
                elif steps[current_step] == "Intercepts":
                    self.build_intercepts(func_data)
                elif steps[current_step] == "Graph Shape":
                    self.build_graph_shape(func_data)
            else:
                st.success("🎉 Graph completed! Well done!")
                if st.button("🔄 Start New Challenge"):
                    st.session_state.current_step = 0
                    del st.session_state.builder_function
                    st.rerun()
    
    def end_behavior_race_mode(self):
        """Timed mode focused on end behavior"""
        st.header("🏃 End Behavior Race")
        st.markdown("Race against time to determine end behavior!")
        
        if 'race_active' not in st.session_state:
            st.session_state.race_active = False
        
        if 'race_functions' not in st.session_state:
            st.session_state.race_functions = []
        
        if 'race_score' not in st.session_state:
            st.session_state.race_score = 0
        
        if not st.session_state.race_active:
            if st.button("🚀 Start Race!"):
                st.session_state.race_active = True
                st.session_state.race_functions = self.generate_race_functions(5)
                st.session_state.race_score = 0
                st.session_state.race_start_time = st.session_state.get('race_start_time', 0)
                st.rerun()
        else:
            if st.session_state.race_functions:
                current_func = st.session_state.race_functions[0]
                
                st.subheader("Determine the end behavior:")
                st.latex(f"f(x) = \\frac{{{current_func['numerator_latex']}}}{{{current_func['denominator_latex']}}}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("As x → -∞:")
                    neg_inf_answer = st.radio("", ["→ +∞", "→ -∞", "→ finite value"], key="neg_inf")
                
                with col2:
                    st.write("As x → +∞:")
                    pos_inf_answer = st.radio("", ["→ +∞", "→ -∞", "→ finite value"], key="pos_inf")
                
                if st.button("⚡ Submit"):
                    correct = self.check_end_behavior(current_func, neg_inf_answer, pos_inf_answer)
                    if correct:
                        st.session_state.race_score += 1
                        st.success("Correct! +1 point")
                    else:
                        st.error("Incorrect! Try the next one.")
                    
                    st.session_state.race_functions.pop(0)
                    st.rerun()
            else:
                st.success(f"🏁 Race finished! Final score: {st.session_state.race_score}/5")
                st.session_state.score += st.session_state.race_score * 2
                st.session_state.race_active = False
    
    def analyze_and_display_function(self, numerator, denominator, show_features, x_range, y_range):
        """Analyze and display a rational function"""
        analyzer = RationalAnalyzer(numerator, denominator)
        analysis = analyzer.get_analysis_summary()
        
        st.session_state.current_analysis = analysis
        
        if 'error' not in analysis:
            fig = analyzer.plot_function(x_range=x_range, y_range=y_range)
            st.pyplot(fig)
    
    def generate_quiz_function(self):
        """Generate a random rational function for quiz mode"""
        level = min(st.session_state.level, 4)
        
        if level == 1:
            # Simple linear functions
            a = random.randint(1, 3)
            b = random.randint(-3, 3)
            c = random.randint(-3, 3)
            d = random.randint(-3, 3)
            if c == 0: c = 1
            if d == 0: d = 1
            
            numerator = f"{a}*x + {b}"
            denominator = f"x + {c}"
            
        elif level == 2:
            # Quadratic denominators
            a = random.randint(1, 2)
            b = random.randint(-2, 2)
            c = random.randint(-3, 3)
            d = random.randint(-3, 3)
            
            numerator = f"{a}*x + {b}"
            denominator = f"x**2 + {c}*x + {d}"
            
        else:
            # More complex functions
            coeffs = [random.randint(-2, 2) for _ in range(6)]
            numerator = f"{coeffs[0]}*x**2 + {coeffs[1]}*x + {coeffs[2]}"
            denominator = f"{coeffs[3]}*x**2 + {coeffs[4]}*x + {coeffs[5]}"
        
        st.session_state.quiz_function = {
            'numerator': numerator,
            'denominator': denominator,
            'numerator_latex': numerator.replace('*', '').replace('**', '^'),
            'denominator_latex': denominator.replace('*', '').replace('**', '^')
        }
    
    def grade_quiz_answers(self, analyzer, va_answer, ha_answer, xi_answer, yi_answer):
        """Grade student answers in quiz mode"""
        score = 0
        analysis = analyzer.get_analysis_summary()
        
        # Check vertical asymptotes
        try:
            user_vas = [float(x.strip()) for x in va_answer.split(',') if x.strip()]
            correct_vas = analysis['vertical_asymptotes']
            if set(user_vas) == set(correct_vas):
                score += 2
        except:
            pass
        
        # Check horizontal asymptote
        try:
            correct_ha = analysis['horizontal_asymptote']
            if ha_answer.strip().lower() == 'none' and correct_ha is None:
                score += 2
            elif correct_ha is not None and abs(float(ha_answer.strip()) - correct_ha) < 0.01:
                score += 2
        except:
            pass
        
        # Check x-intercepts
        try:
            user_xis = [float(x.strip()) for x in xi_answer.split(',') if x.strip()]
            correct_xis = analysis['x_intercepts']
            if set(user_xis) == set(correct_xis):
                score += 1
        except:
            pass
        
        # Check y-intercept
        try:
            correct_yi = analysis['y_intercept']
            if correct_yi is not None and abs(float(yi_answer.strip()) - correct_yi) < 0.01:
                score += 1
        except:
            pass
        
        return score
    
    def generate_builder_function(self):
        """Generate function for graph builder mode"""
        # Similar to quiz function but with specific features
        a = random.randint(1, 2)
        b = random.randint(-2, 2)
        c = random.randint(-2, 2)
        d = random.randint(-2, 2)
        
        numerator = f"{a}*x + {b}"
        denominator = f"(x + {c})*(x + {d})"
        
        st.session_state.builder_function = {
            'numerator': numerator,
            'denominator': denominator,
            'numerator_latex': numerator.replace('*', ''),
            'denominator_latex': denominator.replace('*', '').replace('**', '^')
        }
    
    def build_vertical_asymptotes(self, func_data):
        """Build vertical asymptotes step"""
        st.write("Identify where the function has vertical asymptotes.")
        st.write("💡 Hint: Set the denominator equal to zero and solve.")
        
        va_input = st.text_input("Enter vertical asymptotes (comma-separated):")
        
        if st.button("Check Vertical Asymptotes"):
            analyzer = RationalAnalyzer(func_data['numerator'], func_data['denominator'])
            correct_vas = analyzer.find_vertical_asymptotes()
            
            try:
                user_vas = [float(x.strip()) for x in va_input.split(',') if x.strip()]
                if set(user_vas) == set(correct_vas):
                    st.success("✅ Correct! Moving to next step.")
                    st.session_state.current_step += 1
                    st.rerun()
                else:
                    st.error(f"❌ Incorrect. The correct vertical asymptotes are: {correct_vas}")
            except:
                st.error("❌ Invalid input format. Use comma-separated numbers.")
    
    def build_horizontal_asymptote(self, func_data):
        """Build horizontal asymptote step"""
        st.write("Identify the horizontal asymptote.")
        st.write("💡 Hint: Compare the degrees of the numerator and denominator.")
        
        ha_input = st.text_input("Enter horizontal asymptote (or 'none'):")
        
        if st.button("Check Horizontal Asymptote"):
            analyzer = RationalAnalyzer(func_data['numerator'], func_data['denominator'])
            correct_ha = analyzer.find_horizontal_asymptote()
            
            try:
                if ha_input.strip().lower() == 'none' and correct_ha is None:
                    st.success("✅ Correct! Moving to next step.")
                    st.session_state.current_step += 1
                    st.rerun()
                elif correct_ha is not None and abs(float(ha_input.strip()) - correct_ha) < 0.01:
                    st.success("✅ Correct! Moving to next step.")
                    st.session_state.current_step += 1
                    st.rerun()
                else:
                    st.error(f"❌ Incorrect. The correct horizontal asymptote is: {correct_ha}")
            except:
                st.error("❌ Invalid input format.")
    
    def build_holes(self, func_data):
        """Build holes step"""
        st.write("Identify any holes in the function.")
        st.write("💡 Hint: Look for common factors in numerator and denominator.")
        
        holes_input = st.text_input("Enter holes as (x,y) pairs or 'none':")
        
        if st.button("Check Holes"):
            analyzer = RationalAnalyzer(func_data['numerator'], func_data['denominator'])
            correct_holes = analyzer.find_holes()
            
            if holes_input.strip().lower() == 'none' and not correct_holes:
                st.success("✅ Correct! Moving to next step.")
                st.session_state.current_step += 1
                st.rerun()
            elif correct_holes:
                st.info(f"The correct holes are: {correct_holes}")
                st.session_state.current_step += 1
                st.rerun()
            else:
                st.session_state.current_step += 1
                st.rerun()
    
    def build_intercepts(self, func_data):
        """Build intercepts step"""
        st.write("Find the x and y intercepts.")
        
        xi_input = st.text_input("X-intercepts (comma-separated):")
        yi_input = st.text_input("Y-intercept:")
        
        if st.button("Check Intercepts"):
            analyzer = RationalAnalyzer(func_data['numerator'], func_data['denominator'])
            correct_xi = analyzer.find_x_intercepts()
            correct_yi = analyzer.find_y_intercept()
            
            xi_correct = False
            yi_correct = False
            
            try:
                user_xi = [float(x.strip()) for x in xi_input.split(',') if x.strip()]
                if set(user_xi) == set(correct_xi):
                    xi_correct = True
            except:
                pass
            
            try:
                if correct_yi is not None and abs(float(yi_input.strip()) - correct_yi) < 0.01:
                    yi_correct = True
            except:
                pass
            
            if xi_correct and yi_correct:
                st.success("✅ Correct! Moving to final step.")
                st.session_state.current_step += 1
                st.rerun()
            else:
                st.error(f"❌ Correct answers: X-intercepts: {correct_xi}, Y-intercept: {correct_yi}")
    
    def build_graph_shape(self, func_data):
        """Final step - show complete graph"""
        st.write("🎉 Final step: Here's your completed graph!")
        
        analyzer = RationalAnalyzer(func_data['numerator'], func_data['denominator'])
        fig = analyzer.plot_function()
        st.pyplot(fig)
        
        st.success("🏆 Graph building complete! +10 points!")
        st.session_state.score += 10
        st.session_state.current_step += 1
    
    def generate_race_functions(self, count):
        """Generate functions for end behavior race"""
        functions = []
        for _ in range(count):
            # Generate simple functions for quick analysis
            coeffs = [random.randint(1, 3) for _ in range(4)]
            
            numerator = f"{coeffs[0]}*x + {coeffs[1]}"
            denominator = f"{coeffs[2]}*x + {coeffs[3]}"
            
            functions.append({
                'numerator': numerator,
                'denominator': denominator,
                'numerator_latex': numerator.replace('*', ''),
                'denominator_latex': denominator.replace('*', '')
            })
        
        return functions
    
    def check_end_behavior(self, func_data, neg_inf_answer, pos_inf_answer):
        """Check end behavior answers"""
        analyzer = RationalAnalyzer(func_data['numerator'], func_data['denominator'])
        neg_limit, pos_limit = analyzer.analyze_end_behavior()
        
        # Simplified checking for race mode
        return True  # For now, give points for participation
