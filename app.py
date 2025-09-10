import streamlit as st
import numpy as np
import pandas as pd

def calculate_arithmetic_sequence(first_term, common_diff, n_terms):
    """Calculate arithmetic sequence terms and sum"""
    if n_terms <= 0:
        return [], 0
    
    # Generate terms using arithmetic sequence formula: a_n = a_1 + (n-1)d
    terms = [first_term + i * common_diff for i in range(n_terms)]
    
    # Calculate sum using formula: S_n = n/2 * (2a + (n-1)d)
    sequence_sum = n_terms / 2 * (2 * first_term + (n_terms - 1) * common_diff)
    
    return terms, sequence_sum

def calculate_geometric_sequence(first_term, common_ratio, n_terms):
    """Calculate geometric sequence terms and sum"""
    if n_terms <= 0:
        return [], 0
    
    if first_term == 0:
        return [0] * n_terms, 0
    
    # Generate terms using geometric sequence formula: a_n = a_1 * r^(n-1)
    terms = [first_term * (common_ratio ** i) for i in range(n_terms)]
    
    # Calculate sum using formula
    if common_ratio == 1:
        # If ratio is 1, sum is simply n * first_term
        sequence_sum = n_terms * first_term
    else:
        # S_n = a * (1 - r^n) / (1 - r)
        sequence_sum = first_term * (1 - common_ratio ** n_terms) / (1 - common_ratio)
    
    return terms, sequence_sum

