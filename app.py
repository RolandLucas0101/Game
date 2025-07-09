import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

def euler_method(k, x0, y0, x_final, h):
    """
    Implements Euler's method for solving dy/dx = ky
    
    Parameters:
    k: coefficient in the differential equation
    x0: initial x value
    y0: initial y value
    x_final: final x value to calculate to
    h: step size
    
    Returns:
    DataFrame with columns: step, x, y, dy_dx, explanation
    """
    # Calculate number of steps
    n_steps = int((x_final - x0) / h)
    
    # Initialize arrays
    x_values = [x0]
    y_values = [y0]
    dy_dx_values = [k * y0]
    explanations = [f"Initial condition: x₀ = {x0}, y₀ = {y0}"]
    
    # Perform Euler's method iterations
    for i in range(n_steps):
        x_current = x_values[-1]
        y_current = y_values[-1]
        dy_dx_current = k * y_current
        
        # Calculate next values
        x_next = x_current + h
        y_next = y_current + h * dy_dx_current
        
        x_values.append(x_next)
        y_values.append(y_next)
        dy_dx_values.append(k * y_next)
        
        explanation = f"y₍{i+1}₎ = {y_current:.6f} + {h} × {dy_dx_current:.6f} = {y_next:.6f}"
        explanations.append(explanation)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Step': range(len(x_values)),
        'x': x_values,
        'y': y_values,
        'dy/dx': dy_dx_values,
        'Calculation': explanations
    })
    
    return df

def analytical_solution(k, x0, y0, x_values):
    """
    Calculate the analytical solution for dy/dx = ky
    The analytical solution is y = y₀ * e^(k(x-x₀))
    """
    return y0 * np.exp(k * (x_values - x0))

