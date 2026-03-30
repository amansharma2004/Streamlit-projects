import streamlit as st


st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

# Title and description
st.title("⚖️ BMI Calculator")
st.write("BMI (Body Mass Index) helps estimate whether a person’s body weight is appropriate for their height.")


col1, col2 = st.columns(2)
with col1:
    height_input = st.text_input("Height (m)")
with col2:
    weight_input = st.text_input("Weight (kg)")

# Calculate button
if st.button("Calculate BMI"):
    if not height_input or not weight_input:
        st.warning("Please enter both height and weight.")
    else:
        try:
            height = float(height_input)
            weight = float(weight_input)

            if height <= 0 or weight <= 0:
                st.error("Height and Weight must be greater than 0.")
            else:
                bmi = weight / (height * height)
                exact_bmi = round(bmi, 1)

                
                st.metric(label="Your BMI", value=exact_bmi)

                
                if exact_bmi < 18.5:
                    st.warning(f"Underweight: Your BMI is {exact_bmi}")
                elif 18.5 <= exact_bmi <= 24.9:
                    st.success(f"Normal Weight: Your BMI is {exact_bmi}")
                elif 25 <= exact_bmi <= 29:
                    st.info(f"Overweight: Your BMI is {exact_bmi}")
                else:
                    st.error(f"Obese: Your BMI is {exact_bmi}")

               
                with st.expander("💡 Health Tips"):
                    if exact_bmi < 18.5:
                        st.write("Consider a balanced diet with more calories and protein.")
                    elif 18.5 <= exact_bmi <= 24.9:
                        st.write("Great! Maintain your healthy lifestyle with regular exercise.")
                    elif 25 <= exact_bmi <= 29:
                        st.write("Try increasing physical activity and monitoring calorie intake.")
                    else:
                        st.write("Consult a healthcare provider for personalized advice.")
        except ValueError:
            st.error("Please enter valid numeric values for height and weight.")
