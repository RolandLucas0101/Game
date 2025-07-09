import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import warnings
warnings.filterwarnings('ignore')

class RationalAnalyzer:
    """Class to analyze rational functions and identify key features"""
    
    def __init__(self, numerator_str, denominator_str):
        self.x = sp.Symbol('x')
        try:
            self.numerator = sp.sympify(numerator_str)
            self.denominator = sp.sympify(denominator_str)
            self.function = self.numerator / self.denominator
            self.valid = True
            self.error_message = None
        except Exception as e:
            self.valid = False
            self.error_message = f"Invalid function: {str(e)}"
    
    def find_vertical_asymptotes(self):
        """Find vertical asymptotes by solving denominator = 0"""
        if not self.valid:
            return []
        
        try:
            # Find roots of denominator
            denom_roots = sp.solve(self.denominator, self.x)
            
            # Check which roots are actual asymptotes (not holes)
            asymptotes = []
            for root in denom_roots:
                if root.is_real:
                    # Check if it's a hole (common factor)
                    if not self.is_hole(root):
                        asymptotes.append(float(root))
            
            return sorted(asymptotes)
        except:
            return []
    
    def find_horizontal_asymptote(self):
        """Find horizontal asymptote based on degree comparison"""
        if not self.valid:
            return None
        
        try:
            # Get degrees of numerator and denominator
            num_degree = sp.degree(self.numerator, self.x)
            den_degree = sp.degree(self.denominator, self.x)
            
            if num_degree < den_degree:
                return 0
            elif num_degree == den_degree:
                # Ratio of leading coefficients
                num_leading = sp.LC(self.numerator, self.x)
                den_leading = sp.LC(self.denominator, self.x)
                return float(num_leading / den_leading)
            else:
                # No horizontal asymptote (degree of num > degree of den)
                return None
        except:
            return None
    
    def find_holes(self):
        """Find holes (removable discontinuities)"""
        if not self.valid:
            return []
        
        try:
            # Factor numerator and denominator
            num_factors = sp.factor(self.numerator)
            den_factors = sp.factor(self.denominator)
            
            # Find common factors
            common_factors = sp.gcd(self.numerator, self.denominator)
            
            if common_factors == 1:
                return []  # No common factors
            
            # Find roots of common factors
            holes = []
            common_roots = sp.solve(common_factors, self.x)
            
            for root in common_roots:
                if root.is_real:
                    # Calculate y-coordinate of hole
                    simplified_num = sp.simplify(self.numerator / common_factors)
                    simplified_den = sp.simplify(self.denominator / common_factors)
                    y_val = float(simplified_num.subs(self.x, root) / simplified_den.subs(self.x, root))
                    holes.append((float(root), y_val))
            
            return holes
        except:
            return []
    
    def is_hole(self, x_val):
        """Check if a point is a hole"""
        holes = self.find_holes()
        return any(abs(hole[0] - x_val) < 1e-10 for hole in holes)
    
    def find_x_intercepts(self):
        """Find x-intercepts by solving numerator = 0"""
        if not self.valid:
            return []
        
        try:
            num_roots = sp.solve(self.numerator, self.x)
            intercepts = []
            
            for root in num_roots:
                if root.is_real:
                    # Check if it's not a hole
                    if not self.is_hole(root):
                        intercepts.append(float(root))
            
            return sorted(intercepts)
        except:
            return []
    
    def find_y_intercept(self):
        """Find y-intercept by evaluating f(0)"""
        if not self.valid:
            return None
        
        try:
            if self.denominator.subs(self.x, 0) != 0:
                return float(self.function.subs(self.x, 0))
            else:
                return None  # Vertical asymptote at x=0
        except:
            return None
    
    def analyze_end_behavior(self):
        """Analyze end behavior (limits as x approaches ±∞)"""
        if not self.valid:
            return None, None
        
        try:
            limit_pos_inf = sp.limit(self.function, self.x, sp.oo)
            limit_neg_inf = sp.limit(self.function, self.x, -sp.oo)
            
            # Convert to float if possible
            try:
                limit_pos_inf = float(limit_pos_inf) if limit_pos_inf.is_finite else str(limit_pos_inf)
            except:
                limit_pos_inf = str(limit_pos_inf)
            
            try:
                limit_neg_inf = float(limit_neg_inf) if limit_neg_inf.is_finite else str(limit_neg_inf)
            except:
                limit_neg_inf = str(limit_neg_inf)
            
            return limit_neg_inf, limit_pos_inf
        except:
            return None, None
    
    def plot_function(self, x_range=(-10, 10), y_range=(-10, 10)):
        """Plot the rational function with all features highlighted"""
        if not self.valid:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create x values for plotting
        x_vals = np.linspace(x_range[0], x_range[1], 2000)
        
        # Calculate y values, handling discontinuities
        y_vals = []
        for x_val in x_vals:
            try:
                y_val = float(self.function.subs(self.x, x_val))
                if abs(y_val) > 1000:  # Avoid plotting extreme values
                    y_vals.append(np.nan)
                else:
                    y_vals.append(y_val)
            except:
                y_vals.append(np.nan)
        
        y_vals = np.array(y_vals)
        
        # Plot the function
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
        
        # Plot vertical asymptotes
        v_asymptotes = self.find_vertical_asymptotes()
        for va in v_asymptotes:
            ax.axvline(x=va, color='red', linestyle='--', alpha=0.7, label='Vertical Asymptote' if va == v_asymptotes[0] else "")
        
        # Plot horizontal asymptote
        h_asymptote = self.find_horizontal_asymptote()
        if h_asymptote is not None:
            ax.axhline(y=h_asymptote, color='green', linestyle='--', alpha=0.7, label='Horizontal Asymptote')
        
        # Plot holes
        holes = self.find_holes()
        for hole_x, hole_y in holes:
            circle = Circle((hole_x, hole_y), 0.1, color='white', ec='blue', linewidth=2, zorder=5)
            ax.add_patch(circle)
        
        # Plot x-intercepts
        x_intercepts = self.find_x_intercepts()
        for xi in x_intercepts:
            ax.plot(xi, 0, 'ro', markersize=8, label='X-intercept' if xi == x_intercepts[0] else "")
        
        # Plot y-intercept
        y_intercept = self.find_y_intercept()
        if y_intercept is not None:
            ax.plot(0, y_intercept, 'go', markersize=8, label='Y-intercept')
        
        # Formatting
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('f(x)', fontsize=12)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Add title with function
        ax.set_title(f'f(x) = ({self.numerator})/({self.denominator})', fontsize=14, pad=20)
        
        plt.tight_layout()
        return fig
    
    def get_analysis_summary(self):
        """Get a complete analysis summary"""
        if not self.valid:
            return {"error": self.error_message}
        
        return {
            "vertical_asymptotes": self.find_vertical_asymptotes(),
            "horizontal_asymptote": self.find_horizontal_asymptote(),
            "holes": self.find_holes(),
            "x_intercepts": self.find_x_intercepts(),
            "y_intercept": self.find_y_intercept(),
            "end_behavior": self.analyze_end_behavior()
        }
