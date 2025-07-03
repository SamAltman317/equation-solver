import streamlit as st
from sympy import symbols, Eq, solve, Rational
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

st.set_page_config(page_title="一元一次方程求解器", layout="centered")

st.title("一元一次方程求解器")
# 不显示任何示例或说明

def preprocess_expr(expr):
    expr = expr.replace('[', '(').replace(']', ')')
    expr = expr.replace('{', '(').replace('}', ')')
    expr = expr.replace('^', '**')
    expr = expr.replace(' ', '')
    return expr

equation = st.text_input("请输入一元一次方程：", "")

if st.button("求解") and equation:
    try:
        eq_str = preprocess_expr(equation)
        if '=' not in eq_str:
            st.error("方程必须包含等号")
        else:
            x = symbols('x')
            left, right = eq_str.split('=')
            transformations = standard_transformations + (implicit_multiplication_application,)
            left_expr = parse_expr(left, transformations=transformations)
            right_expr = parse_expr(right, transformations=transformations)
            eq = Eq(left_expr, right_expr)
            sol = solve(eq, x)
            if not sol:
                st.warning("方程无解")
            elif len(sol) == 1:
                x_val = float(sol[0])
                x_frac = Rational(sol[0]).limit_denominator()
                st.success(f"方程的解为: x = {x_frac}  (小数: {x_val:.4f})")
            else:
                st.info(f"方程有多个解: {sol}")
    except Exception as e:
        st.error(f"解析失败: {e}") 