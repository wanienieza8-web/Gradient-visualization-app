import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.misc import derivative

# Page configuration
st.set_page_config(page_title="Gradient Visualizer", layout="wide")

st.title("🎯 Gradient and Steepest Ascent Visualizer")
st.markdown("### Understanding Gradients in Calculus")

# Sidebar for inputs
st.sidebar.header("📊 Control Panel")

# Function selection
st.sidebar.subheader("1. Choose a Function")
function_choice = st.sidebar.selectbox(
    "Select f(x, y):",
    ["x² + y²", "x² - y²", "sin(x) × cos(y)", "x³ - 3xy²", "Custom"]
)

# Custom function input
if function_choice == "Custom":
    custom_func = st.sidebar.text_input(
        "Enter your function (use x and y):",
        "x**2 + y**2"
    )
else:
    custom_func = None

# Point selection
st.sidebar.subheader("2. Choose a Point")
col1, col2 = st.sidebar.columns(2)
x_point = col1.number_input("x-coordinate:", value=1.0, step=0.5)
y_point = col2.number_input("y-coordinate:", value=1.0, step=0.5)

# Range selection
st.sidebar.subheader("3. Adjust View Range")
view_range = st.sidebar.slider("Range:", 1, 5, 3)

# Define the function based on selection
def get_function(choice, custom=None):
    if choice == "x² + y²":
        return lambda x, y: x**2 + y**2
    elif choice == "x² - y²":
        return lambda x, y: x**2 - y**2
    elif choice == "sin(x) × cos(y)":
        return lambda x, y: np.sin(x) * np.cos(y)
    elif choice == "x³ - 3xy²":
        return lambda x, y: x**3 - 3*x*y**2
    elif choice == "Custom" and custom:
        try:
            return lambda x, y: eval(custom)
        except:
            st.sidebar.error("Invalid function! Using x² + y² instead.")
            return lambda x, y: x**2 + y**2
    else:
        return lambda x, y: x**2 + y**2

# Get the selected function
f = get_function(function_choice, custom_func)

# Calculate partial derivatives (gradient components)
def partial_x(x, y):
    return derivative(lambda x_val: f(x_val, y), x, dx=1e-6)

def partial_y(x, y):
    return derivative(lambda y_val: f(x, y_val), y, dx=1e-6)

# Calculate gradient at the chosen point
grad_x = partial_x(x_point, y_point)
grad_y = partial_y(x_point, y_point)
grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)

# Create grid for 3D surface
x_range = np.linspace(-view_range, view_range, 50)
y_range = np.linspace(-view_range, view_range, 50)
X, Y = np.meshgrid(x_range, y_range)

try:
    Z = f(X, Y)
except:
    st.error("Error evaluating function. Please check your custom function.")
    Z = X**2 + Y**2

# Calculate z-coordinate at the chosen point
z_point = f(x_point, y_point)

# Main content area
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("3D Visualization")
    
    # Create 3D surface plot
    fig = go.Figure()
    
    # Add surface
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis',
        opacity=0.9,
        name='f(x,y)'
    ))
    
    # Add the chosen point
    fig.add_trace(go.Scatter3d(
        x=[x_point], y=[y_point], z=[z_point],
        mode='markers',
        marker=dict(size=8, color='red'),
        name='Chosen Point'
    ))
    
    # Add gradient vector (scaled for visibility)
    scale = 0.5
    fig.add_trace(go.Scatter3d(
        x=[x_point, x_point + scale*grad_x],
        y=[y_point, y_point + scale*grad_y],
        z=[z_point, z_point],
        mode='lines+markers',
        line=dict(color='red', width=6),
        marker=dict(size=4),
        name='Gradient Vector'
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z = f(x,y)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        height=600,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("📐 Gradient Information")
    
    # Display function
    if function_choice != "Custom":
        st.markdown(f"**Function:** f(x, y) = {function_choice}")
    else:
        st.markdown(f"**Function:** f(x, y) = {custom_func}")
    
    st.markdown(f"**Point:** ({x_point}, {y_point})")
    st.markdown(f"**f({x_point}, {y_point}) = {z_point:.3f}**")
    
    st.markdown("---")
    
    st.markdown("**Gradient Vector ∇f:**")
    st.markdown(f"∇f = ({grad_x:.3f}, {grad_y:.3f})")
    
    st.markdown(f"**Magnitude:** {grad_magnitude:.3f}")
    
    # Direction angle
    if grad_magnitude > 0:
        angle = np.degrees(np.arctan2(grad_y, grad_x))
        st.markdown(f"**Direction:** {angle:.1f}°")
    
    st.markdown("---")
    
    # Explanation box
    st.info("""
    **What does the gradient mean?**
    
    🎯 **Direction:** The red arrow shows the direction of steepest ascent (fastest increase).
    
    📈 **Magnitude:** The length tells you how steep the climb is at this point.
    
    💡 **Intuition:** If you're standing on a hill at this point, the gradient points in the direction you should walk to climb uphill fastest!
    """)

# Detailed explanation at the bottom
st.markdown("---")
st.subheader("📚 Understanding Gradients")

explanation_col1, explanation_col2 = st.columns(2)

with explanation_col1:
    st.markdown("""
    **What is a Gradient?**
    
    The gradient of f(x, y) is a vector that contains the partial derivatives:
    
    ∇f = (∂f/∂x, ∂f/∂y)
    
    - **∂f/∂x**: How fast f changes when you move in the x-direction
    - **∂f/∂y**: How fast f changes when you move in the y-direction
    
    The gradient always points in the direction where the function increases fastest.
    """)

with explanation_col2:
    st.markdown("""
    **Key Properties:**
    
    ✅ Gradient points toward steepest ascent
    
    ✅ Length = rate of steepest ascent
    
    ✅ Perpendicular to level curves
    
    ✅ Zero gradient = flat point (local max/min)
    
    To find steepest **descent**, go in the opposite direction: -∇f
    """)

# Footer
st.markdown("---")
st.markdown("*Built for calculus students • Adjust the controls in the sidebar to explore different functions and points*")
