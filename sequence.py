# (1)
# Complete the sequence_calculator function, which should
# Return the n-th number of the sequence S_n, defined as:
# S_n = 3*S_(n-1) - S_(n-2), with S_0 = 0 and S_1 = 1.
# Your implementation should minimize the execution time.
#
# (2)
# Find the time complexity of the proposed solution, using
# the "Big O" notation, and explain in detail why such
# complexity is obtained, for n ranging from 0 to at least
# 100000. HINT: you are dealing with very large numbers!
#
# (3)
# Plot the execution time VS n (again, for n ranging from 0
# to at least 100000).
#
# (4)
# Confirm that the empirically obtained time complexity curve
# from (3) matches the claimed time complexity from (2) (e.g.
# by using curve fitting techniques).

import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import sys

def sequence_calculator(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, 3*b - a
    
    return b

# Measure execution time for different n values
def measure_execution_time(max_n=100000, num_samples=50):
    n_values = np.linspace(0, max_n, num_samples, dtype=int)
    times = []
    
    for n in n_values:
        start_time = time.time()
        sequence_calculator(n)
        end_time = time.time()
        times.append(end_time - start_time)
    
    return n_values, times

# Function for curve fitting - linear for O(n)
def linear_func(x, a, b):
    return a * x + b

# Add these functions to test different complexity models
def quadratic_func(x, a, b, c):
    return a * x * x + b * x + c

def logarithmic_func(x, a, b, c):
    return a * x * np.log(x + 1) + b * x + c

# Add exponential function for fitting
def exp_func(x, a, b, c):
    return a * np.exp(b * x) + c

# Plot execution time vs n
def plot_execution_time():
    n_values, times = measure_execution_time()
    
    # Calculate R² values
    ss_tot = np.sum((times - np.mean(times))**2)
    
    # Linear fitting
    popt_linear, _ = curve_fit(linear_func, n_values, times)
    residuals_linear = times - linear_func(n_values, *popt_linear)
    ss_res_linear = np.sum(residuals_linear**2)
    r2_linear = 1 - (ss_res_linear / ss_tot)
    
    # Quadratic fitting
    popt_quad, _ = curve_fit(quadratic_func, n_values, times)
    residuals_quad = times - quadratic_func(n_values, *popt_quad)
    ss_res_quad = np.sum(residuals_quad**2)
    r2_quad = 1 - (ss_res_quad / ss_tot)
    
    # n log n fitting
    popt_log, _ = curve_fit(logarithmic_func, n_values, times)
    residuals_log = times - logarithmic_func(n_values, *popt_log)
    ss_res_log = np.sum(residuals_log**2)
    r2_log = 1 - (ss_res_log / ss_tot)
    
    # Exponential fitting - need to use a subset of data to avoid overflow
    # Scale down x values for exponential fit to avoid numerical issues
    x_scaled = n_values / np.max(n_values)
    try:
        # Use a lower upper bound for optimization to avoid overflow
        popt_exp, _ = curve_fit(lambda x, a, b, c: a * np.exp(b * x) + c, 
                               x_scaled, times, 
                               bounds=([0, 0, -np.inf], [np.inf, 10, np.inf]))
        
        # Scale parameters back for plotting
        a_exp, b_exp, c_exp = popt_exp
        b_exp = b_exp / np.max(n_values)  # Adjust b based on scaling
        
        # Calculate R² for exponential fit
        residuals_exp = times - (a_exp * np.exp(b_exp * n_values) + c_exp)
        ss_res_exp = np.sum(residuals_exp**2)
        r2_exp = 1 - (ss_res_exp / ss_tot)
    except:
        print("Warning: Could not fit exponential function (numerical overflow)")
        r2_exp = 0
    
    # Create plots with the calculated values
    fig, axs = plt.subplots(3, 2, figsize=(14, 16))
    fig.suptitle('Execution Time vs n - Complexity Analysis', fontsize=16)
    
    # Add vertical space between rows
    plt.subplots_adjust(hspace=0.44)
    
    # Raw data plot
    axs[0, 0].scatter(n_values, times, label='Measured times')
    axs[0, 0].set_title('Raw Measurement Data')
    axs[0, 0].set_xlabel('n')
    axs[0, 0].set_ylabel('Time (seconds)')
    axs[0, 0].grid(True)
    
    # Linear fitting plot
    axs[0, 1].scatter(n_values, times, label='Measured times')
    axs[0, 1].plot(n_values, linear_func(n_values, *popt_linear), 'r-', 
                   label=f'O(n): {popt_linear[0]:.2e}*n + {popt_linear[1]:.2e}')
    axs[0, 1].set_title('Linear Fit - O(n)')
    axs[0, 1].set_xlabel('n')
    axs[0, 1].set_ylabel('Time (seconds)')
    axs[0, 1].legend()
    axs[0, 1].grid(True)
    
    # Quadratic fitting plot
    axs[1, 0].scatter(n_values, times, label='Measured times')
    axs[1, 0].plot(n_values, quadratic_func(n_values, *popt_quad), 'g-', 
                  label=f'O(n²): {popt_quad[0]:.2e}*n² + {popt_quad[1]:.2e}*n + {popt_quad[2]:.2e}')
    axs[1, 0].set_title('Quadratic Fit - O(n²)')
    axs[1, 0].set_xlabel('n')
    axs[1, 0].set_ylabel('Time (seconds)')
    axs[1, 0].legend()
    axs[1, 0].grid(True)
    
    # n log n fitting plot
    axs[1, 1].scatter(n_values, times, label='Measured times')
    axs[1, 1].plot(n_values, logarithmic_func(n_values, *popt_log), 'b-', 
                  label=f'O(n log n)')
    axs[1, 1].set_title('n log n Fit - O(n log n)')
    axs[1, 1].set_xlabel('n')
    axs[1, 1].set_ylabel('Time (seconds)')
    axs[1, 1].legend()
    axs[1, 1].grid(True)
    
    # Exponential fitting plot
    axs[2, 0].scatter(n_values, times, label='Measured times')
    if r2_exp > 0:
        axs[2, 0].plot(n_values, a_exp * np.exp(b_exp * n_values) + c_exp, 'm-',
                      label=f'O(e^n): {a_exp:.2e}*e^({b_exp:.2e}*n) + {c_exp:.2e}')
        axs[2, 0].set_title('Exponential Fit - O(e^n)')
    else:
        axs[2, 0].text(0.5, 0.5, 'Exponential fit failed (numerical overflow)', 
                     horizontalalignment='center', verticalalignment='center', 
                     transform=axs[2, 0].transAxes)
        axs[2, 0].set_title('Exponential Fit - Failed')
    axs[2, 0].set_xlabel('n')
    axs[2, 0].set_ylabel('Time (seconds)')
    axs[2, 0].legend()
    axs[2, 0].grid(True)
    
    # Summary panel
    axs[2, 1].axis('off')
    axs[2, 1].text(0.1, 0.9, "Goodness of Fit (R²):", fontsize=12)
    axs[2, 1].text(0.1, 0.8, f"Linear: {r2_linear:.6f}", fontsize=10)
    axs[2, 1].text(0.1, 0.7, f"Quadratic: {r2_quad:.6f}", fontsize=10)
    axs[2, 1].text(0.1, 0.6, f"n log n: {r2_log:.6f}", fontsize=10)
    axs[2, 1].text(0.1, 0.5, f"Exponential: {r2_exp:.6f}", fontsize=10)
    
    # Determine and display best model
    models = {'Linear (O(n))': r2_linear, 'Quadratic (O(n²))': r2_quad, 
              'n log n (O(n log n))': r2_log, 'Exponential (O(e^n))': r2_exp}
    best_model = max(models, key=models.get)
    axs[2, 1].text(0.1, 0.3, f"Best fit: {best_model}", fontsize=12, fontweight='bold')
    axs[2, 1].text(0.1, 0.2, f"R² = {models[best_model]:.6f}", fontsize=10)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('sequence_time_complexity.png')
    plt.show()
    
    print(f"R² values - Linear: {r2_linear:.6f}, Quadratic: {r2_quad:.6f}, n log n: {r2_log:.6f}, Exponential: {r2_exp:.6f}")
    print(f"{best_model} provides the best fit with R² = {models[best_model]:.6f}")

def main():
    # Get result for n=100000
    result = sequence_calculator(100000)
    
    # Increase limit for string conversion
    sys.set_int_max_str_digits(100000)
    
    # Find the order of magnitude
    order = len(str(result)) - 1
    
    # Display in standard scientific notation
    coefficient = result / (10**order)
    print(f"S_100000 = {coefficient:.6f} × 10^{order}")
    
    # Plot time complexity
    plot_execution_time()

if __name__ == "__main__":
    main()

"""
Time complexity analysis:

The implemented solution has O(n²) time complexity because:
1. We use a simple iterative approach with a loop that runs (n-1) times
2. Each iteration performs arithmetic on increasingly large numbers
3. As n grows, the sequence values grow exponentially in magnitude
4. Python's arbitrary-precision integer operations take O(m) time where m is the number of bits
5. The number of bits in S_n grows linearly with n, making each operation O(n)

Therefore, O(n) loop iterations × O(n) cost per operation = O(n²) overall complexity.

The curve fitting confirms the quadratic relationship between execution time 
and n, validating the O(n²) time complexity, as shown by the higher R² value
for the quadratic model compared to linear.
"""