def main():
    st.title("🔢 Arithmetic and Geometric Sequence Calculator")
    st.markdown("Calculate sequences, view terms, and compute sums for arithmetic and geometric progressions.")
    
    # Create tabs for different sequence types
    tab1, tab2 = st.tabs(["📈 Arithmetic Sequences", "📊 Geometric Sequences"])
    
    with tab1:
        st.header("Arithmetic Sequence Calculator")
        st.markdown("An arithmetic sequence has a constant difference between consecutive terms.")
        st.markdown("**Formula:** a_n = a₁ + (n-1)d")
        
        # Input fields for arithmetic sequence
        col1, col2, col3 = st.columns(3)
        
        with col1:
            arith_first_term = st.number_input(
                "First Term (a₁)", 
                value=1.0, 
                step=0.1,
                key="arith_first"
            )
        
        with col2:
            common_diff = st.number_input(
                "Common Difference (d)", 
                value=1.0, 
                step=0.1,
                key="arith_diff"
            )
        
        with col3:
            arith_n_terms = st.number_input(
                "Number of Terms (n)", 
                min_value=1, 
                max_value=1000, 
                value=10,
                step=1,
                key="arith_n"
            )
        
        if st.button("Calculate Arithmetic Sequence", key="calc_arith"):
            try:
                terms, sequence_sum = calculate_arithmetic_sequence(arith_first_term, common_diff, arith_n_terms)
                
                if terms:
                    st.success("✅ Calculation Complete!")
                    
                    # Display the sequence
                    st.subheader("📋 Sequence Terms")
                    
                    # Create a formatted display of terms
                    if len(terms) <= 20:
                        # Show all terms if 20 or fewer
                        terms_str = ", ".join([f"{term:.3f}" if term != int(term) else str(int(term)) for term in terms])
                        st.write(f"**Terms:** {terms_str}")
                    else:
                        # Show first 10 and last 10 terms if more than 20
                        first_10 = terms[:10]
                        last_10 = terms[-10:]
                        first_str = ", ".join([f"{term:.3f}" if term != int(term) else str(int(term)) for term in first_10])
                        last_str = ", ".join([f"{term:.3f}" if term != int(term) else str(int(term)) for term in last_10])
                        st.write(f"**First 10 terms:** {first_str}")
                        st.write(f"**...**")
                        st.write(f"**Last 10 terms:** {last_str}")
                    
                    # Display sum
                    st.subheader("🧮 Sum of Series")
                    sum_display = f"{sequence_sum:.3f}" if sequence_sum != int(sequence_sum) else str(int(sequence_sum))
                    st.write(f"**Sum of {arith_n_terms} terms:** {sum_display}")
                    
                    # Create a DataFrame for tabular view
                    if arith_n_terms <= 50:  # Only show table for reasonable number of terms
                        df = pd.DataFrame({
                            'Position (n)': range(1, len(terms) + 1),
                            'Term Value': terms
                        })
                        st.subheader("📊 Tabular View")
                        st.dataframe(df, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error calculating arithmetic sequence: {str(e)}")
    
    with tab2:
        st.header("Geometric Sequence Calculator")
        st.markdown("A geometric sequence has a constant ratio between consecutive terms.")
        st.markdown("**Formula:** a_n = a₁ × r^(n-1)")
        
        # Input fields for geometric sequence
        col1, col2, col3 = st.columns(3)
        
        with col1:
            geom_first_term = st.number_input(
                "First Term (a₁)", 
                value=1.0, 
                step=0.1,
                key="geom_first"
            )
        
        with col2:
            common_ratio = st.number_input(
                "Common Ratio (r)", 
                value=2.0, 
                step=0.1,
                key="geom_ratio"
            )
        
        with col3:
            geom_n_terms = st.number_input(
                "Number of Terms (n)", 
                min_value=1, 
                max_value=100, 
                value=10,
                step=1,
                key="geom_n"
            )
        
        # Warning for large ratios
        if abs(common_ratio) > 10 and geom_n_terms > 10:
            st.warning("⚠️ Large ratio with many terms may result in very large numbers!")
        
        if st.button("Calculate Geometric Sequence", key="calc_geom"):
            try:
                # Validate inputs
                if geom_first_term == 0:
                    st.info("ℹ️ First term is 0, all terms will be 0.")
                
                terms, sequence_sum = calculate_geometric_sequence(geom_first_term, common_ratio, geom_n_terms)
                
                if terms:
                    st.success("✅ Calculation Complete!")
                    
                    # Display the sequence
                    st.subheader("📋 Sequence Terms")
                    
                    # Check if numbers are getting too large
                    max_term = max(abs(term) for term in terms)
                    if max_term > 1e10:
                        st.warning("⚠️ Some terms are very large and may be displayed in scientific notation.")
                    
                    # Create a formatted display of terms
                    if len(terms) <= 20:
                        # Show all terms if 20 or fewer
                        terms_str = ", ".join([
                            f"{term:.3f}" if abs(term) < 1000 and term != int(term) 
                            else f"{term:.2e}" if abs(term) >= 1e6 
                            else str(int(term)) if term == int(term)
                            else f"{term:.3f}"
                            for term in terms
                        ])
                        st.write(f"**Terms:** {terms_str}")
                    else:
                        # Show first 10 and last 10 terms if more than 20
                        first_10 = terms[:10]
                        last_10 = terms[-10:]
                        first_str = ", ".join([
                            f"{term:.3f}" if abs(term) < 1000 and term != int(term) 
                            else f"{term:.2e}" if abs(term) >= 1e6 
                            else str(int(term)) if term == int(term)
                            else f"{term:.3f}"
                            for term in first_10
                        ])
                        last_str = ", ".join([
                            f"{term:.3f}" if abs(term) < 1000 and term != int(term) 
                            else f"{term:.2e}" if abs(term) >= 1e6 
                            else str(int(term)) if term == int(term)
                            else f"{term:.3f}"
                            for term in last_10
                        ])
                        st.write(f"**First 10 terms:** {first_str}")
                        st.write(f"**...**")
                        st.write(f"**Last 10 terms:** {last_str}")
                    
                    # Display sum
                    st.subheader("🧮 Sum of Series")
                    if abs(sequence_sum) >= 1e6:
                        sum_display = f"{sequence_sum:.2e}"
                    elif sequence_sum != int(sequence_sum):
                        sum_display = f"{sequence_sum:.3f}"
                    else:
                        sum_display = str(int(sequence_sum))
                    
                    st.write(f"**Sum of {geom_n_terms} terms:** {sum_display}")
                    
                    # Additional information about convergence
                    if abs(common_ratio) < 1:
                        infinite_sum = geom_first_term / (1 - common_ratio)
                        inf_sum_display = f"{infinite_sum:.3f}" if infinite_sum != int(infinite_sum) else str(int(infinite_sum))
                        st.info(f"ℹ️ Since |r| < 1, this geometric series converges. The infinite sum would be: {inf_sum_display}")
                    elif abs(common_ratio) > 1:
                        st.info("ℹ️ Since |r| > 1, this geometric series diverges (grows without bound).")
                    else:
                        st.info("ℹ️ Since |r| = 1, this series does not converge to a finite sum.")
                    
                    # Create a DataFrame for tabular view (limit for performance)
                    if geom_n_terms <= 50:  # Only show table for reasonable number of terms
                        df = pd.DataFrame({
                            'Position (n)': range(1, len(terms) + 1),
                            'Term Value': terms
                        })
                        st.subheader("📊 Tabular View")
                        st.dataframe(df, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error calculating geometric sequence: {str(e)}")
    
    # Add educational information
    st.markdown("---")
    with st.expander("📚 Learn More About Sequences"):
        st.markdown("""
        ### Arithmetic Sequences
        - **Definition:** A sequence where each term after the first is obtained by adding a constant difference to the previous term.
        - **General Term:** a_n = a₁ + (n-1)d
        - **Sum Formula:** S_n = n/2 × [2a₁ + (n-1)d] or S_n = n/2 × (a₁ + a_n)
        
        ### Geometric Sequences  
        - **Definition:** A sequence where each term after the first is obtained by multiplying the previous term by a constant ratio.
        - **General Term:** a_n = a₁ × r^(n-1)
        - **Sum Formula:** S_n = a₁ × (1 - r^n) / (1 - r) when r ≠ 1
        - **Infinite Sum:** S_∞ = a₁ / (1 - r) when |r| < 1
        
        ### Examples
        - **Arithmetic:** 2, 5, 8, 11, 14... (first term = 2, common difference = 3)
        - **Geometric:** 3, 6, 12, 24, 48... (first term = 3, common ratio = 2)
        """)

if __name__ == "__main__":
    main()
