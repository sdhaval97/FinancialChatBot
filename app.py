from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
api_key = ""
openai_client = OpenAI(api_key=api_key)

def portfolio_alignment(age, goals):
    """
    Function to align the portfolio with the duration of the client's goals.
    """
    recommended_stock_percentage = max(110 - age, 0)
    
    goal_durations = [goal['duration'] for goal in goals]
    
    if all(duration == 'long-term' for duration in goal_durations):
        recommendation = f"For a client with long-term goals, an aggressive investment strategy is recommended. \
        The percentage of stocks in the portfolio should be {recommended_stock_percentage}%."
    else:
        recommendation = "Recommendation for portfolio alignment based on specific goals."
    
    return recommendation

def retirement_planning(retirement_age, desired_income):
    """
    Function to calculate recommended monthly savings for retirement.
    """
    recommended_savings = desired_income / retirement_age
    
    return recommended_savings

def budgeting(income, expenses):
    """
    Function to provide budgeting recommendations based on income and expenses.
    """
    basics = 0.5 * income
    blissful = 0.2 * income
    intentional = 0.3 * income
    void = 0  
    
    if expenses > basics:
        budget_recommendation = "Your expenses exceed the recommended basics (needs) budget. Consider reducing non-essential expenses."
    else:
        budget_recommendation = "Your expenses are within the recommended basics (needs) budget."
    
    return budget_recommendation


def age_specific_planning(age):
    """
    Function to provide age-specific financial planning advice.
    """
    if age >= 20 and age <= 30:
        planning_advice = "Financial planning advice for age group 20-30."
    elif age >= 30 and age <= 40:
        planning_advice = "Financial planning advice for age group 30-40."
    
    return planning_advice

def generate_investment_analysis_response(accounts, risk_tolerance):
    prompt = f"""
    Assess the growth potential of investments in different accounts (RRSP, TFSA, and non-registered). 
    The user's investment details are as follows:
    - RRSP: {accounts['RRSP']}
    - TFSA: {accounts['TFSA']}
    - Non-registered: {accounts['non_registered']}
    
    Provide insights on aligning investments with risk tolerance and suggest strategies for optimizing RRSP, TFSA, and non-registered account investments.
    """
    response = openai_client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
        stop=None
    )
    return response.choices[0].text.strip()

def generate_debt_repayment_response(debts, strategy):
    prompt = f"""
    Calculate efficient strategies for paying off debts, including {strategy} method. 
    The user's debt details are as follows:
    - Credit Cards: {debts['credit_cards']}
    - Student Loans: {debts['student_loans']}
    - Personal Loans: {debts['personal_loans']}
    
    Provide a detailed explanation of the chosen debt repayment strategy, highlighting advantages, disadvantages, and practical tips for implementation.
    """
    response = openai_client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
        stop=None
    )
    return response.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def process():
    age = int(request.form.get("age"))
    income = float(request.form.get("income"))
    expenses = float(request.form.get("expenses"))
    retirement_age = int(request.form.get("retirement_age"))
    desired_income = float(request.form.get("desired_income"))
    rrsp_amount = float(request.form.get("rrsp_amount"))
    tfsa_amount = float(request.form.get("tfsa_amount"))
    non_registered_amount = float(request.form.get("non_registered_amount"))
    credit_card_debt = float(request.form.get("credit_card_debt"))
    student_loan_debt = float(request.form.get("student_loan_debt"))
    personal_loan_debt = float(request.form.get("personal_loan_debt"))
    risk_tolerance = request.form.get("risk_tolerance")
    repayment_strategy = request.form.get("repayment_strategy")

    recommendation = portfolio_alignment(age, goals)  
    retirement_planning_response = retirement_planning(retirement_age, desired_income)
    budgeting_response = budgeting(income, expenses)
    age_specific_planning_response = age_specific_planning(age)

    investment_analysis_response = generate_investment_analysis_response({
        'RRSP': rrsp_amount,
        'TFSA': tfsa_amount,
        'non_registered': non_registered_amount
    }, risk_tolerance)

    debt_repayment_response = generate_debt_repayment_response({
        'credit_cards': credit_card_debt,
        'student_loans': student_loan_debt,
        'personal_loans': personal_loan_debt
    }, repayment_strategy)

    return render_template('results.html', recommendation=recommendation, retirement_planning_response=retirement_planning_response,
                           budgeting_response=budgeting_response, debt_repayment_strategy_response=debt_repayment_strategy_response,
                           age_specific_planning_response=age_specific_planning_response, investment_analysis_response=investment_analysis_response,
                           debt_repayment_response=debt_repayment_response)

if __name__ == "__main__":
    app.run(debug=True)