def main():
    # Page configuration
    st.set_page_config(
        page_title="Euler's Method Calculator",
        page_icon="📊",
        layout="wide"
    )
    
    # Title and description
    st.title("Euler's Method for Differential Equations")
    st.markdown("### Solving dy/dx = ky using Euler's Method")
    
    # Educational context
    with st.expander("📚 About Euler's Method"):
        st.markdown("""
        **Euler's Method** is a numerical technique for solving ordinary differential equations (ODEs) with a given initial value.
        
        For the differential equation **dy/dx = ky**, where:
        - **k** is a constant coefficient
        - **y** is the dependent variable
        - **x** is the independent variable
        
        The method uses the iterative formula:
        **y₍ₙ₊₁₎ = yₙ + h × f(xₙ, yₙ)**
        
        Where:
        - **h** is the step size
        - **f(x,y) = ky** for our specific equation
        
        The analytical solution for comparison is: **y = y₀ × e^(k(x-x₀))**
        """)
    
    # Input section
    st.header("Input Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Differential Equation Parameters")
        k = st.number_input(
            "Coefficient k (dy/dx = ky)",
            value=0.5,
            step=0.1,
            format="%.3f",
            help="The proportionality constant in the differential equation"
        )
        
        h = st.number_input(
            "Step size (h)",
            value=0.1,
            min_value=0.001,
            max_value=1.0,
            step=0.01,
            format="%.3f",
            help="Smaller step sizes give more accurate results but require more calculations"
        )
    
    with col2:
        st.subheader("Initial Conditions & Range")
        x0 = st.number_input(
            "Initial x value (x₀)",
            value=0.0,
            step=0.1,
            format="%.3f"
        )
        
        y0 = st.number_input(
            "Initial y value (y₀)",
            value=1.0,
            step=0.1,
            format="%.3f"
        )
        
        x_final = st.number_input(
            "Final x value",
            value=2.0,
            step=0.1,
            format="%.3f"
        )
    
    # Validation
    if x_final <= x0:
        st.error("Final x value must be greater than initial x value!")
        return
    
    if h <= 0:
        st.error("Step size must be positive!")
        return
    
    # Calculate button
    if st.button("Calculate Euler's Method", type="primary"):
        try:
            # Perform Euler's method calculation
            with st.spinner("Calculating..."):
                results_df = euler_method(k, x0, y0, x_final, h)
            
            # Display results
            st.header("Results")
            
            # Summary
            final_x = results_df['x'].iloc[-1]
            final_y = results_df['y'].iloc[-1]
            n_steps = len(results_df) - 1
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Final x value", f"{final_x:.6f}")
            with col2:
                st.metric("Approximated y value", f"{final_y:.6f}")
            with col3:
                st.metric("Number of steps", n_steps)
            
            # Step-by-step table
            st.subheader("Step-by-Step Calculations")
            
            # Format the dataframe for display
            display_df = results_df.copy()
            display_df['x'] = display_df['x'].round(6)
            display_df['y'] = display_df['y'].round(6)
            display_df['dy/dx'] = display_df['dy/dx'].round(6)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Analytical solution comparison
            st.subheader("Comparison with Analytical Solution")
            
            # Calculate analytical solution
            x_analytical = np.linspace(x0, x_final, 1000)
            y_analytical = analytical_solution(k, x0, y0, x_analytical)
            
            # Calculate analytical solution at final point
            y_analytical_final = analytical_solution(k, x0, y0, final_x)
            
            # Display comparison
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Euler's Method Result", f"{final_y:.6f}")
            with col2:
                st.metric("Analytical Solution", f"{y_analytical_final:.6f}")
            with col3:
                error = abs(final_y - y_analytical_final)
                st.metric("Absolute Error", f"{error:.6f}")
            
            # Plot results
            st.subheader("Graphical Visualization")
            
            fig = go.Figure()
            
            # Add Euler's method points
            fig.add_trace(go.Scatter(
                x=results_df['x'],
                y=results_df['y'],
                mode='lines+markers',
                name="Euler's Method",
                line=dict(color='blue', width=2),
                marker=dict(size=6)
            ))
            
            # Add analytical solution
            fig.add_trace(go.Scatter(
                x=x_analytical,
                y=y_analytical,
                mode='lines',
                name='Analytical Solution',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title=f"Euler's Method vs Analytical Solution (dy/dx = {k}y)",
                xaxis_title="x",
                yaxis_title="y",
                legend=dict(x=0.02, y=0.98),
                template="plotly_white",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Error analysis
            st.subheader("Error Analysis")
            
            # Calculate errors at each step
            y_analytical_at_steps = analytical_solution(k, x0, y0, results_df['x'])
            errors = np.abs(results_df['y'] - y_analytical_at_steps)
            
            # Create error plot
            fig_error = go.Figure()
            
            fig_error.add_trace(go.Scatter(
                x=results_df['x'],
                y=errors,
                mode='lines+markers',
                name='Absolute Error',
                line=dict(color='orange', width=2),
                marker=dict(size=6)
            ))
            
            fig_error.update_layout(
                title="Absolute Error at Each Step",
                xaxis_title="x",
                yaxis_title="Absolute Error",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig_error, use_container_width=True)
            
            # Download results
            st.subheader("Download Results")
            
            # Create downloadable CSV
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name=f"euler_method_results_k{k}_h{h}.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")
            st.error("Please check your input parameters and try again.")
    
    # Example section
    st.header("Example Problems")
    
    with st.expander("💡 Try These Examples"):
        st.markdown("""
        **Example 1: Exponential Growth**
        - k = 0.5, x₀ = 0, y₀ = 1, x_final = 2, h = 0.1
        - Models population growth or compound interest
        
        **Example 2: Exponential Decay**
        - k = -0.3, x₀ = 0, y₀ = 100, x_final = 5, h = 0.2
        - Models radioactive decay or cooling
        
        **Example 3: High Precision**
        - k = 1.0, x₀ = 0, y₀ = 1, x_final = 1, h = 0.01
        - Compare accuracy with smaller step size
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit • Euler's Method Implementation*")

if __name__ == "__main__":
    main()
